#!/usr/bin/env python3
"""
Preflight checks for PRTG skill sessions.

Checks:
1) Credentials can be loaded from .env
2) API v2 auth works for probes/devices/sensors/channels
3) Filter syntax query works with quoted text
4) Optional API v1 fallback connectivity
5) Local spectrum.css availability hint
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Callable, List, Tuple

from prtg_client import PRTGClient, PRTGError, load_credentials


CheckResult = Tuple[str, str, str]


def run_check(name: str, fn: Callable[[], str]) -> CheckResult:
    try:
        detail = fn()
        return ("PASS", name, detail)
    except Exception as exc:  # pylint: disable=broad-except
        return ("FAIL", name, str(exc))


def run_warn(name: str, fn: Callable[[], str]) -> CheckResult:
    try:
        detail = fn()
        return ("WARN", name, detail)
    except Exception as exc:  # pylint: disable=broad-except
        return ("WARN", name, str(exc))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run PRTG skill preflight checks.")
    parser.add_argument(
        "credentials_file",
        nargs="?",
        help="Optional path to .env file. Defaults to first *.env in CWD.",
    )
    args = parser.parse_args()

    creds = load_credentials(args.credentials_file)
    client = PRTGClient(host=creds["host"], api_key=creds["api_key"], timeout=30)

    checks: List[CheckResult] = []
    checks.append(run_check("Credentials", lambda: f"Loaded from {creds['source']}"))
    checks.append(
        run_check(
            "API v2 devices",
            lambda: f"Fetched {len(client.get('experimental/devices', params={'limit': 1}))} sample row(s).",
        )
    )
    checks.append(
        run_check(
            "API v2 sensors",
            lambda: f"Fetched {len(client.get('experimental/sensors', params={'limit': 1}))} sample row(s).",
        )
    )
    checks.append(
        run_check(
            "API v2 channels",
            lambda: f"Fetched {len(client.get('experimental/channels', params={'limit': 1}))} sample row(s).",
        )
    )
    checks.append(
        run_check(
            "Filter syntax",
            lambda: (
                f"Filter query returned "
                f"{len(client.get('experimental/sensors', params={'filter': 'name contains \"Ping\"', 'limit': 1}))} sample row(s)."
            ),
        )
    )

    def v1_probe() -> str:
        data = client.get_v1("table.json", params={"content": "devices", "output": "json", "count": 1})
        if isinstance(data, dict):
            return "v1 fallback endpoint reachable."
        raise PRTGError("Unexpected v1 response shape.")

    checks.append(run_warn("API v1 fallback (optional)", v1_probe))

    spectrum_file = Path.cwd() / "spectrum.css"
    checks.append(
        run_warn(
            "Local spectrum.css",
            lambda: (
                f"Found {spectrum_file}"
                if spectrum_file.exists()
                else "spectrum.css not found in CWD (run scripts/fetch_spectrum.py if you need branded HTML)."
            ),
        )
    )

    print("\nPRTG skill preflight")
    print("=" * 60)
    for state, name, detail in checks:
        print(f"[{state}] {name}: {detail}")

    failures = [c for c in checks if c[0] == "FAIL"]
    if failures:
        print("\nResult: FAILED preflight checks.")
        return 1
    print("\nResult: READY (warnings are non-blocking).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
