from typing import Dict, Union
from ..models.position import Position

POSITION_MESSAGE_TYPES = {1, 2, 3, 18, 19, 27}

def parse_position_message(message: Dict) -> Union[Position, None]:
    """Parse AIS message and return Position if it's a position report."""
    msg_data = message.get('Message', {})
    msg_id = msg_data.get('MessageID')

    if msg_id not in POSITION_MESSAGE_TYPES:
        return None

    try:
        return Position(
            lat=float(msg_data['Latitude']),
            lon=float(msg_data['Longitude']),
            timestamp=int(message['UTCTimeStamp']),
            mmsi=str(msg_data['UserID'])
        )
    except (KeyError, ValueError):
        return None