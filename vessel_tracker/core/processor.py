import json
from typing import Generator
from tqdm import tqdm

from ..models.position import Position
from ..utils.file import open_file, count_lines
from ..utils.parsing import parse_position_message
from ..utils.progress import MESSAGE_PROCESSOR


class MessageProcessor:
    """Processes AIS messages from input file."""

    def __init__(self, input_path: str):
        self.input_path = input_path
        self._total_messages = None

    @property
    def total_messages(self) -> int:
        """Lazy loading of total message count."""
        if self._total_messages is None:
            self._total_messages = count_lines(self.input_path)
        return self._total_messages

    def process_messages(self) -> Generator[Position, None, None]:
        """Process input file and yield valid position reports."""
        with open_file(self.input_path) as f:
            for line in tqdm(f, total=self.total_messages, **MESSAGE_PROCESSOR):
                try:
                    message = json.loads(line)
                    position = parse_position_message(message)
                    if position:
                        yield position
                except json.JSONDecodeError:
                    continue