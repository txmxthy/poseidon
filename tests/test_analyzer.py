import pytest
from vessel_tracker.core.analyzer import VesselAnalyzer


def test_find_stops(sample_positions):
    """Test stop detection with sample positions."""
    analyzer = VesselAnalyzer(min_duration=3600)
    analyzer.vessel_data = {"123456789": sample_positions}

    stops = analyzer.find_stops()

    assert len(stops) == 1
    assert stops[0].mmsi == "123456789"
    assert stops[0].timestamp == sample_positions[0].timestamp


def test_find_stops_multiple_vessels(sample_positions):
    """Test stop detection with multiple vessels."""
    # Create a second vessel's positions by offsetting the first
    vessel2_positions = [
        p.__class__(lat=p.lat + 1, lon=p.lon + 1, timestamp=p.timestamp, mmsi="987654321")
        for p in sample_positions
    ]

    analyzer = VesselAnalyzer(min_duration=3600)
    analyzer.vessel_data = {
        "123456789": sample_positions,
        "987654321": vessel2_positions
    }

    stops = analyzer.find_stops()

    assert len(stops) == 2
    assert {stop.mmsi for stop in stops} == {"123456789", "987654321"}


def test_find_stops_no_stops():
    """Test when no stops are found."""
    analyzer = VesselAnalyzer()
    analyzer.vessel_data = {}

    stops = analyzer.find_stops()

    assert len(stops) == 0


def test_find_stops_short_duration(sample_positions):
    """Test with minimum duration longer than actual stops."""
    analyzer = VesselAnalyzer(min_duration=7200)  # 2 hours
    analyzer.vessel_data = {"123456789": sample_positions}

    stops = analyzer.find_stops()

    assert len(stops) == 0