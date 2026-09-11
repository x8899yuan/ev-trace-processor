from collections import Counter
from pathlib import Path


class TraceAnalyzer:
    """Analyze trace message collections and generate summary metrics."""

    def analyze(self, messages, trace_file):
        file_path = Path(trace_file)

        message_count = len(messages)
        file_size_mb = (
            round(file_path.stat().st_size / (1024 * 1024), 2)
            if file_path.exists()
            else 0
        )

        if not messages:
            return {
                "file_name": file_path.name,
                "file_size_mb": file_size_mb,
                "message_count": 0,
                "unique_ids": 0,
                "first_timestamp": 0,
                "last_timestamp": 0,
                "duration_sec": 0,
                "standard_frames": 0,
                "extended_frames": 0,
                "avg_msg_rate": 0,
                "channel_count": 0,
                "channels": [],
                "top_ids": {},
            }

        timestamps = []
        arbitration_ids = []
        channels = set()
        standard_frames = 0
        extended_frames = 0

        for msg in messages:
            timestamps.append(float(getattr(msg, "timestamp", 0)))

            arb_id = int(getattr(msg, "arbitration_id", 0))
            arbitration_ids.append(arb_id)

            if getattr(msg, "is_extended_id", False):
                extended_frames += 1
            else:
                standard_frames += 1

            if hasattr(msg, "channel"):
                channels.add(getattr(msg, "channel"))

        first_timestamp = min(timestamps)
        last_timestamp = max(timestamps)
        duration_sec = max(last_timestamp - first_timestamp, 0)

        avg_msg_rate = (
            round(message_count / duration_sec, 2)
            if duration_sec > 0
            else 0
        )

        top_ids = dict(Counter(arbitration_ids).most_common(20))

        return {
            "file_name": file_path.name,
            "file_size_mb": file_size_mb,
            "message_count": message_count,
            "unique_ids": len(set(arbitration_ids)),
            "first_timestamp": round(first_timestamp, 6),
            "last_timestamp": round(last_timestamp, 6),
            "duration_sec": round(duration_sec, 3),
            "standard_frames": standard_frames,
            "extended_frames": extended_frames,
            "avg_msg_rate": avg_msg_rate,
            "channel_count": len(channels),
            "channels": sorted(list(channels)),
            "top_ids": {
                f"0x{can_id:X}": count
                for can_id, count in top_ids.items()
            },
        }
