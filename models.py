from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ArchiveVolume:
    """One numbered split-archive volume."""

    path: Path
    volume_number: int
    size_bytes: int


@dataclass(frozen=True)
class ProcessingResult:
    """Final output from processing one KPM trace package."""

    merged_archive: Path
    extraction_folder: Path
    final_trace_files: list[Path]
