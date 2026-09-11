from pathlib import Path

from readers.reader_factory import create_reader
from analyzers.trace_analyzer import TraceAnalyzer
from exporters.html_reporter import HtmlReporter


def generate_report(trace_file: str) -> str:
    """Generate an HTML report for a supported trace file."""

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

    trace_file = input("Enter path to trace file (.blf): ").strip()

    if not trace_file:
        print("No trace file specified.")
        return

    trace_path = Path(trace_file)

    if not trace_path.exists():
        print(f"File not found: {trace_file}")
        return

    try:
        report_path = generate_report(trace_file)

        print()
        print("Report generated successfully")
        print(f"HTML Report: {report_path}")

    except Exception as exc:
        print()
        print("Report generation failed")
        print(str(exc))


if __name__ == "__main__":
    main()
