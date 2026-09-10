from pathlib import Path
from typing import Iterator

import can

from trace_metadata import TraceMetadata


class TraceReaderError(Exception):
    """Raised when a vehicle trace file cannot be read or analyzed."""


class TraceReader:
    """Stream CAN messages from a supported trace file and collect metadata."""

    SUPPORTED_FILE_TYPES = {
        ".blf": "BLF",
        ".asc": "ASC",
        ".mf4": "MF4",
    }

    def analyze(self, trace_file: Path) -> TraceMetadata:
        """Analyze a trace file without loading all messages into memory."""

        trace_file = trace_file.resolve()
        self._validate_trace_file(trace_file)

        metadata = TraceMetadata(
            file_path=trace_file,
            file_type=self.SUPPORTED_FILE_TYPES[trace_file.suffix.lower()],
            file_size_bytes=trace_file.stat().st_size,
        )

        try:
            for message in self._open_reader(trace_file):
                self._update_metadata(metadata, message)
        except Exception as error:
            raise TraceReaderError(
                f"Unable to analyze trace file:\n{trace_file}\n\n{error}"
            ) from error

        return metadata

    def _open_reader(self, trace_file: Path) -> Iterator[can.Message]:
        """Create the appropriate python-can reader for the file type."""

        suffix = trace_file.suffix.lower()

        if suffix == ".blf":
            return iter(can.BLFReader(trace_file))

        if suffix == ".asc":
            return iter(can.ASCReader(trace_file))

        if suffix == ".mf4":
            try:
                return iter(can.MF4Reader(trace_file))
            except NotImplementedError as error:
                raise TraceReaderError(
                    "MF4 support requires the optional python-can MF4 "
                    "dependencies. Install them with:\n"
                    "python -m pip install python-can[mf4]"
                ) from error

        raise TraceReaderError(
            f"Unsupported trace-file type: {suffix or 'no extension'}"
        )

    def _validate_trace_file(self, trace_file: Path) -> None:
        """Validate the input path and supported file extension."""

        if not trace_file.exists():
            raise TraceReaderError(
                f"Trace file does not exist:\n{trace_file}"
            )

        if not trace_file.is_file():
            raise TraceReaderError(
                f"Trace path is not a file:\n{trace_file}"
            )

        suffix = trace_file.suffix.lower()

        if suffix not in self.SUPPORTED_FILE_TYPES:
            supported_types = ", ".join(
                sorted(self.SUPPORTED_FILE_TYPES)
            )
            raise TraceReaderError(
                f"Unsupported trace-file type: {suffix or 'no extension'}\n"
                f"Supported types: {supported_types}"
            )

        if trace_file.stat().st_size == 0:
            raise TraceReaderError(
                f"Trace file is empty:\n{trace_file}"
            )

    @staticmethod
    def _update_metadata(
        metadata: TraceMetadata,
        message: can.Message,
    ) -> None:
        """Add one python-can message to the metadata counters."""

        metadata.total_messages += 1
        metadata.update_timestamps(message.timestamp)
        metadata.add_channel_message(message.channel)
        metadata.add_can_id(
            arbitration_id=message.arbitration_id,
            is_extended_id=message.is_extended_id,
        )

        if message.is_fd:
            metadata.can_fd_messages += 1
        else:
            metadata.classic_can_messages += 1

        if message.is_extended_id:
            metadata.extended_id_messages += 1
        else:
            metadata.standard_id_messages += 1

        if message.is_error_frame:
            metadata.error_frames += 1

        if message.is_remote_frame:
            metadata.remote_frames += 1
