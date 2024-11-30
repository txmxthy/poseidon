from vessel_tracker.utils.geo import haversine_distance, calculate_speed
from vessel_tracker.models.position import Position


def test_haversine_distance():
    """Test distance calculation between London and Paris."""
    # London
    lat1, lon1 = 51.5074, -0.1278
    # Paris
    lat2, lon2 = 48.8566, 2.3522

    distance = haversine_distance(lat1, lon1, lat2, lon2)

    # Distance should be approximately 344 km
    assert 343_000 < distance < 345_000


def test_calculate_speed(sample_positions):
    """Test speed calculation between two close positions."""
    pos1, pos2 = sample_positions[0], sample_positions[-1]

    speed = calculate_speed(pos1, pos2)

    # Speed should be very low (positions are close)
    assert speed < 1.0


def test_calculate_speed_zero_time_difference(sample_position):
    """Test speed calculation with same timestamp."""
    pos1 = sample_position
    pos2 = Position(
        lat=pos1.lat + 0.1,
        lon=pos1.lon + 0.1,
        timestamp=pos1.timestamp,  # Same timestamp
        mmsi=pos1.mmsi
    )

    speed = calculate_speed(pos1, pos2)

    assert speed == 0