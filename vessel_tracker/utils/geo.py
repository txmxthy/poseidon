import math
from ..models.position import Position

EARTH_RADIUS = 6371e3  # Earth's radius in meters
KNOTS_CONVERSION = 0.514444  # Conversion factor from m/s to knots


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points using the haversine formula."""
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) * math.sin(delta_phi / 2) + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2) * math.sin(delta_lambda / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS * c


def calculate_speed(pos1: Position, pos2: Position) -> float:
    """Calculate speed in knots between two positions."""
    distance = haversine_distance(pos1.lat, pos1.lon, pos2.lat, pos2.lon)
    time_diff = pos2.timestamp - pos1.timestamp
    if time_diff == 0:
        return 0

    return (distance / time_diff) / KNOTS_CONVERSION