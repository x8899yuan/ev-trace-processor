from pathlib import Path


TRACE_TYPES = {
    ".blf",
    ".asc",
    ".pcap",
    ".pcapng",
    ".mf4",
    ".mdf",
    ".esotrace",
}


class TraceDetector:
    """Locate supported vehicle trace files recursively."""

    @staticmethod
    def find_trace_files(folder: Path) -> list[Path]:
        """Return all recognized trace files under a folder."""

        trace_files = [
            path
            for path in folder.rglob("*")
            if path.is_file() and path.suffix.lower() in TRACE_TYPES
        ]

        return sorted(trace_files, key=lambda path: str(path).lower())
