from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProcessorConfig:
    input_folder: Path
    output_folder: Path
    seven_zip_path: Path