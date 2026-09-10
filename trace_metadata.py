from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class CanIdStatistics:
    """Message-count statistics for a single CAN arbitration ID."""

    arbitration_id: int
    message_count: int
    is_extended_id: bool

    @property
    def arbitration_id_hex(self) -> str:
        """Return the arbitration ID in hexadecimal format."""

        if self.is_extended_id:
            return f"0x{self.arbitration_id:08X}"

        return f"0x{self.arbitration_id:03X}"


@dataclass
class TraceMetadata:
    """Summary information collected from a vehicle trace file."""

    file_path: Path
    file_type: str
    file_size_bytes: int

    total_messages: int = 0

    start_timestamp: float | None = None
    end_timestamp: float | None = None

    classic_can_messages: int = 0
    can_fd_messages: int = 0

    standard_id_messages: int = 0
    extended_id_messages: int = 0

    error_frames: int = 0
    remote_frames: int = 0

    channels: set[int | str] = field(default_factory=set)
    messages_by_channel: dict[int | str, int] = field(default_factory=dict)

    can_id_counts: dict[int, int] = field(default_factory=dict)
    extended_can_ids: set[int] = field(default_factory=set)

    @property
    def file_name(self) -> str:
        """Return the trace file name."""

        return self.file_path.name

    @property
    def duration_seconds(self) -> float:
        """Return the trace duration in seconds."""

        if self.start_timestamp is None or self.end_timestamp is None:
            return 0.0

        return max(0.0, self.end_timestamp - self.start_timestamp)

    @property
    def start_datetime(self) -> datetime | None:
        """Convert the starting Unix timestamp to local date and time."""

        if self.start_timestamp is None:
            return None

        return datetime.fromtimestamp(self.start_timestamp)

    @property
    def end_datetime(self) -> datetime | None:
        """Convert the ending Unix timestamp to local date and time."""

        if self.end_timestamp is None:
            return None

        return datetime.fromtimestamp(self.end_timestamp)

    def update_timestamps(self, timestamp: float) -> None:
        """Update the trace start and end timestamps."""

        if self.start_timestamp is None or timestamp < self.start_timestamp:
            self.start_timestamp = timestamp

        if self.end_timestamp is None or timestamp > self.end_timestamp:
            self.end_timestamp = timestamp

    def add_channel_message(self, channel: int | str | None) -> None:
        """Record one message for a CAN channel."""

        normalized_channel: int | str
        normalized_channel = "Unknown" if channel is None else channel

        self.channels.add(normalized_channel)
        self.messages_by_channel[normalized_channel] = (
            self.messages_by_channel.get(normalized_channel, 0) + 1
        )

    def add_can_id(
        self,
        arbitration_id: int,
        is_extended_id: bool,
    ) -> None:
        """Record one occurrence of a CAN arbitration ID."""

        self.can_id_counts[arbitration_id] = (
            self.can_id_counts.get(arbitration_id, 0) + 1
        )

        if is_extended_id:
            self.extended_can_ids.add(arbitration_id)

    def get_top_can_ids(self, limit: int = 20) -> list[CanIdStatistics]:
        """Return the most frequently occurring CAN IDs."""

        if limit < 1:
            return []

        sorted_can_ids = sorted(
            self.can_id_counts.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        return [
            CanIdStatistics(
                arbitration_id=arbitration_id,
                message_count=message_count,
                is_extended_id=arbitration_id in self.extended_can_ids,
            )
            for arbitration_id, message_count in sorted_can_ids[:limit]
        ]
