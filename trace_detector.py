from pathlib import Path

TRACE_TYPES = {
    ".blf",
    ".asc",
    ".pcap",
    ".pcapng",
    ".mf4",
}


def find_trace_files(folder: Path):
    traces = []

    for file in folder.rglob("*"):
        if (
            file.is_file()
            and file.suffix.lower() in TRACE_TYPES
        ):
            traces.append(file)

    return traces