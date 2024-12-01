import json
from typing import Generator, List
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
import multiprocessing as mp
from functools import partial
import itertools

from ..models.position import Position
from ..utils.file import open_file, count_lines
from ..utils.parsing import parse_position_message
from ..utils.progress import MESSAGE_PROCESSOR
from ..utils.profiling import profiler


class MessageProcessor:
    """Processes AIS messages from input file with parallel processing support."""

    def __init__(self, input_path: str, chunk_size: int = 100000, max_workers: int = None):
        self.input_path = input_path
        self.chunk_size = chunk_size
        self.max_workers = max_workers or mp.cpu_count()
        self._total_messages = None

    @property
    def total_messages(self) -> int:
        """Lazy loading of total message count."""
        if self._total_messages is None:
            with profiler.profile_section("counting_messages"):
                self._total_messages = count_lines(self.input_path)
        return self._total_messages

    def _process_chunk(self, chunk: List[str]) -> List[Position]:
        """Process a chunk of messages and return valid positions."""
        positions = []
        for line in chunk:
            try:
                message = json.loads(line)
                position = parse_position_message(message)
                if position:
                    positions.append(position)
            except json.JSONDecodeError:
                continue
        return positions

    @profiler.profile_function()
    def process_messages(self) -> Generator[Position, None, None]:
        """Process input file in parallel and yield valid position reports."""
        chunk = []

        with profiler.profile_section("parallel_processing"):
            with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                futures = []

                # Submit chunks for parallel processing
                with open_file(self.input_path) as f:
                    for i, line in enumerate(f):
                        chunk.append(line)

                        if len(chunk) >= self.chunk_size:
                            futures.append(
                                executor.submit(self._process_chunk, chunk.copy())
                            )
                            chunk = []

                # Process final chunk if any
                if chunk:
                    futures.append(
                        executor.submit(self._process_chunk, chunk)
                    )

                # Process results as they complete
                with tqdm(total=len(futures), **MESSAGE_PROCESSOR) as pbar:
                    for future in as_completed(futures):
                        try:
                            positions = future.result()
                            for position in positions:
                                yield position
                            pbar.update(1)
                        except Exception as e:
                            print(f"Error processing chunk: {e}")
                            continue
