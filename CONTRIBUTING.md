# Contributing to Space Cadet

Thanks for helping improve Space Cadet. This repository contains a MyBB 1.8.41 child theme maintained as focused overrides of MyBB Master Style. Contributions are welcome through issues and pull requests.

## How to Contribute

1. Search existing issues and pull requests before starting a change.
2. Fork the repository and clone your fork if you are contributing from outside the project. If you already have a checkout, use it.
3. Create a focused branch in a separate worktree, keeping the primary checkout on `main`:

   ```bash
   git worktree add -b feature/your-change ../space-cadet-your-change main
   ```

4. Make the smallest practical change that solves the issue.
5. Rebuild the theme and test the affected pages and controls in a MyBB test forum.
6. Commit with a clear message and reference the related issue when there is one.
7. Push your branch and open a pull request.

## Code Style

- Follow the style of the template or stylesheet you are editing. Use four spaces in Python and tabs inside template and stylesheet CDATA where consistent with the surrounding code.
- Preserve MyBB variables, template names, XML attributes, UTF-8 encoding, and CDATA wrappers.
- Keep build scripts dependency-free and changes compatible with MyBB 1.8.41.
- Preserve native MyBB permissions and actions when changing their presentation.
- Keep user-facing text clear and check keyboard focus, narrow layouts, and dropdown positioning for interface changes.
- Do not commit credentials, cookies, signing keys, database exports, production configuration, or private server addresses. Sanitize screenshots and logs before sharing them.

## Development Workflow

Use Python 3 to run the repository's dependency-free build scripts from the repository root. Treat `upstream/` as read-only and do not edit the generated `space-cadet-theme.xml` directly.

When changing a stock MyBB component, copy it from the upstream split into the matching override directory and edit the copy:

```text
upstream/mybb-1.8.41/theme_parts/templates/header.xml
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

## Refreshing the Upstream Reference

To refresh the split upstream reference from the official XML:

```bash
python3 scripts/split_theme.py
```

This command deletes and recreates only `upstream/mybb-1.8.41/theme_parts/`; it does not modify `theme_overrides/`. Use it only when refreshing the baseline.

## Versioning

Project metadata lives in `theme.json`:

- `theme_version` is the Space Cadet release version and follows semantic versioning.
- `mybb_version` is MyBB's compatibility code. Keep it at `1841` while targeting MyBB 1.8.41.
- `name` and `output` control the generated theme name and filename.

Record release changes in `CHANGELOG.md` and rebuild the XML after changing version metadata. Include the generated XML alongside its source overrides when committing theme changes.

## Issues

- Search existing issues before opening a new one.
- Include the theme and MyBB versions, affected page or control, reproduction steps, expected behavior, and actual behavior.
- For layout bugs, include the browser, viewport size, and a sanitized screenshot when possible. Mention whether resizing or scrolling triggers the problem.
- For permission-dependent controls, state whether you are a guest, member, moderator, or administrator and whether the affected content belongs to you or another user.

## Pull Requests

- Keep each pull request focused on one problem or related set of changes.
- Explain the user-visible behavior and reference the related issue.
- Include source overrides and the rebuilt `space-cadet-theme.xml` together.
- Mention the checks and manual testing performed, including relevant desktop and narrow-screen behavior.
- Call out compatibility changes, new assets, and anything that still needs live-forum verification.
- Retain third-party license files and the theme's required attribution.

## License

By contributing, you agree that your contributions will be licensed under this repository's [license](LICENSE), including its attribution-preservation terms.
