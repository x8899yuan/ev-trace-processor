import re
from pathlib import Path

from exceptions import VolumeDiscoveryError
from models import ArchiveVolume


VOLUME_PATTERN = re.compile(
    r"^(?P<archive_name>.+\.7z)\.(?P<volume_number>\d{3})$"
)


def discover_archive_volumes(input_folder: Path) -> list[ArchiveVolume]:
    """Find and validate one numbered 7z volume set."""

    if not input_folder.exists():
        raise VolumeDiscoveryError(
            f"Input folder does not exist:\n{input_folder}"
        )

    first_volumes = sorted(input_folder.glob("*.7z.001"))

    if not first_volumes:
        raise VolumeDiscoveryError(
            f"No .7z.001 file was found in:\n{input_folder}"
        )

    if len(first_volumes) > 1:
        names = "\n".join(f"  {path.name}" for path in first_volumes)
        raise VolumeDiscoveryError(
            "Multiple archive sets were found:\n"
            f"{names}\n\n"
            "Place only one archive set in the input folder."
        )

    first_volume = first_volumes[0]
    match = VOLUME_PATTERN.match(first_volume.name)

    if match is None:
        raise VolumeDiscoveryError(
            f"Invalid volume name: {first_volume.name}"
        )

    archive_name = match.group("archive_name")
    volume_paths = input_folder.glob(
        f"{archive_name}.[0-9][0-9][0-9]"
    )

    volumes: list[ArchiveVolume] = []

    for volume_path in volume_paths:
        volume_match = VOLUME_PATTERN.match(volume_path.name)
        if volume_match is None:
            continue

        volumes.append(
            ArchiveVolume(
                path=volume_path,
                volume_number=int(volume_match.group("volume_number")),
                size_bytes=volume_path.stat().st_size,
            )
        )

    volumes.sort(key=lambda volume: volume.volume_number)
    validate_volume_sequence(volumes)
    return volumes


def validate_volume_sequence(volumes: list[ArchiveVolume]) -> None:
    """Require a continuous sequence beginning with volume 001."""

    if not volumes:
        raise VolumeDiscoveryError("No archive volumes were discovered.")

    actual_numbers = [volume.volume_number for volume in volumes]
    expected_numbers = list(range(1, actual_numbers[-1] + 1))

    if actual_numbers != expected_numbers:
        missing_numbers = sorted(
            set(expected_numbers) - set(actual_numbers)
        )
        missing_text = ", ".join(
            f"{number:03d}" for number in missing_numbers
        )
        raise VolumeDiscoveryError(
            "Archive volume sequence is incomplete.\n"
            f"Found volumes: {actual_numbers}\n"
            f"Missing volumes: {missing_text or 'Unknown'}"
        )


def get_merged_archive_name(first_volume: ArchiveVolume) -> str:
    """Return the archive name without the numbered suffix."""

    match = VOLUME_PATTERN.match(first_volume.path.name)
    if match is None:
        raise VolumeDiscoveryError(
            "Unable to determine the merged archive name from: "
            f"{first_volume.path.name}"
        )

    return match.group("archive_name")
