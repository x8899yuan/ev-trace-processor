from abc import ABC, abstractmethod
from typing import Iterable, Any


class BaseReader(ABC):
    """Base interface for all trace readers.

    Every reader converts its native file format into a common
    internal representation that can later be consumed by
    analyzers, decoders, and exporters.
    """

    @abstractmethod
    def read(self, file_path: str) -> Iterable[Any]:
        """Read a trace file and yield frames/messages."""
        raise NotImplementedError
