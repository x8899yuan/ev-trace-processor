from pathlib import Path
from datetime import datetime


class HtmlReporter:
    """Generate HTML reports from trace analysis results."""

    def generate(self, analysis_result, output_dir="reports"):
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = output_path / f"trace_report_{timestamp}.html"

        top_ids_rows = ""
        for can_id, count in analysis_result.get("top_ids", {}).items():
            top_ids_rows += f"<tr><td>{can_id}</td><td>{count:,}</td></tr>"

        channels = analysis_result.get("channels", [])
        channel_text = ", ".join(str(ch) for ch in channels) if channels else "N/A"

        html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset=\"utf-8\">
<title>EV Trace Report</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 30px; background:#f5f5f5; }}
h1,h2 {{ color:#1f4e79; }}
.table {{ border-collapse: collapse; width: 100%; background:white; }}
.table th, .table td {{ border:1px solid #ddd; padding:8px; }}
.table th {{ background:#1f4e79; color:white; }}
.card {{ background:white; padding:20px; margin-bottom:20px; border-radius:8px; }}
</style>
</head>
<body>

<h1>EV Trace Analysis Report</h1>

<div class=\"card\">
<h2>File Information</h2>
<table class=\"table\">
<tr><td><b>File Name</b></td><td>{analysis_result.get('file_name')}</td></tr>
<tr><td><b>File Size (MB)</b></td><td>{analysis_result.get('file_size_mb')}</td></tr>
</table>
</div>

<div class=\"card\">
<h2>Trace Statistics</h2>
<table class=\"table\">
<tr><td><b>Total Messages</b></td><td>{analysis_result.get('message_count',0):,}</td></tr>
<tr><td><b>Unique CAN IDs</b></td><td>{analysis_result.get('unique_ids',0):,}</td></tr>
<tr><td><b>First Timestamp</b></td><td>{analysis_result.get('first_timestamp')}</td></tr>
<tr><td><b>Last Timestamp</b></td><td>{analysis_result.get('last_timestamp')}</td></tr>
<tr><td><b>Duration (sec)</b></td><td>{analysis_result.get('duration_sec')}</td></tr>
<tr><td><b>Average Msg Rate</b></td><td>{analysis_result.get('avg_msg_rate')} msg/sec</td></tr>
<tr><td><b>Standard Frames</b></td><td>{analysis_result.get('standard_frames',0):,}</td></tr>
<tr><td><b>Extended Frames</b></td><td>{analysis_result.get('extended_frames',0):,}</td></tr>
<tr><td><b>Channel Count</b></td><td>{analysis_result.get('channel_count')}</td></tr>
<tr><td><b>Channels</b></td><td>{channel_text}</td></tr>
</table>
</div>

<div class=\"card\">
<h2>Top 20 CAN IDs</h2>
<table class=\"table\">
<tr><th>CAN ID</th><th>Message Count</th></tr>
{top_ids_rows}
</table>
</div>

</body>
</html>
"""

        report_file.write_text(html, encoding='utf-8')
        return str(report_file)
