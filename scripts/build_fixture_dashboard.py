#!/usr/bin/env python3
"""
Build a static HTML dashboard from local fixture JSON files.

Default fixture directory:
    assets/fixtures/
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_status(raw: str) -> str:
    value = str(raw or "UNKNOWN").upper()
    if value.startswith("SUMMED_INFO_"):
        value = value.replace("SUMMED_INFO_", "", 1)
    if "DOWN" in value:
        return "DOWN"
    if "WARN" in value or "UNUSUAL" in value:
        return "WARNING"
    if "PAUSED" in value or "UNKNOWN" in value:
        return "PAUSED/UNKNOWN"
    if "UP" in value:
        return "UP"
    return "OTHER"


def status_badge(status: str) -> str:
    normalized = normalize_status(status)
    mapping = {
        "UP": ("#8F9900", "#FDFFEB"),
        "DOWN": ("#E3063D", "#FFF6F8"),
        "WARNING": ("#DE6800", "#FFF8F3"),
        "PAUSED/UNKNOWN": ("#686B76", "#F1F1F3"),
        "OTHER": ("#686B76", "#F1F1F3"),
    }
    fg, bg = mapping.get(normalized, mapping["OTHER"])
    return (
        f'<span style="display:inline-block;padding:2px 10px;border-radius:999px;'
        f'background:{bg};color:{fg};font-size:12px;font-weight:600">{normalized}</span>'
    )


def build_html(devices: List[Dict], sensors: List[Dict], timeseries: List[Dict]) -> str:
    status_counts: Dict[str, int] = {}
    for sensor in sensors:
        status = normalize_status(sensor.get("status", "UNKNOWN"))
        status_counts[status] = status_counts.get(status, 0) + 1

    down_warning = [
        s for s in sensors if normalize_status(s.get("status", "UNKNOWN")) in {"DOWN", "WARNING"}
    ]
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    rows = []
    for sensor in down_warning:
        parent = sensor.get("parent", {})
        rows.append(
            "<tr>"
            f"<td>{parent.get('name', 'Unknown')}</td>"
            f"<td>{sensor.get('name', 'Unknown')}</td>"
            f"<td>{sensor.get('kind_name', 'Unknown')}</td>"
            f"<td>{status_badge(sensor.get('status', 'UNKNOWN'))}</td>"
            "</tr>"
        )

    ts_preview = []
    for row in timeseries[:5]:
        cols = "".join(f"<td>{value}</td>" for value in row.values())
        ts_preview.append(f"<tr>{cols}</tr>")

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>PRTG Fixture Dashboard</title>
  <style>
    :root {{
      --text:#31343F;
      --brand:#050F34;
      --bg:#F9F9FA;
      --card:#FFFFFF;
      --border:#DBDCDF;
      --accent:#0F67FF;
    }}
    body {{
      margin: 0;
      font-family: Roboto, "Segoe UI", Tahoma, Arial, Helvetica, Verdana, sans-serif;
      color: var(--text);
      background: var(--bg);
    }}
    .container {{ max-width: 1100px; margin: 0 auto; padding: 20px; }}
    .card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 16px;
    }}
    .kpis {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }}
    .kpi {{ padding: 12px; border: 1px solid var(--border); border-radius: 6px; background: #fff; }}
    h1 {{ color: var(--brand); margin: 0; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ padding: 8px; border-bottom: 1px solid var(--border); text-align: left; font-size: 13px; }}
    th {{ color: var(--brand); background: #F1F1F3; }}
    .meta {{ color: #686B76; font-size: 12px; margin-top: 4px; }}
    @media (max-width: 860px) {{
      .kpis {{ grid-template-columns: 1fr 1fr; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="card">
      <h1>PRTG Fixture Dashboard</h1>
      <div class="meta">Offline fixture mode | Generated: {generated}</div>
    </div>

    <div class="card kpis">
      <div class="kpi"><strong>{len(devices)}</strong><div class="meta">Devices</div></div>
      <div class="kpi"><strong>{len(sensors)}</strong><div class="meta">Sensors</div></div>
      <div class="kpi"><strong>{status_counts.get("DOWN", 0)}</strong><div class="meta">Down</div></div>
      <div class="kpi"><strong>{status_counts.get("WARNING", 0)}</strong><div class="meta">Warning</div></div>
    </div>

    <div class="card">
      <h2>Problem Sensors</h2>
      <table>
        <tr><th>Device</th><th>Sensor</th><th>Type</th><th>Status</th></tr>
        {''.join(rows) if rows else '<tr><td colspan="4">No down/warning sensors in fixtures.</td></tr>'}
      </table>
    </div>

    <div class="card">
      <h2>Timeseries Preview</h2>
      <table>
        <tr>{''.join(f'<th>{key}</th>' for key in (timeseries[0].keys() if timeseries else ['datetime']))}</tr>
        {''.join(ts_preview) if ts_preview else '<tr><td>No fixture timeseries rows found.</td></tr>'}
      </table>
    </div>
  </div>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a dashboard from local fixture files.")
    parser.add_argument(
        "--fixtures-dir",
        default="assets/fixtures",
        help="Directory containing devices/sensors/channels/timeseries fixture JSON files.",
    )
    parser.add_argument(
        "--output",
        default="fixture-dashboard.html",
        help="Output HTML file path.",
    )
    args = parser.parse_args()

    fixture_dir = Path(args.fixtures_dir)
    output = Path(args.output)

    devices = load_json(fixture_dir / "devices.sample.json")
    sensors = load_json(fixture_dir / "sensors.sample.json")
    timeseries = load_json(fixture_dir / "timeseries.sample.json")

    html = build_html(devices, sensors, timeseries)
    output.write_text(html, encoding="utf-8")
    print(f"Wrote fixture dashboard: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
