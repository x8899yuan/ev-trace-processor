import subprocess
from pathlib import Path

from exceptions import ArchiveValidationError


class ArchiveValidator:
    """Validate a reconstructed archive with 7-Zip."""

    def __init__(self, seven_zip_path: Path) -> None:
        self.seven_zip_path = seven_zip_path

    def validate_archive(self, archive: Path) -> None:
        """Run the 7-Zip integrity test command."""

        if not self.seven_zip_path.exists():
            raise FileNotFoundError(
                f"7-Zip executable was not found:\n{self.seven_zip_path}"
            )

        print("\nTesting merged archive...")

        result = subprocess.run(
            [str(self.seven_zip_path), "t", str(archive)],
            capture_output=True,
            text=True,
            errors="replace",
            check=False,
        )

        output = f"{result.stdout}\n{result.stderr}".strip()

        if result.returncode != 0 or "Everything is Ok" not in output:
            raise ArchiveValidationError(
                f"Archive validation failed.\n\n{output}"
            )

        print("Archive validation passed: Everything is Ok.")
