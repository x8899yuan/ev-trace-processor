from datetime import datetime

from trace_metadata import TraceMetadata


class TraceReporter:
    """Format and display vehicle trace metadata in the console."""

    def __init__(self, top_can_id_limit: int = 20) -> None:
        if top_can_id_limit < 1:
            raise ValueError("top_can_id_limit must be at least 1.")

        self.top_can_id_limit = top_can_id_limit

    def print_report(self, metadata: TraceMetadata) -> None:
        """Print a complete metadata report for one trace file."""

        print()
        print("=" * 78)
        print("VEHICLE TRACE METADATA REPORT")
        print("=" * 78)

        self._print_file_summary(metadata)
        self._print_message_summary(metadata)
        self._print_channel_summary(metadata)
        self._print_top_can_ids(metadata)

        print("=" * 78)

    def _print_file_summary(self, metadata: TraceMetadata) -> None:
        """Print file identity, size, and timing information."""

        print("\nFile summary")
        print("-" * 78)
        print(f"File name:       {metadata.file_name}")
        print(f"File path:       {metadata.file_path}")
        print(f"File type:       {metadata.file_type}")
        print(
            "File size:       "
            f"{metadata.file_size_bytes:,} bytes "
            f"({self._format_bytes(metadata.file_size_bytes)})"
        )
        print(
            "Start time:      "
            f"{self._format_datetime(metadata.start_datetime)}"
        )
        print(
            "End time:        "
            f"{self._format_datetime(metadata.end_datetime)}"
        )
        print(
            "Duration:        "
            f"{self._format_duration(metadata.duration_seconds)}"
        )

    @staticmethod
    def _print_message_summary(metadata: TraceMetadata) -> None:
        """Print message and frame-type counters."""

        print("\nMessage summary")
        print("-" * 78)
        print(f"Total messages:  {metadata.total_messages:,}")
        print(f"Classic CAN:     {metadata.classic_can_messages:,}")
        print(f"CAN FD:          {metadata.can_fd_messages:,}")
        print(f"Standard IDs:    {metadata.standard_id_messages:,}")
        print(f"Extended IDs:    {metadata.extended_id_messages:,}")
        print(f"Error frames:    {metadata.error_frames:,}")
        print(f"Remote frames:   {metadata.remote_frames:,}")
        print(f"Unique CAN IDs:  {len(metadata.can_id_counts):,}")
        print(f"Channels found:  {len(metadata.channels):,}")

    @staticmethod
    def _print_channel_summary(metadata: TraceMetadata) -> None:
        """Print message totals for every detected channel."""

        print("\nMessages by channel")
        print("-" * 78)

        if not metadata.messages_by_channel:
            print("No channel information was found.")
            return

        sorted_channels = sorted(
            metadata.messages_by_channel.items(),
            key=lambda item: str(item[0]).lower(),
        )

        print(f"{'Channel':<22}{'Messages':>18}{'Percentage':>18}")
        print(f"{'-' * 22}{'-' * 18}{'-' * 18}")

        for channel, message_count in sorted_channels:
            percentage = TraceReporter._calculate_percentage(
                message_count,
                metadata.total_messages,
            )
            print(
                f"{str(channel):<22}"
                f"{message_count:>18,}"
                f"{percentage:>17.2f}%"
            )

    def _print_top_can_ids(self, metadata: TraceMetadata) -> None:
        """Print the most frequently occurring arbitration IDs."""

        print(f"\nTop {self.top_can_id_limit} CAN IDs")
        print("-" * 78)

        top_can_ids = metadata.get_top_can_ids(
            limit=self.top_can_id_limit
        )

        if not top_can_ids:
            print("No CAN IDs were found.")
            return

        print(
            f"{'Rank':<8}"
            f"{'CAN ID':<18}"
            f"{'Format':<14}"
            f"{'Messages':>18}"
            f"{'Percentage':>18}"
        )
        print(
            f"{'-' * 8}"
            f"{'-' * 18}"
            f"{'-' * 14}"
            f"{'-' * 18}"
            f"{'-' * 18}"
        )

        for rank, can_id in enumerate(top_can_ids, start=1):
            id_format = "Extended" if can_id.is_extended_id else "Standard"
            percentage = self._calculate_percentage(
                can_id.message_count,
                metadata.total_messages,
            )

            print(
                f"{rank:<8}"
                f"{can_id.arbitration_id_hex:<18}"
                f"{id_format:<14}"
                f"{can_id.message_count:>18,}"
                f"{percentage:>17.2f}%"
            )

    @staticmethod
    def _calculate_percentage(part: int, total: int) -> float:
        """Return part as a percentage of total without dividing by zero."""

        if total <= 0:
            return 0.0

        return part / total * 100.0

    @staticmethod
    def _format_datetime(value: datetime | None) -> str:
        """Format a datetime for the console report."""

        if value is None:
            return "Not available"

        return value.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    @staticmethod
    def _format_duration(duration_seconds: float) -> str:
        """Format a duration as days, hours, minutes, and seconds."""

        duration_seconds = max(0.0, duration_seconds)
        total_seconds = int(duration_seconds)
        milliseconds = int(round((duration_seconds - total_seconds) * 1000))

        if milliseconds == 1000:
            total_seconds += 1
            milliseconds = 0

        days, remaining_seconds = divmod(total_seconds, 86_400)
        hours, remaining_seconds = divmod(remaining_seconds, 3_600)
        minutes, seconds = divmod(remaining_seconds, 60)

        components: list[str] = []

        if days:
            components.append(f"{days}d")

        if days or hours:
            components.append(f"{hours:02d}h")

        if days or hours or minutes:
            components.append(f"{minutes:02d}m")

        components.append(f"{seconds:02d}.{milliseconds:03d}s")
        return " ".join(components)

    @staticmethod
    def _format_bytes(size_bytes: int) -> str:
        """Convert a byte count into a human-readable binary size."""

        size = float(size_bytes)

        for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
            if size < 1024.0 or unit == "TiB":
                return f"{size:,.2f} {unit}"

            size /= 1024.0

        return f"{size_bytes:,} B"
