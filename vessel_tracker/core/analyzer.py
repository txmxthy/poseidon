from typing import Dict, List, Generator
from tqdm import tqdm

from ..models.position import Position
from ..utils.geo import calculate_speed
from ..utils.progress import VESSEL_ANALYZER

class VesselAnalyzer:
    """Analyzes vessel positions to identify stops."""

    def __init__(self, min_duration: int = 3600):
        self.min_duration = min_duration
        self.vessel_data: Dict[str, List[Position]] = {}

    def group_positions(self, positions: Generator[Position, None, None]) -> None:
        """Group positions by vessel MMSI."""
        print("\nGrouping positions by vessel...")
        for pos in positions:
            if pos.mmsi not in self.vessel_data:
                self.vessel_data[pos.mmsi] = []
            self.vessel_data[pos.mmsi].append(pos)

    def _analyze_vessel_positions(self, positions: List[Position]) -> List[Position]:
        """Analyze positions for a single vessel to find stops."""
        positions.sort(key=lambda x: x.timestamp)
        stops = []
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
                if pos.timestamp - stop_start.timestamp >= self.min_duration:
                    stops.append(stop_start)
                stop_start = None

            prev_pos = pos

        # Check final stop
        if stop_start is not None and \
                positions[-1].timestamp - stop_start.timestamp >= self.min_duration:
            stops.append(stop_start)

        return stops

    def find_stops(self) -> List[Position]:
        """Find vessel stops across all vessels."""
        if not self.vessel_data:
            return []

        stops = []
        vessel_count = len(self.vessel_data)
        print(f"\nProcessing {vessel_count:,} vessels...")

        with tqdm(self.vessel_data.items(), total=vessel_count, **VESSEL_ANALYZER) as pbar:
            for mmsi, positions in pbar:
                vessel_stops = self._analyze_vessel_positions(positions)
                stops.extend(vessel_stops)

        return stops