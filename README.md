# Space Cadet Theme for MyBB

Space Cadet is a custom MyBB theme built from the open-source MyBB 1.8.40 Master Style. The project begins with the complete stock theme so every template and stylesheet can be inspected, then modified components can be retained while unchanged components are eventually removed from the release export.

## Repository Structure

```text
theme_parts/
├── properties.xml
├── stylesheets/       # 7 editable stock stylesheets
└── templates/         # 971 editable stock templates
upstream/
└── mybb-1.8.40/
    └── mybb_theme.xml # untouched upstream reference
scripts/
├── split_theme.py
└── assemble_theme.py
theme.json
space-cadet-theme.xml
```

The `upstream/` file is the authoritative MyBB baseline and should not be edited. Make theme changes under `theme_parts/`.

## Development Workflow

To reset `theme_parts/` from the untouched upstream theme:

```bash
python3 scripts/split_theme.py
```

**Warning:** this command deletes and recreates `theme_parts/`, overwriting theme work. Use it only when intentionally resetting or updating the baseline.

After editing templates or stylesheets, rebuild the importable theme:

```bash
python3 scripts/assemble_theme.py
```

The generated file is `space-cadet-theme.xml`. Import it through MyBB Admin CP under **Templates & Style → Import a Theme** and test it on a non-production forum.

## Versioning

Project metadata lives in `theme.json`:

- `theme_version` is the Space Cadet release version and follows semantic versioning.
- `mybb_version` is MyBB's compatibility code. Keep it at `1840` while the theme targets MyBB 1.8.40.
- `name` and `output` control the generated theme name and filename.

## Testing

Test guest and member views, forum and thread pages, profiles, private messages, moderation controls, and responsive layouts. Re-import the generated XML into a clean MyBB 1.8.40 test installation before publishing a release.

## License

The baseline theme is derived from MyBB. Retain the applicable MyBB copyright and license notices. New Space Cadet assets and licensing should be documented here before the first public release.
