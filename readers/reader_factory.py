from pathlib import Path

from readers.blf_reader import BlfReader
from readers.base_reader import BaseReader


class UnsupportedTraceFormatError(Exception):
    """Raised when no reader exists for a trace format."""


READERS = {
    ".blf": BlfReader,
}


def create_reader(file_path: str) -> BaseReader:
    """Return the appropriate reader for a trace file."""

    suffix = Path(file_path).suffix.lower()

    reader_class = READERS.get(suffix)
    if reader_class is None:
        supported = ", ".join(sorted(READERS.keys()))
        raise UnsupportedTraceFormatError(
            f"Unsupported trace format: {suffix}. Supported formats: {supported}"
        )

    return reader_class()
