#!/usr/bin/env python3
"""Build the minimal Space Cadet child-theme export from overrides."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OVERRIDES = ROOT / "theme_overrides"
CONFIG = ROOT / "theme.json"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").strip()


def attribute(xml: str, name: str) -> str:
    match = re.search(rf"\s{re.escape(name)}=([\"'])(.*?)\1", xml, re.DOTALL)
    return match.group(2) if match else ""


def load_parts(folder: str, tag: str) -> list[str]:
    parts: dict[str, str] = {}
    directory = OVERRIDES / folder
    for path in sorted(directory.glob("*.xml")):
        xml = read(path)
        name = attribute(xml, "name")
        if not name or not xml.startswith(f"<{tag}") or not xml.endswith(f"</{tag}>"):
            raise ValueError(f"Invalid {tag} override: {path}")
        if name in parts:
            raise ValueError(f"Duplicate {tag} override: {name}")
        parts[name] = xml
    return list(parts.values())


def main() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    output_path = ROOT / config["output"]
    stylesheets = load_parts("stylesheets", "stylesheet")
    templates = load_parts("templates", "template")
    output = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<!-- {config["name"]} release {config["theme_version"]} -->',
        f'<theme name="{config["name"]}" version="{config["mybb_version"]}">',
        read(OVERRIDES / "properties.xml"),
        "<stylesheets>", *stylesheets, "</stylesheets>",
        "<templates>", *templates, "</templates>",
        "</theme>", "",
    ]
    output_path.write_text("\n".join(output), encoding="utf-8")
    print(
        f'Assembled {config["name"]} {config["theme_version"]}: '
        f'{len(stylesheets)} stylesheet overrides and {len(templates)} template overrides.'
    )


if __name__ == "__main__":
    try:
        main()
    except (KeyError, json.JSONDecodeError, OSError, ValueError) as error:
        print(f"Theme assembly failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
