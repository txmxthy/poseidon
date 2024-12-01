from typing import Dict, List, Generator
from tqdm import tqdm
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

from ..models.position import Position
from ..utils.geo import calculate_speed
from ..utils.progress import VESSEL_ANALYZER


def analyze_vessel_positions(data: tuple) -> List[Position]:
    """Analyze positions for a single vessel to find stops."""
    mmsi, positions = data
    positions.sort(key=lambda x: x.timestamp)
    stops = []
    stop_start = None
    prev_pos = None

    # Pre-calculate all speeds for this vessel's positions
    for pos in positions:
        if prev_pos is None:
            prev_pos = pos
            continue

        speed = calculate_speed(prev_pos, pos)

        if speed < 1.0:  # Less than 1 knot
            if stop_start is None:
                stop_start = prev_pos
        elif stop_start is not None:
            if pos.timestamp - stop_start.timestamp >= 3600:  # 1 hour
                stops.append(stop_start)
            stop_start = None

        prev_pos = pos

    # Check final stop
    if stop_start is not None and \
            positions[-1].timestamp - stop_start.timestamp >= 3600:
        stops.append(stop_start)

    return stops


class VesselAnalyzer:
    """Analyzes vessel positions to identify stops."""

    def __init__(self, min_duration: int = 3600, max_workers: int = None):
        self.min_duration = min_duration
        self.max_workers = max_workers or mp.cpu_count()
        self.vessel_data: Dict[str, List[Position]] = {}

    def group_positions(self, positions: Generator[Position, None, None]) -> None:
        """Group positions by vessel MMSI using dictionary comprehension."""
        print("\nGrouping positions by vessel...")
        # Use a temporary dictionary to collect positions
        temp_dict: Dict[str, List[Position]] = {}
        for pos in positions:
            if pos.mmsi not in temp_dict:
                temp_dict[pos.mmsi] = []
            temp_dict[pos.mmsi].append(pos)

        self.vessel_data = temp_dict

    def find_stops(self) -> List[Position]:
        """Find vessel stops across all vessels using parallel processing."""
        if not self.vessel_data:
            return []

        vessel_count = len(self.vessel_data)
        print(f"\nProcessing {vessel_count:,} vessels...")

        all_stops = []
        items = list(self.vessel_data.items())

        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            with tqdm(total=vessel_count, **VESSEL_ANALYZER) as pbar:
                # Process vessels in parallel
                futures = [executor.submit(analyze_vessel_positions, item) for item in items]

                # Collect results as they complete
                for future in futures:
                    stops = future.result()
                    all_stops.extend(stops)
                    pbar.update(1)

        return all_stops