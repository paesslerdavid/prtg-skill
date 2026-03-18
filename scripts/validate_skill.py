#!/usr/bin/env python3
"""
Local validation for this skill repository.

Checks:
- SKILL.md frontmatter includes required keys
- SKILL.md stays under recommended line budget
- Referenced files in SKILL.md (${CLAUDE_SKILL_DIR}/...) exist locally
- Core directories/files required by this skill exist
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Tuple


ROOT = Path(__file__).resolve().parents[1]
SKILL_FILE = ROOT / "SKILL.md"


def parse_frontmatter(text: str) -> Tuple[dict, int]:
    if not text.startswith("---\n"):
        return {}, 0
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, 0
    raw = text[4:end].splitlines()
    data = {}
    for line in raw:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data, end + len("\n---\n")


def extract_skill_dir_refs(text: str) -> List[str]:
    pattern = re.compile(r"\$\{CLAUDE_SKILL_DIR\}/([A-Za-z0-9_\-./]+)")
    return sorted(set(pattern.findall(text)))


def main() -> int:
    errors: List[str] = []
    warnings: List[str] = []

    if not SKILL_FILE.exists():
        print("ERROR: SKILL.md not found.")
        return 1

    skill_text = SKILL_FILE.read_text(encoding="utf-8")
    frontmatter, _ = parse_frontmatter(skill_text)

    if "name" not in frontmatter:
        errors.append("Frontmatter missing required key: name")
    if "description" not in frontmatter:
        errors.append("Frontmatter missing required key: description")

    line_count = len(skill_text.splitlines())
    if line_count > 500:
        warnings.append(f"SKILL.md is {line_count} lines; consider keeping under 500 lines.")

    refs = extract_skill_dir_refs(skill_text)
    for rel_path in refs:
        if not (ROOT / rel_path).exists():
            errors.append(f"Referenced file does not exist: {rel_path}")

    required = [
        "README.md",
        "references/api-endpoints.md",
        "references/api-filtering.md",
        "references/api-schemas.md",
        "scripts/update_docs.py",
        "scripts/fetch_spectrum.py",
        "scripts/preflight.py",
        "scripts/prtg_client.py",
        "scripts/build_fixture_dashboard.py",
        "references/write-operations-playbook.md",
        "references/error-handling.md",
        "assets/dashboard-templates/status-overview-template.html",
        "assets/dashboard-templates/timeseries-template.html",
        "assets/fixtures/devices.sample.json",
    ]
    for rel_path in required:
        if not (ROOT / rel_path).exists():
            errors.append(f"Missing required repository file: {rel_path}")

    print("Skill validation")
    print("=" * 60)
    if warnings:
        for item in warnings:
            print(f"WARN: {item}")
    else:
        print("WARN: none")

    if errors:
        for item in errors:
            print(f"ERROR: {item}")
        print("\nResult: FAILED")
        return 1

    print("ERROR: none")
    print("\nResult: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
