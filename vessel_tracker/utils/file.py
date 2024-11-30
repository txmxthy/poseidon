import gzip
from typing import TextIO
import os
from tqdm import tqdm
from .progress import MESSAGE_COUNTER

def open_file(filepath: str) -> TextIO:
    """Open file handling both .gz and regular files."""
    if filepath.endswith('.gz'):
        return gzip.open(filepath, 'rt')
    return open(filepath, 'r')

def count_lines(filepath: str) -> int:
    """Count number of lines in a file, handling both .gz and regular files."""
    count = 0
    with open_file(filepath) as f:
        for _ in tqdm(f, **MESSAGE_COUNTER):
            count += 1
    return count

def ensure_output_dir(filepath: str) -> None:
    """Ensure the output directory exists."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)