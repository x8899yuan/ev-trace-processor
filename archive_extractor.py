import subprocess

from pathlib import Path


class ArchiveExtractor:

    @staticmethod
    def extract(
        archive,
        destination,
        seven_zip
    ):

        destination.mkdir(
            exist_ok=True
        )

        subprocess.run(
            [
                seven_zip,
                "x",
                str(archive),
                f"-o{destination}",
                "-y"
            ],
            check=True
        )