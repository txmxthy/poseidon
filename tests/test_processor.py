import pytest
import json
import tempfile
import gzip
from pathlib import Path
from vessel_tracker.core.processor import MessageProcessor
from vessel_tracker.utils.parsing import parse_position_message


def create_test_file(messages: list[dict], compress: bool = False) -> Path:
    """Helper to create a test file with messages."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.gz' if compress else '') as f:
        if compress:
            with gzip.GzipFile(fileobj=f, mode='wb') as gz:
                for msg in messages:
                    gz.write(f"{json.dumps(msg)}\n".encode())
        else:
            for msg in messages:
                f.write(f"{json.dumps(msg)}\n".encode())
        return Path(f.name)


def test_process_messages(sample_message):
    """Test processing of valid messages."""
    # Create a temporary file with test messages
    test_file = create_test_file([
        sample_message,
        {**sample_message, "Message": {**sample_message["Message"], "MessageID": 4}},  # Invalid type
        {**sample_message, "Message": {**sample_message["Message"], "Latitude": "invalid"}},  # Invalid data
    ])

    try:
        processor = MessageProcessor(str(test_file))
        positions = list(processor.process_messages())

        assert len(positions) == 1
        assert positions[0].mmsi == "123456789"
        assert positions[0].lat == 51.5074
        assert positions[0].lon == -0.1278
    finally:
        test_file.unlink()


def test_process_messages_compressed(sample_message):
    """Test processing of compressed files."""
    test_file = create_test_file([sample_message], compress=True)

    try:
        processor = MessageProcessor(str(test_file))
        positions = list(processor.process_messages())

        assert len(positions) == 1
        assert positions[0].mmsi == "123456789"
    finally:
        test_file.unlink()


def test_process_invalid_file():
    """Test handling of non-existent file."""
    with pytest.raises(FileNotFoundError):
        processor = MessageProcessor("/nonexistent/file.json")
        list(processor.process_messages())
