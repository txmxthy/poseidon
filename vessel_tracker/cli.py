#!/usr/bin/env python
import sys
import argparse
import os
from typing import List, Optional
from pathlib import Path

from vessel_tracker.core import process_vessel_data


def resolve_path(path: str) -> str:
    """Convert relative path to absolute path from current working directory."""
    return str(Path(os.getcwd()) / path)


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Process vessel AIS data to identify stops.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "input_file",
        help="Path to input file (JSON or JSON.gz)",
    )

    parser.add_argument(
        "output_file",
        help="Path for output GeoJSON file",
    )

    parser.add_argument(
        "--min-duration",
        type=int,
        default=3600,
        help="Minimum stop duration in seconds",
    )

    parsed_args = parser.parse_args(args)

    # Resolve relative paths
    parsed_args.input_file = resolve_path(parsed_args.input_file)
    parsed_args.output_file = resolve_path(parsed_args.output_file)

    return parsed_args


def main() -> int:
    """Main entry point for the vessel tracker."""
    try:
        args = parse_args()
        process_vessel_data(
            input_path=args.input_file,
            output_path=args.output_file,
            min_stop_duration=args.min_duration
        )
        return 0
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())