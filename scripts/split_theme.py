#!/usr/bin/env python3
"""Refresh the split MyBB 1.8.40 upstream reference."""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "upstream" / "mybb-1.8.40" / "mybb_theme.xml"
OUTPUT = ROOT / "upstream" / "mybb-1.8.40" / "theme_parts"


def one(source: str, tag: str) -> str:
    match = re.search(rf"<{tag}\b.*?</{tag}>", source, re.DOTALL)
    if not match:
        raise ValueError(f"Missing <{tag}> in {SOURCE.name}")
    return match.group(0).strip()


def named(source: str, tag: str) -> list[tuple[str, str]]:
    pattern = re.compile(
        rf"(<{tag}\s+[^>]*\bname=([\"'])(.*?)\2[^>]*>.*?</{tag}>)",
        re.DOTALL,
    )
    return [(match.group(3), match.group(1).strip()) for match in pattern.finditer(source)]


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8-sig")
    stylesheets = named(source, "stylesheet")
    templates = named(source, "template")
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    (OUTPUT / "stylesheets").mkdir(parents=True)
    (OUTPUT / "templates").mkdir()
    (OUTPUT / "properties.xml").write_text(one(source, "properties") + "\n", encoding="utf-8")
    for name, fragment in stylesheets:
        (OUTPUT / "stylesheets" / f"{name}.xml").write_text(fragment + "\n", encoding="utf-8")
    for name, fragment in templates:
        (OUTPUT / "templates" / f"{name}.xml").write_text(fragment + "\n", encoding="utf-8")
    print(f"Refreshed upstream split: {len(stylesheets)} stylesheets and {len(templates)} templates.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        print(f"Upstream split failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
