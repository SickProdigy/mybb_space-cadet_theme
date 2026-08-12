#!/usr/bin/env python3
"""Split the official MyBB 1.8.40 master theme into editable fragments."""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "upstream" / "mybb-1.8.40" / "mybb_theme.xml"
OUTPUT = ROOT / "theme_parts"


def extract_one(source: str, tag: str) -> str:
    match = re.search(rf"<{tag}\b.*?</{tag}>", source, re.DOTALL)
    if match is None:
        raise ValueError(f"{SOURCE.name} does not contain <{tag}>")
    return match.group(0).strip()


def extract_named(source: str, tag: str) -> list[tuple[str, str]]:
    pattern = re.compile(
        rf"(<{tag}\s+[^>]*\bname=([\"'])(.*?)\2[^>]*>.*?</{tag}>)",
        re.DOTALL,
    )
    return [(match.group(3), match.group(1).strip()) for match in pattern.finditer(source)]


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8-sig")
    stylesheets = extract_named(source, "stylesheet")
    templates = extract_named(source, "template")

    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    stylesheet_dir = OUTPUT / "stylesheets"
    template_dir = OUTPUT / "templates"
    stylesheet_dir.mkdir(parents=True)
    template_dir.mkdir(parents=True)

    (OUTPUT / "properties.xml").write_text(
        extract_one(source, "properties") + "\n", encoding="utf-8"
    )
    for name, fragment in stylesheets:
        (stylesheet_dir / f"{name}.xml").write_text(fragment + "\n", encoding="utf-8")
    for name, fragment in templates:
        (template_dir / f"{name}.xml").write_text(fragment + "\n", encoding="utf-8")

    print(f"Split {len(stylesheets)} stylesheets and {len(templates)} templates into theme_parts/.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        print(f"Theme split failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
