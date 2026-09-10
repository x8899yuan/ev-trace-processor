import sys

from archive_discovery import (
    discover_archive_volumes,
    get_merged_archive_name,
)
from archive_extractor import ArchiveExtractor
from archive_merger import ArchiveMerger
from archive_validator import ArchiveValidator
from config import load_config
from exceptions import TraceProcessorError
from models import ProcessingResult
from trace_detector import TraceDetector


def process_trace_package() -> ProcessingResult:
    """Run the complete KPM trace reconstruction workflow."""

    config = load_config()
    config.output_folder.mkdir(parents=True, exist_ok=True)

    # 1. Discover and verify numbered 7z chunks
    volumes = discover_archive_volumes(config.input_folder)
    print(f"Found {len(volumes)} archive volume(s).")

    for volume in volumes:
        print(
            f"{volume.volume_number:03d}: {volume.path.name} "
            f"({volume.size_bytes:,} bytes)"
        )

    # 2. Build the merged archive path
    merged_archive_name = get_merged_archive_name(volumes[0])
    merged_archive = config.output_folder / merged_archive_name

    # 3. Merge the numbered chunks
    merger = ArchiveMerger(config)
    merger.merge(volumes=volumes, output_file=merged_archive)

    # 4. Validate the reconstructed 7z archive
    validator = ArchiveValidator(config.seven_zip_path)
    validator.validate_archive(merged_archive)

    # 5. Extract the 7z archive
    extraction_folder = config.output_folder / "Extracted"
    extractor = ArchiveExtractor(config)
    extractor.extract_7z(
        archive=merged_archive,
        destination=extraction_folder,
    )

    # 6. Extract ZIP files contained inside the 7z archive
    extractor.extract_nested_zip_files(
        root_folder=extraction_folder
    )

    # 7. Detect final vehicle trace files
    final_trace_files = TraceDetector.find_trace_files(
        extraction_folder
    )

    return ProcessingResult(
        merged_archive=merged_archive,
        extraction_folder=extraction_folder,
        final_trace_files=final_trace_files,
    )


def print_result(result: ProcessingResult) -> None:
    """Print the final processing summary."""

    print("\n" + "=" * 70)
    print("KPM TRACE PROCESSING COMPLETED")
    print("=" * 70)
    print(f"Merged archive:\n{result.merged_archive}")
    print(f"\nExtraction folder:\n{result.extraction_folder}")

    if result.final_trace_files:
        print("\nFinal trace files:")
        for trace_file in result.final_trace_files:
            print(f"  {trace_file}")
            print(f"  Size: {trace_file.stat().st_size:,} bytes")
    else:
        print(
            "\nNo BLF, ASC, PCAP, PCAPNG, MF4, MDF, "
            "or ESOTRACE file was found."
        )

    print("=" * 70)


def main() -> int:
    """Application entry point."""

    try:
        result = process_trace_package()
        print_result(result)
        return 0
    except TraceProcessorError as error:
        print("\nPROCESSING ERROR")
        print(error)
        return 1
    except FileNotFoundError as error:
        print("\nFILE NOT FOUND")
        print(error)
        return 2
    except PermissionError as error:
        print("\nPERMISSION ERROR")
        print(error)
        return 3
    except KeyboardInterrupt:
        print("\nProcessing canceled.")
        return 130
    except Exception as error:
        print("\nUNEXPECTED ERROR")
        print(error)
        return 99


if __name__ == "__main__":
    sys.exit(main())
