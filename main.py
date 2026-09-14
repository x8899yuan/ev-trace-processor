"""
EV Trace Processor
Automated BLF Processing Workflow
"""

from pathlib import Path

from readers.reader_factory import ReaderFactory
from analyzers.trace_analyzer import TraceAnalyzer
from exporters.html_reporter import HtmlReporter


def verify_report(report_path):
    report_file = Path(report_path)

    if not report_file.exists():
        return False

    if report_file.stat().st_size == 0:
        return False

    return True


def get_trace_files():
    data_folder = Path("data/blf")

    if not data_folder.exists():
        raise FileNotFoundError(
            f"Folder not found: {data_folder.resolve()}"
        )

    trace_files = sorted(data_folder.glob("*.blf"))

    if not trace_files:
        raise FileNotFoundError(
            f"No BLF files found in {data_folder.resolve()}"
        )

    return trace_files


def print_summary(
    total_found,
    successful_files,
    failed_files,
    deleted_files,
    generated_reports,
):
    print("")
    print("=" * 60)
    print("EV TRACE PROCESSOR SUMMARY")
    print("=" * 60)

    print(f"Files Found : {total_found}")
    print(f"Processed   : {len(successful_files)}")
    print(f"Failed      : {len(failed_files)}")
    print(f"Deleted     : {len(deleted_files)}")

    print("Generated Reports")
    print("-" * 60)

    if generated_reports:
        for report in generated_reports:
            print(report)
    else:
        print("None")

    if failed_files:
        print("Failed Files")
        print("-" * 60)

        for item in failed_files:
            print(f"{item['file']} -> {item['error']}")

    print("=" * 60)


def main():
    print("" + "=" * 70)
    print("EV TRACE PROCESSOR")
    print("=" * 70)

    successful_files = []
    failed_files = []
    deleted_files = []
    generated_reports = []

    try:
        trace_files = get_trace_files()

        print(f"Found {len(trace_files)} BLF file(s)")

        for trace_file in trace_files:
            print(f"Processing: {trace_file.name}")

            try:
                reader = ReaderFactory.get_reader(trace_file)

                messages = reader.read(trace_file)

                analyzer = TraceAnalyzer()

                analysis_results = analyzer.analyze(
                    messages,
                    trace_file,
                )

                reporter = HtmlReporter()

                report_path = reporter.generate(
                    analysis_results,
                    trace_file,
                )

                if verify_report(report_path):
                    generated_reports.append(str(report_path))

                    trace_file.unlink()

                    successful_files.append(trace_file.name)
                    deleted_files.append(trace_file.name)

                    print(f"  SUCCESS - Report verified")
                    print(f"  DELETED - {trace_file.name}")
                else:
                    failed_files.append(
                        {
                            'file': trace_file.name,
                            'error': 'Report verification failed',
                        }
                    )

                    print("  FAILED - Report verification failed")

            except Exception as exc:
                failed_files.append(
                    {
                        'file': trace_file.name,
                        'error': str(exc),
                    }
                )

                print(f"  FAILED - {exc}")

        print_summary(
            total_found=len(trace_files),
            successful_files=successful_files,
            failed_files=failed_files,
            deleted_files=deleted_files,
            generated_reports=generated_reports,
        )

    except Exception as exc:
        print(f"ERROR: {exc}")


if __name__ == '__main__':
    main()
