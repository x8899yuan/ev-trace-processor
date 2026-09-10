from pathlib import Path

from config import ProcessorConfig
from exceptions import ArchiveMergeError
from models import ArchiveVolume


class ArchiveMerger:
    """Merge numbered archive volumes in binary mode."""

    def __init__(self, config: ProcessorConfig) -> None:
        self.config = config

    def merge(
        self,
        volumes: list[ArchiveVolume],
        output_file: Path,
    ) -> Path:
        """Merge volumes and verify the exact byte count."""

        if not volumes:
            raise ArchiveMergeError("No archive volumes were provided.")

        output_file.parent.mkdir(parents=True, exist_ok=True)

        if output_file.exists():
            if not self.config.overwrite:
                raise ArchiveMergeError(
                    f"Output archive already exists:\n{output_file}"
                )
            output_file.unlink()

        expected_size = sum(volume.size_bytes for volume in volumes)
        bytes_written = 0

        try:
            with output_file.open("wb") as output_stream:
                for volume in volumes:
                    print(f"Adding {volume.path.name}")

                    with volume.path.open("rb") as input_stream:
                        while True:
                            data = input_stream.read(self.config.buffer_size)
                            if not data:
                                break
                            output_stream.write(data)
                            bytes_written += len(data)
        except OSError as error:
            if output_file.exists():
                output_file.unlink()
            raise ArchiveMergeError(f"Merge failed: {error}") from error

        if bytes_written != expected_size:
            raise ArchiveMergeError(
                "Merged size does not match the chunk total.\n"
                f"Expected: {expected_size:,} bytes\n"
                f"Created:  {bytes_written:,} bytes"
            )

        print("\nMerge completed.")
        print(f"Merged size: {bytes_written:,} bytes")
        return output_file
