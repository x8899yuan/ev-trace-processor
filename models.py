from dataclasses import dataclass
from pathlib import Path


@dataclass
class ArchiveVolume:
    path: Path
    volume_number: int
    size_bytes: int


@dataclass
class ProcessingResult:
    merged_archive: Path
    final_trace_files: list[Path]