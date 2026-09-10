import shutil
import subprocess
import zipfile
from pathlib import Path

from config import ProcessorConfig
from exceptions import ArchiveExtractionError


class ArchiveExtractor:
    """Extract the merged 7z archive and nested ZIP archives."""

    def __init__(self, config: ProcessorConfig) -> None:
        self.config = config

    def extract_7z(self, archive: Path, destination: Path) -> list[Path]:
        """Extract the reconstructed 7z archive with 7-Zip."""

        self._prepare_destination(destination)
        print(f"\nExtracting 7z archive: {archive.name}")

        result = subprocess.run(
            [
                str(self.config.seven_zip_path),
                "x",
                str(archive),
                f"-o{destination}",
                "-y",
            ],
            capture_output=True,
            text=True,
            errors="replace",
            check=False,
        )

        output = f"{result.stdout}\n{result.stderr}".strip()

        if result.returncode != 0:
            raise ArchiveExtractionError(
                f"7z extraction failed.\n\n{output}"
            )

        extracted_files = self._list_files(destination)
        if not extracted_files:
            raise ArchiveExtractionError(
                "7-Zip completed, but no extracted files were found in:\n"
                f"{destination}"
            )

        print(f"7z extraction complete: {len(extracted_files)} file(s)")
        return extracted_files

    def extract_nested_zip_files(self, root_folder: Path) -> list[Path]:
        """Test and extract every ZIP found under the extraction folder."""

        zip_files = sorted(root_folder.rglob("*.zip"))
        if not zip_files:
            print("\nNo nested ZIP archive was found.")
            return []

        all_extracted_files: list[Path] = []

        for zip_file in zip_files:
            destination = zip_file.parent / f"{zip_file.stem}_extracted"
            self._prepare_destination(destination)
            print(f"\nExtracting nested ZIP: {zip_file.name}")

            try:
                with zipfile.ZipFile(zip_file, mode="r") as zip_archive:
                    bad_file = zip_archive.testzip()
                    if bad_file is not None:
                        raise ArchiveExtractionError(
                            "The ZIP archive contains a damaged file:\n"
                            f"{bad_file}"
                        )
                    zip_archive.extractall(destination)
            except zipfile.BadZipFile as error:
                raise ArchiveExtractionError(
                    f"Invalid ZIP archive:\n{zip_file}"
                ) from error

            extracted_files = self._list_files(destination)
            all_extracted_files.extend(extracted_files)
            print(
                f"ZIP extraction complete: {len(extracted_files)} file(s)"
            )

        return all_extracted_files

    def _prepare_destination(self, destination: Path) -> None:
        if destination.exists() and self.config.overwrite:
            shutil.rmtree(destination)

        destination.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _list_files(folder: Path) -> list[Path]:
        return sorted(
            (path for path in folder.rglob("*") if path.is_file()),
            key=lambda path: str(path).lower(),
        )
