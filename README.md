# Space Cadet Theme for MyBB

Space Cadet is a MyBB 1.8.40 child theme built from the open-source MyBB Master Style. The complete stock theme is retained as a versioned reference, while the importable release contains only intentional Space Cadet overrides.

## Repository Structure

```text
upstream/mybb-1.8.40/
├── mybb_theme.xml          # untouched official master theme
└── theme_parts/
    ├── properties.xml
    ├── stylesheets/        # 7 stock stylesheets
    └── templates/          # 971 stock templates
theme_overrides/
├── properties.xml
├── stylesheets/            # Space Cadet additions or replacements
└── templates/              # modified stock templates only
images/space-cadet/
└── fontawesome/             # self-hosted Font Awesome Free Solid assets
scripts/
├── split_theme.py
└── assemble_theme.py
theme.json                  # project and compatibility metadata
space-cadet-theme.xml       # generated minimal import file
```

Treat everything under `upstream/` as read-only. Do not edit the generated `space-cadet-theme.xml` directly.

## Development Workflow

When changing a stock MyBB component, copy it from the upstream split into the matching override directory and edit the copy:

```text
upstream/mybb-1.8.40/theme_parts/templates/header.xml
→ theme_overrides/templates/header.xml
```

Custom components can be created directly under `theme_overrides/`. If a file exists there, it should represent an intentional Space Cadet change.

Build the importable child theme after editing overrides:

```bash
python3 scripts/assemble_theme.py
```

The assembler includes theme properties, override stylesheets, and override templates only. All other components inherit from MyBB Master Style. Import `space-cadet-theme.xml` through **Admin CP → Templates & Style → Import a Theme** on a non-production forum.

The XML does not contain binary assets. Copy `images/space-cadet/` to the same path beneath the MyBB installation before testing or publishing. Font Awesome Free 6.4.0 is vendored under `images/space-cadet/fontawesome/`; retain its included `LICENSE.txt` when redistributing the theme.

To refresh the split upstream reference from the official XML:

```bash
python3 scripts/split_theme.py
```

This command deletes and recreates only `upstream/mybb-1.8.40/theme_parts/`; it does not modify `theme_overrides/`.

## Versioning

Project metadata lives in `theme.json`:

- `theme_version` is the Space Cadet release version and follows semantic versioning.
- `mybb_version` is MyBB's compatibility code. Keep it at `1840` while targeting MyBB 1.8.40.
- `name` and `output` control the generated theme name and filename.

## Testing

Confirm the generated XML parses and imports without warnings. Test guest/member sessions, forum and thread pages, profiles, private messages, moderation controls, and narrow screens. Re-import into a clean MyBB 1.8.40 test installation before publishing a release.

## License

The baseline derives from MyBB. Retain applicable MyBB copyright and license notices. Document the license for new Space Cadet code and assets before the first public release.
