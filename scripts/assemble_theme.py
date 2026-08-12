#!/usr/bin/env python3
"""Assemble editable fragments into the configured Space Cadet theme export."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARTS = ROOT / "theme_parts"
REFERENCE = ROOT / "upstream" / "mybb-1.8.40" / "mybb_theme.xml"
CONFIG = ROOT / "theme.json"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").strip()


def attribute(xml: str, name: str) -> str:
    match = re.search(rf"\s{re.escape(name)}=([\"'])(.*?)\1", xml, re.DOTALL)
    return match.group(2) if match else ""


def reference_names(source: str, tag: str) -> list[str]:
    pattern = re.compile(rf"<{tag}\s+[^>]*\bname=([\"'])(.*?)\1")
    return [match.group(2) for match in pattern.finditer(source)]


def load_parts(folder: str, tag: str) -> dict[str, str]:
    parts: dict[str, str] = {}
    for path in sorted((PARTS / folder).glob("*.xml")):
        xml = read(path)
        name = attribute(xml, "name")
        if not name or not xml.startswith(f"<{tag}") or not xml.endswith(f"</{tag}>"):
            raise ValueError(f"Invalid {tag} fragment: {path}")
        if name in parts:
            raise ValueError(f"Duplicate {tag} name: {name}")
        parts[name] = xml
    return parts


def ordered(reference: list[str], parts: dict[str, str]) -> list[str]:
    result = [parts[name] for name in reference if name in parts]
    result.extend(parts[name] for name in sorted(parts) if name not in reference)
    return result


def main() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    output_path = ROOT / config["output"]
    reference = read(REFERENCE)
    properties = read(PARTS / "properties.xml")
    stylesheets = load_parts("stylesheets", "stylesheet")
    templates = load_parts("templates", "template")
    output = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<theme name="{config["name"]}" version="{config["mybb_version"]}">',
        properties,
        "<stylesheets>",
        *ordered(reference_names(reference, "stylesheet"), stylesheets),
        "</stylesheets>",
        "<templates>",
        *ordered(reference_names(reference, "template"), templates),
        "</templates>",
        "</theme>",
        "",
    ]
    output_path.write_text("\n".join(output), encoding="utf-8")
    print(
        f'Assembled {config["name"]} {config["theme_version"]}: '
        f'{len(stylesheets)} stylesheets and {len(templates)} templates into {output_path.name}.'
    )


if __name__ == "__main__":
    try:
        main()
    except (KeyError, json.JSONDecodeError, OSError, ValueError) as error:
        print(f"Theme assembly failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
