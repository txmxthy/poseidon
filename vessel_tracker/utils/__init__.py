"""Utility functions for vessel tracking."""
from vessel_tracker.utils.geo import haversine_distance, calculate_speed
from vessel_tracker.utils.file import open_file, count_lines, ensure_output_dir
from vessel_tracker.utils.parsing import parse_position_message
from vessel_tracker.utils.progress import (
    get_progress_bar_settings,
    MESSAGE_COUNTER,
    MESSAGE_PROCESSOR,
    VESSEL_ANALYZER,
    GEOJSON_CREATOR
)

__all__ = [
    'haversine_distance',
    'calculate_speed',
    'open_file',
    'count_lines',
    'ensure_output_dir',
    'parse_position_message',
    'get_progress_bar_settings',
    'MESSAGE_COUNTER',
    'MESSAGE_PROCESSOR',
    'VESSEL_ANALYZER',
    'GEOJSON_CREATOR'
]