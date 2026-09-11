from pathlib import Path

from readers.reader_factory import create_reader
from analyzers.trace_analyzer import TraceAnalyzer
from exporters.html_reporter import HtmlReporter


BLF_FOLDER = Path("data/blf")


def select_blf_file() -> Path:
    if not BLF_FOLDER.exists():
        raise FileNotFoundError(f"BLF folder not found: {BLF_FOLDER}")

    blf_files = sorted(BLF_FOLDER.glob("*.blf"))

    if not blf_files:
        raise FileNotFoundError(f"No .blf files found in {BLF_FOLDER}")

    print(f"
Found {len(blf_files)} BLF file(s):
")

    for index, file_path in enumerate(blf_files, start=1):
        print(f"[{index}] {file_path.name}")

    while True:
        selection = input("
Select file number: ").strip()

        try:
            selection = int(selection)

            if 1 <= selection <= len(blf_files):
                return blf_files[selection - 1]

        except ValueError:
            pass

        print("Invalid selection. Please try again.")


def generate_report(trace_file: str) -> str:
    reader = create_reader(trace_file)

    analyzer = TraceAnalyzer()
    report = analyzer.analyze(reader, trace_file)

    report_name = f"{Path(trace_file).stem}_report.html"
    output_file = Path("reports") / report_name

    reporter = HtmlReporter()
    report_path = reporter.export(report, str(output_file))

    return report_path


def main() -> None:
    print("=" * 70)
    print("EV Trace Processor")
    print("=" * 70)

    try:
        trace_file = select_blf_file()

        print(f"
Selected: {trace_file.name}")
        print("Generating report...
")

        report_path = generate_report(str(trace_file))

        print("Report generated successfully")
        print(f"HTML Report: {report_path}")

    except Exception as exc:
        print("
Report generation failed")
        print(str(exc))


if __name__ == "__main__":
    main()
