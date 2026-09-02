from pathlib import Path

from archive_discovery import discover_volumes
from archive_merger import ArchiveMerger
from archive_validator import ArchiveValidator
from archive_extractor import ArchiveExtractor
from trace_detector import find_trace_files


SEVEN_ZIP = Path(r"C:\Program Files\7-Zip\7z.exe")
INPUT_FOLDER = Path(r"C:\Temp\PnC Testing Traces\test")
OUTPUT_FOLDER = INPUT_FOLDER / "Processed"


def process_archives() -> Path:
    """Discover, merge, validate, and extract archive volumes."""
    print("1. Discovering archive volumes...")
    volumes = discover_volumes(INPUT_FOLDER)

    if not volumes:
        raise FileNotFoundError(
            f"No archive volumes were found in: {INPUT_FOLDER}"
        )

    print(f"   Found {len(volumes)} archive volume(s).")

    merged_archive = OUTPUT_FOLDER / volumes[0].path.name.removesuffix(".001")

    print("2. Merging archive volumes...")
    ArchiveMerger.merge(volumes, merged_archive)

    print("3. Validating merged archive...")
    ArchiveValidator.test_archive(merged_archive, str(SEVEN_ZIP))

    extraction_folder = OUTPUT_FOLDER / "Extracted"

    print("4. Extracting archive...")
    ArchiveExtractor.extract(
        merged_archive,
        extraction_folder,
        str(SEVEN_ZIP),
    )

    return extraction_folder


def locate_trace_files(extraction_folder: Path) -> list[Path]:
    """Find supported trace files in the extraction folder."""
    print("5. Searching for trace files...")
    return find_trace_files(extraction_folder)


def print_trace_summary(traces: list[Path]) -> None:
    """Print a summary of discovered trace files."""
    print("\nTrace Files Found:")
    print("-" * 60)

    if not traces:
        print("No supported trace files were found.")
        return

    for index, trace in enumerate(traces, start=1):
        print(f"{index}. {trace}")

    print("-" * 60)
    print(f"Total trace files found: {len(traces)}")


def main() -> None:
    """Run the EV Trace Processor application."""
    print("=" * 60)
    print("EV Trace Processor")
    print("=" * 60)
    print("Application started\n")

    try:
        OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

        extraction_folder = process_archives()
        traces = locate_trace_files(extraction_folder)
        print_trace_summary(traces)

        print("\nApplication completed successfully")

    except Exception as error:
        print(f"\nApplication failed: {error}")
        raise


if __name__ == "__main__":
    main()
