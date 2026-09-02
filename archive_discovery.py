import re

from pathlib import Path
from models import ArchiveVolume


VOLUME_PATTERN = re.compile(
    r"^(?P<base>.+\.7z)\.(?P<number>\d{3})$"
)


def discover_volumes(folder: Path):

    volumes = []

    for path in folder.glob("*.7z.*"):

        match = VOLUME_PATTERN.match(path.name)

        if not match:
            continue

        volumes.append(
            ArchiveVolume(
                path=path,
                volume_number=int(match.group("number")),
                size_bytes=path.stat().st_size
            )
        )

    volumes.sort(
        key=lambda x: x.volume_number
    )

    return volumes
