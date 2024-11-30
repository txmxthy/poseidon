import json
import math
import gzip
from typing import Dict, List, Generator, TextIO, Union
from dataclasses import dataclass
from datetime import datetime
import os
from tqdm import tqdm


@dataclass
class Position:
    lat: float
    lon: float
    timestamp: int
    mmsi: str


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points using the haversine formula."""
    R = 6371e3  # Earth's radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) * math.sin(delta_phi / 2) + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2) * math.sin(delta_lambda / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def calculate_speed(pos1: Position, pos2: Position) -> float:
    """Calculate speed in knots between two positions."""
    distance = haversine_distance(pos1.lat, pos1.lon, pos2.lat, pos2.lon)
    time_diff = pos2.timestamp - pos1.timestamp
    if time_diff == 0:
        return 0
    # Convert m/s to knots (1 knot = 0.514444 m/s)
    return (distance / time_diff) / 0.514444


def parse_position_message(message: Dict) -> Union[Position, None]:
    """Parse AIS message and return Position if it's a position report."""
    msg_data = message.get('Message', {})
    msg_id = msg_data.get('MessageID')

    if msg_id not in [1, 2, 3, 18, 19, 27]:
        return None

    try:
        return Position(
            lat=float(msg_data['Latitude']),
            lon=float(msg_data['Longitude']),
            timestamp=int(message['UTCTimeStamp']),
            mmsi=str(msg_data['UserID'])
        )
    except (KeyError, ValueError):
        return None


def count_lines(filepath: str) -> int:
    """Count number of lines in a file, handling both .gz and regular files."""
    count = 0
    with open_file(filepath) as f:
        for _ in f:
            count += 1
    return count


def open_file(filepath: str) -> TextIO:
    """Open file handling both .gz and regular files."""
    if filepath.endswith('.gz'):
        return gzip.open(filepath, 'rt')
    return open(filepath, 'r')


def process_input_file(input_path: str) -> Generator[Position, None, None]:
    """Process input file and yield valid position reports."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    total_lines = count_lines(input_path)
    with open_file(input_path) as f:
        for line in tqdm(f, total=total_lines, desc="Processing messages"):
            try:
                message = json.loads(line)
                position = parse_position_message(message)
                if position:
                    yield position
            except json.JSONDecodeError:
                continue


def find_stops(positions: Generator[Position, None, None], min_duration: int = 3600) -> List[Position]:
    """Find vessel stops that last at least min_duration seconds."""
    stops = []
    vessel_data: Dict[str, List[Position]] = {}

    # Group positions by vessel MMSI
    print("Grouping positions by vessel...")
    for pos in positions:
        if pos.mmsi not in vessel_data:
            vessel_data[pos.mmsi] = []
        vessel_data[pos.mmsi].append(pos)

    # Process each vessel's positions
    print(f"Processing {len(vessel_data)} vessels...")
    for mmsi in tqdm(vessel_data.keys(), desc="Analyzing vessels"):
        positions = vessel_data[mmsi]
        positions.sort(key=lambda x: x.timestamp)

        stop_start = None
        prev_pos = None

        for pos in positions:
            if prev_pos is None:
                prev_pos = pos
                continue

            speed = calculate_speed(prev_pos, pos)

            if speed < 1.0:  # Less than 1 knot
                if stop_start is None:
                    stop_start = prev_pos
            elif stop_start is not None:
                if pos.timestamp - stop_start.timestamp >= min_duration:
                    stops.append(stop_start)
                stop_start = None

            prev_pos = pos

        # Check final stop
        if stop_start is not None and \
                positions[-1].timestamp - stop_start.timestamp >= min_duration:
            stops.append(stop_start)

    return stops


def create_geojson(stops: List[Position], output_path: str):
    """Create GeoJSON output file from list of stops."""
    features = [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [stop.lon, stop.lat]
            },
            "properties": {
                "mmsi": stop.mmsi,
                "timestamp": stop.timestamp,
                "datetime": datetime.utcfromtimestamp(stop.timestamp).isoformat()
            }
        }
        for stop in tqdm(stops, desc="Creating GeoJSON features")
    ]

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"Writing output to {output_path}...")
    with open(output_path, 'w') as f:
        json.dump(geojson, f, indent=2)


def main(input_path: str, output_path: str):
    """Main function to process vessel data and identify stops."""
    print(f"Processing input file: {input_path}")
    print(f"Output will be written to: {output_path}")

    positions = process_input_file(input_path)
    stops = find_stops(positions)
    create_geojson(stops, output_path)

    print(f"Processing complete. Found {len(stops)} stops.")


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 3:
        print("Usage: python vessel_tracker.py <input_file> <output_file>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])