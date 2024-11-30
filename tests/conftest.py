import pytest
from datetime import datetime, timezone
from vessel_tracker.models.position import Position

@pytest.fixture
def sample_position() -> Position:
    """Create a sample position."""
    return Position(
        lat=51.5074,
        lon=-0.1278,
        timestamp=int(datetime(2024, 1, 1, tzinfo=timezone.utc).timestamp()),
        mmsi="123456789"
    )

@pytest.fixture
def sample_positions() -> list[Position]:
    """Create a sequence of positions simulating a vessel stopping."""
    base_time = int(datetime(2024, 1, 1, tzinfo=timezone.utc).timestamp())
    return [
        Position(lat=51.5074, lon=-0.1278, timestamp=base_time, mmsi="123456789"),
        Position(lat=51.5074, lon=-0.1278, timestamp=base_time + 1800, mmsi="123456789"),
        Position(lat=51.5074, lon=-0.1278, timestamp=base_time + 3600, mmsi="123456789"),
        Position(lat=51.5075, lon=-0.1279, timestamp=base_time + 5400, mmsi="123456789"),
    ]

@pytest.fixture
def sample_message() -> dict:
    """Create a sample AIS message."""
    return {
        "Message": {
            "MessageID": 1,
            "UserID": "123456789",
            "Latitude": 51.5074,
            "Longitude": -0.1278
        },
        "UTCTimeStamp": 1704067200
    }