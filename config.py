from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProcessorConfig:
    """Application configuration."""

    input_folder: Path
    output_folder: Path
    seven_zip_path: Path
    overwrite: bool = True
    buffer_size: int = 8 * 1024 * 1024


def load_config() -> ProcessorConfig:
    """Load the local configuration.

    Update input_folder when processing a different KPM package.
    """

    input_folder = Path(
        r"C:\Temp\PnC Testing Traces\test"
    )

    return ProcessorConfig(
        input_folder=input_folder,
        output_folder=input_folder / "Processed",
        seven_zip_path=Path(r"C:\Program Files\7-Zip\7z.exe"),
        overwrite=True,
    )
