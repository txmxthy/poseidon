from dataclasses import dataclass
from datetime import datetime

@dataclass
class Position:
    """Represents a vessel's position at a specific time."""
    lat: float
    lon: float
    timestamp: int
    mmsi: str

    @property
    def datetime(self) -> datetime:
        """Convert timestamp to datetime object."""
        return datetime.utcfromtimestamp(self.timestamp)

    def to_dict(self) -> dict:
        """Convert position to dictionary format."""
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [self.lon, self.lat]
            },
            "properties": {
                "mmsi": self.mmsi,
                "timestamp": self.timestamp,
                "datetime": self.datetime.isoformat()
            }
        }