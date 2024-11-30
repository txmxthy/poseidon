import pytest
from datetime import datetime, timezone
import json
from vessel_tracker import (
    Position,
    haversine_distance,
    calculate_speed,
    parse_position_message,
    find_stops,
    create_geojson
)


@pytest.fixture
def sample_position():
    return Position(
        lat=51.5074,
        lon=-0.1278,
        timestamp=int(datetime(2024, 1, 1, tzinfo=timezone.utc).timestamp()),
        mmsi="123456789"
    )


@pytest.fixture
def sample_positions():
    # Create a sequence of positions simulating a vessel stopping
    base_time = int(datetime(2024, 1, 1, tzinfo=timezone.utc).timestamp())
    positions = [
        Position(lat=51.5074, lon=-0.1278, timestamp=base_time, mmsi="123456789"),
        Position(lat=51.5074, lon=-0.1278, timestamp=base_time + 1800, mmsi="123456789"),  # 30 mins
        Position(lat=51.5074, lon=-0.1278, timestamp=base_time + 3600, mmsi="123456789"),  # 1 hour
        Position(lat=51.5075, lon=-0.1279, timestamp=base_time + 5400, mmsi="123456789"),  # 1.5 hours
    ]
    return positions


def test_haversine_distance():
    # Test distance between London and Paris
    london = (51.5074, -0.1278)
    paris = (48.8566, 2.3522)
    distance = haversine_distance(london[0], london[1], paris[0], paris[1])

    # Distance should be approximately 344 km
    assert 343000 < distance < 345000


def test_calculate_speed():
    pos1 = Position(lat=51.5074, lon=-0.1278, timestamp=0, mmsi="123456789")
    pos2 = Position(lat=51.5075, lon=-0.1279, timestamp=3600, mmsi="123456789")

    speed = calculate_speed(pos1, pos2)
    # Speed should be very low (positions are close)
    assert speed < 1.0


def test_parse_position_message():
    valid_message = {
        "Message": {
            "MessageID": 1,
            "UserID": "123456789",
            "Latitude": 51.5074,
            "Longitude": -0.1278
        },
        "UTCTimeStamp": 1704067200
    }

    position = parse_position_message(valid_message)
    assert position is not None
    assert position.mmsi == "123456789"
    assert position.lat == 51.5074
    assert position.lon == -0.1278
    assert position.timestamp == 1704067200


def test_parse_invalid_message():
    invalid_message = {
        "Message": {
            "MessageID": 4,  # Not a position report
            "UserID": "123456789"
        },
        "UTCTimeStamp": 1704067200
    }

    position = parse_position_message(invalid_message)
    assert position is None


def test_find_stops(sample_positions):
    stops = find_stops((pos for pos in sample_positions))
    assert len(stops) == 1
    assert stops[0].mmsi == "123456789"


def test_create_geojson(sample_positions, tmp_path):
    output_file = tmp_path / "test_output.geojson"
    create_geojson(sample_positions, str(output_file))

    assert output_file.exists()
    with open(output_file) as f:
        data = json.load(f)

    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) == len(sample_positions)

    feature = data["features"][0]
    assert feature["type"] == "Feature"
    assert feature["geometry"]["type"] == "Point"
    assert len(feature["geometry"]["coordinates"]) == 2
    assert "mmsi" in feature["properties"]
    assert "timestamp" in feature["properties"]
    assert "datetime" in feature["properties"]


def test_empty_positions_list(tmp_path):
    output_file = tmp_path / "empty_output.geojson"
    create_geojson([], str(output_file))

    assert output_file.exists()
    with open(output_file) as f:
        data = json.load(f)

    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) == 0