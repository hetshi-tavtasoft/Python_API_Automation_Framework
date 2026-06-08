import os
import json
from datetime import datetime
from pathlib import Path


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: #0d1117;
    color: #e6edf3;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    padding: 32px 24px;
  }}
  .container {{ max-width: 1200px; margin: 0 auto; }}

  /* Header */
  .header {{
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 32px; padding-bottom: 20px;
    border-bottom: 1px solid #30363d;
  }}
  .header h1 {{
    font-size: 24px; font-weight: 700;
    background: linear-gradient(135deg, #58a6ff, #3fb950);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }}
  .header .meta {{ text-align: right; color: #8b949e; font-size: 13px; line-height: 1.6; }}

  /* Stats Cards */
  .cards {{
    display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px;
    margin-bottom: 28px;
  }}
  .card {{
    background: #161b22; border: 1px solid #30363d; border-radius: 10px;
    padding: 18px 16px; text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
  }}
  .card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 20px rgba(0,0,0,0.4); }}
  .card .value {{ font-size: 28px; font-weight: 700; margin-bottom: 4px; }}
  .card .label {{ font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; color: #8b949e; }}
  .card-total .value {{ color: #58a6ff; }}
  .card-passed .value {{ color: #3fb950; }}
  .card-failed .value {{ color: #f85149; }}
  .card-skipped .value {{ color: #d29922; }}
  .card-rate .value {{ color: #58a6ff; }}

  /* Chart Section */
  .chart-section {{
    background: #161b22; border: 1px solid #30363d; border-radius: 10px;
    padding: 24px; margin-bottom: 28px;
    display: flex; align-items: center; gap: 40px;
  }}
  .chart-section h2 {{ font-size: 16px; color: #8b949e; margin-bottom: 16px; }}

  .pie-chart {{
    position: relative; width: 180px; height: 180px; flex-shrink: 0;
  }}
  .pie-chart svg {{ width: 100%; height: 100%; transform: rotate(-90deg); }}
  .pie-chart .center-text {{
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    text-align: center;
  }}
  .pie-chart .center-text .big {{ font-size: 32px; font-weight: 700; color: #e6edf3; }}
  .pie-chart .center-text .small {{ font-size: 12px; color: #8b949e; }}

  .chart-legend {{ display: flex; flex-direction: column; gap: 10px; }}
  .chart-legend .item {{
    display: flex; align-items: center; gap: 10px; font-size: 14px;
  }}
  .chart-legend .dot {{
    width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0;
  }}
  .chart-legend .count {{ margin-left: auto; color: #8b949e; }}

  /* Duration Bar Chart */
  .duration-chart {{
    background: #161b22; border: 1px solid #30363d; border-radius: 10px;
    padding: 24px; margin-bottom: 28px;
  }}
  .duration-chart h2 {{ font-size: 16px; color: #8b949e; margin-bottom: 16px; }}
  .bar-row {{
    display: flex; align-items: center; gap: 12px; margin-bottom: 8px;
  }}
  .bar-row .bar-label {{
    width: 260px; font-size: 13px; white-space: nowrap; overflow: hidden;
    text-overflow: ellipsis; color: #e6edf3; flex-shrink: 0;
  }}
  .bar-row .bar-track {{
    flex: 1; height: 22px; background: #0d1117; border-radius: 4px;
    overflow: hidden; position: relative;
  }}
  .bar-row .bar-fill {{
    height: 100%; border-radius: 4px; transition: width 0.8s ease;
  }}
  .bar-row .bar-fill.passed {{ background: linear-gradient(90deg, #3fb950, #2ea043); }}
  .bar-row .bar-fill.failed {{ background: linear-gradient(90deg, #f85149, #da3633); }}
  .bar-row .bar-duration {{
    width: 60px; text-align: right; font-size: 12px; color: #8b949e; flex-shrink: 0;
  }}

  /* Test Results Table */
  .table-section {{
    background: #161b22; border: 1px solid #30363d; border-radius: 10px;
    overflow: hidden; margin-bottom: 28px;
  }}
  .table-section h2 {{
    font-size: 16px; color: #8b949e; padding: 16px 20px;
    border-bottom: 1px solid #30363d;
  }}
  table {{
    width: 100%; border-collapse: collapse; font-size: 14px;
  }}
  thead th {{
    background: #0d1117; color: #8b949e; font-weight: 600;
    text-transform: uppercase; font-size: 11px; letter-spacing: 0.5px;
    padding: 12px 16px; text-align: left; border-bottom: 1px solid #30363d;
  }}
  tbody td {{
    padding: 12px 16px; border-bottom: 1px solid #21262d;
    vertical-align: middle;
  }}
  tbody tr:hover td {{ background: #1c2128; }}
  tbody tr:last-child td {{ border-bottom: none; }}
  .status-badge {{
    display: inline-flex; align-items: center; gap: 6px;
    padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 600;
  }}
  .status-badge.passed {{ background: rgba(63,185,80,0.15); color: #3fb950; }}
  .status-badge.failed {{ background: rgba(248,81,73,0.15); color: #f85149; }}
  .status-badge.skipped {{ background: rgba(210,153,34,0.15); color: #d29922; }}
  .status-badge.error {{ background: rgba(248,81,73,0.15); color: #f85149; }}
  .test-name {{ color: #e6edf3; font-weight: 500; cursor: pointer; }}
  .test-details {{ display: none; background: #0d1117; }}
  .test-details.open {{ display: table-row; }}
  .test-details td {{ padding: 0; }}
  .test-details .detail-content {{
    padding: 16px 20px; font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px; line-height: 1.5; color: #8b949e;
    border-top: 1px solid #21262d;
  }}
  .test-details .detail-content pre {{
    white-space: pre-wrap; word-break: break-word; margin: 0;
  }}
  .detail-toggle {{ cursor: pointer; user-select: none; opacity: 0.6; }}
  .detail-toggle:hover {{ opacity: 1; }}

  /* Environment */
  .env-section {{
    background: #161b22; border: 1px solid #30363d; border-radius: 10px;
    padding: 20px; margin-bottom: 28px;
  }}
  .env-section h2 {{ font-size: 16px; color: #8b949e; margin-bottom: 14px; }}
  .env-grid {{
    display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 10px;
  }}
  .env-item {{
    display: flex; justify-content: space-between; padding: 8px 12px;
    background: #0d1117; border-radius: 6px; font-size: 13px;
  }}
  .env-item .key {{ color: #8b949e; }}
  .env-item .value {{ color: #e6edf3; font-weight: 500; }}

  .footer {{
    text-align: center; color: #484f58; font-size: 12px; padding: 20px 0;
  }}

  @media (max-width: 768px) {{
    .cards {{ grid-template-columns: repeat(2, 1fr); }}
    .chart-section {{ flex-direction: column; }}
    .bar-row .bar-label {{ width: 140px; }}
  }}
</style>
</head>
<body>
<div class="container">

  <!-- Header -->
  <div class="header">
    <h1>🚀 {title}</h1>
    <div class="meta">
      <div>Run: {timestamp}</div>
      <div>Duration: {total_duration}</div>
    </div>
  </div>

  <!-- Stats Cards -->
  <div class="cards">
    <div class="card card-total">
      <div class="value">{total}</div>
      <div class="label">Total Tests</div>
    </div>
    <div class="card card-passed">
      <div class="value">{passed}</div>
      <div class="label">Passed</div>
    </div>
    <div class="card card-failed">
      <div class="value">{failed}</div>
      <div class="label">Failed</div>
    </div>
    <div class="card card-skipped">
      <div class="value">{skipped}</div>
      <div class="label">Skipped</div>
    </div>
    <div class="card card-rate">
      <div class="value">{pass_rate}%</div>
      <div class="label">Pass Rate</div>
    </div>
  </div>

  <!-- Pie Chart -->
  <div class="chart-section">
    <div>
      <h2>Test Results Distribution</h2>
      <div class="pie-chart">
        <svg viewBox="0 0 100 100">
          {pie_slices}
        </svg>
        <div class="center-text">
          <div class="big">{total}</div>
          <div class="small">tests</div>
        </div>
      </div>
    </div>
    <div class="chart-legend">
      <div class="item"><span class="dot" style="background:#3fb950"></span> Passed <span class="count">{passed}</span></div>
      <div class="item"><span class="dot" style="background:#f85149"></span> Failed <span class="count">{failed}</span></div>
      <div class="item"><span class="dot" style="background:#d29922"></span> Skipped <span class="count">{skipped}</span></div>
    </div>
  </div>

  <!-- Duration Bars -->
  <div class="duration-chart">
    <h2>Test Duration (slowest first)</h2>
    {duration_bars}
  </div>

  <!-- Test Results Table -->
  <div class="table-section">
    <h2>Test Results</h2>
    <table>
      <thead>
        <tr>
          <th style="width:40px">#</th>
          <th>Test</th>
          <th style="width:100px">Status</th>
          <th style="width:80px">Duration</th>
          <th style="width:30px"></th>
        </tr>
      </thead>
      <tbody>
        {test_rows}
      </tbody>
    </table>
  </div>

  <!-- Environment -->
  <div class="env-section">
    <h2>Environment</h2>
    <div class="env-grid">
      {env_items}
    </div>
  </div>

  <div class="footer">Generated by Enterprise API Automation Framework</div>
</div>

<script>
  document.querySelectorAll('.detail-toggle').forEach(function(toggle) {{
    toggle.addEventListener('click', function() {{
      var details = this.closest('tr').nextElementSibling;
      if (details && details.classList.contains('test-details')) {{
        details.classList.toggle('open');
        this.textContent = details.classList.contains('open') ? '▲' : '▼';
      }}
    }});
  }});
</script>
</body>
</html>"""


def _generate_pie(total, passed, failed, skipped):
    if total == 0:
        return '<circle cx="50" cy="50" r="40" fill="none" stroke="#30363d" stroke-width="8"/>'

    slices = []
    data = [
        (passed, "#3fb950", "Passed"),
        (failed, "#f85149", "Failed"),
        (skipped, "#d29922", "Skipped"),
    ]
    data = [(c, color, label) for c, color, label in data if c > 0]
    total_valid = sum(c for c, _, _ in data)
    if total_valid == 0:
        return '<circle cx="50" cy="50" r="40" fill="none" stroke="#30363d" stroke-width="8"/>'

    offset = 0
    for count, color, label in data:
        pct = count / total_valid
        angle = pct * 360
        if angle >= 359.99:
            large_arc = 1
            end_x = 50 + 40 * 0.0001
            end_y = 50 - 40
        else:
            large_arc = 1 if angle > 180 else 0
            rad = (angle - 90) * 3.14159 / 180
            end_x = 50 + 40 * __import__("math").cos(rad)
            end_y = 50 + 40 * __import__("math").sin(rad)

        start_rad = (offset - 90) * 3.14159 / 180
        start_x = 50 + 40 * __import__("math").cos(start_rad)
        start_y = 50 + 40 * __import__("math").sin(start_rad)

        slices.append(
            f'<path d="M50,50 L{start_x:.2f},{start_y:.2f} '
            f'A40,40 0 {large_arc},1 {end_x:.2f},{end_y:.2f} Z" '
            f'fill="{color}"/>'
        )
        offset += angle

    return "\n".join(slices)


def _duration_str(seconds):
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    if seconds < 60:
        return f"{seconds:.2f}s"
    return f"{int(seconds // 60)}m {int(seconds % 60)}s"


def generate_report(test_results, env_info, output_path, title="API Automation Test Report"):
    total = len(test_results)
    passed = sum(1 for r in test_results if r["status"] == "passed")
    failed = sum(1 for r in test_results if r["status"] == "failed")
    skipped = sum(1 for r in test_results if r["status"] in ("skipped", "xfailed"))
    total_duration = sum(r["duration"] for r in test_results)
    pass_rate = round((passed / total * 100) if total > 0 else 0, 1)

    sorted_tests = sorted(test_results, key=lambda r: r["duration"], reverse=True)
    max_dur = sorted_tests[0]["duration"] if sorted_tests else 1

    # Duration bars
    bars = []
    for r in sorted_tests:
        pct = (r["duration"] / max_dur * 100) if max_dur > 0 else 0
        status_class = "passed" if r["status"] == "passed" else "failed"
        bars.append(
            f'<div class="bar-row">'
            f'<span class="bar-label">{r["name"][:60]}</span>'
            f'<div class="bar-track"><div class="bar-fill {status_class}" style="width:{pct:.1f}%"></div></div>'
            f'<span class="bar-duration">{_duration_str(r["duration"])}</span>'
            f'</div>'
        )

    # Test table rows
    rows = []
    status_icons = {"passed": "✅", "failed": "❌", "skipped": "⏭️", "error": "💥"}
    for i, r in enumerate(test_results, 1):
        status_class = r["status"]
        icon = status_icons.get(status_class, "❓")
        details = r.get("details", "").strip()
        has_details = bool(details)
        rows.append(
            f'<tr>'
            f'<td style="color:#8b949e">{i}</td>'
            f'<td class="test-name">{r["name"]}</td>'
            f'<td><span class="status-badge {status_class}">{icon} {status_class.title()}</span></td>'
            f'<td style="color:#8b949e">{_duration_str(r["duration"])}</td>'
            f'<td class="detail-toggle" style="cursor:pointer">{"" if has_details else ""}</td>'
            f'</tr>'
        )
        if has_details:
            rows.append(
                f'<tr class="test-details"><td colspan="5">'
                f'<div class="detail-content"><pre>{details}</pre></div>'
                f'</td></tr>'
            )

    env_items = "".join(
        f'<div class="env-item"><span class="key">{k}</span><span class="value">{v}</span></div>'
        for k, v in env_info.items()
    )

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pie_slices = _generate_pie(total, passed, failed, skipped)

    html = TEMPLATE.format(
        title=title,
        timestamp=timestamp,
        total_duration=_duration_str(total_duration),
        total=total,
        passed=passed,
        failed=failed,
        skipped=skipped,
        pass_rate=pass_rate,
        pie_slices=pie_slices,
        duration_bars="".join(bars),
        test_rows="".join(rows),
        env_items=env_items,
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return output_path
