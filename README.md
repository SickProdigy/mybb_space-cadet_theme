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
├── fontawesome/             # self-hosted Font Awesome Free Solid and Brands assets
└── fonts/droid-sans/        # local Droid Sans webfonts and Apache 2.0 license
scripts/
├── split_theme.py
└── assemble_theme.py
theme.json                  # project and compatibility metadata
space-cadet-theme.xml       # generated minimal import file
```

Treat everything under `upstream/` as read-only. Do not edit the generated `space-cadet-theme.xml` directly.

## Installation

Space Cadet requires MyBB 1.8.40. Use the generated `space-cadet-theme.xml` for the theme import; do not import the upstream XML or individual override fragments.

1. Copy the repository's `images/space-cadet/` directory to `images/space-cadet/` under the MyBB forum root. Keep the included Font Awesome and Droid Sans files in their existing subdirectories.
2. In MyBB Admin CP, open **Templates & Style → Themes → Import a Theme**.
3. Select `space-cadet-theme.xml`, give the theme a name if desired, and import it. Leave **Ignore Version Compatibility** disabled when installing on MyBB 1.8.40.
4. Set Space Cadet as the default theme or select it for the test account under **User CP → Edit Options**.
5. Confirm the imported theme inherits unchanged components from **MyBB Master Style**. Do not detach or copy all master templates into Space Cadet.
6. Hard-refresh the browser and clear any proxy/CDN cache, then test the index, forum and thread listings, search results, member list and profiles, calendar views, private messages, and moderation pages on desktop and mobile.

For upgrades, replace `images/space-cadet/` with the release assets and import the new generated XML. Test upgrades on a non-production forum first; importing may create a separate theme instead of overwriting an existing customized installation.

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
python3 -c "import xml.etree.ElementTree as ET; ET.parse('space-cadet-theme.xml')"
git diff --check
```

The first command assembles the release; the next two validate its XML and check for whitespace errors. The assembler includes theme properties, override stylesheets, and override templates only. All other components inherit from MyBB Master Style. Import `space-cadet-theme.xml` through **Admin CP → Templates & Style → Import a Theme** on a non-production forum.

The XML does not contain binary assets. Copy `images/space-cadet/` to the same path beneath the MyBB installation before testing or publishing. Font Awesome Free 6.4.0 assets are vendored under `images/space-cadet/fontawesome/`, and Droid Sans webfonts are under `images/space-cadet/fonts/droid-sans/`. Retain both included license files when redistributing the theme.

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

Confirm the generated XML parses and imports without warnings. Test guest/member sessions, forum and thread listings, search and help results, member lists and profiles, monthly and weekly calendars, private messages, moderation controls, header dropdowns, and post actions. Check desktop, narrow desktop browser windows, tablet, and phone widths, including menus and controls near viewport edges. Re-import into a clean MyBB 1.8.40 test installation before publishing a release.

## Texture Credits

The optional repeating background textures under `images/space-cadet/backgrounds/` are sourced from Transparent Textures and used under the Creative Commons Attribution 3.0 license:

- `black-felt.png` by E. van Zummeren
- `scbg.png` by Atle Mo
- `asfalt-dark.png` by Atle Mo
- `tactile-noise-dark.png` by Atle Mo
- `dark-geometric.png` by Mike Warner
- `dark-matter.png` by Atle Mo
- `graphy-dark.png` by We Are Pixel8
- `shattered-dark.png` by Luuk van Baars
- `diagmonds.png` by INS
- `hexellence.png` by Kim Ruddock

Source: https://www.transparenttextures.com/
License: https://creativecommons.org/licenses/by/3.0/

## License

The baseline derives from MyBB. Retain applicable MyBB copyright and license notices. Document the license for new Space Cadet code and assets before the first public release.
