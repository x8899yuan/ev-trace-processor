from datetime import timedelta
from typing import Dict, Any

import can

from readers.base_reader import BaseReader


class BlfReader(BaseReader):
    """Read BLF trace files using python-can."""

    def read(self, file_path: str):
        with can.BLFReader(file_path) as reader:
            for message in reader:
                yield message

    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """Collect high-level statistics from a BLF file."""

        message_count = 0
        unique_ids = set()
        channels = set()
        first_ts = None
        last_ts = None

        with can.BLFReader(file_path) as reader:
            for msg in reader:
                message_count += 1
                unique_ids.add(msg.arbitration_id)

                if hasattr(msg, 'channel'):
                    channels.add(msg.channel)

                if first_ts is None:
                    first_ts = msg.timestamp

                last_ts = msg.timestamp

        duration_seconds = 0.0
        if first_ts is not None and last_ts is not None:
            duration_seconds = max(0.0, last_ts - first_ts)

        return {
            'file_path': file_path,
            'message_count': message_count,
            'unique_id_count': len(unique_ids),
            'channel_count': len(channels),
            'channels': sorted(channels),
            'duration_seconds': round(duration_seconds, 3),
            'duration_text': str(timedelta(seconds=int(duration_seconds))),
        }
