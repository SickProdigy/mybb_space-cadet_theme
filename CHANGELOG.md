# Changelog

## 1.0.4 - 2026-10-18

- Replaced the understated adjacent-thread text with dedicated Previous Thread and Next Thread buttons below the thread.
- Moved post reporting to a quick Report link beside each numbered post permalink and added permission-aware moderation shortcuts without removing MyBB's bulk inline moderation flow.
- Split the Moderate menu by context: the opening post mirrors available thread tools, while replies mirror available inline-post tools, including custom moderator tools.

## 1.0.3 - 2026-10-18

- Reworked Portal announcements with a right-side responsive sidebar, compact author identity, purple title accents, reverse gradient framing, Print, and client-side sharing.
- Refined thread view with Portal-inspired framing, compact top tools, per-post sharing, a plain opening-post Reply, and a Quick Quote/Quote Reply menu.
- Made thread sharing follow MyBB-generated friendly or dynamic links while retaining direct MyBB post permalinks.
- Moved forum and thread browsing activity into compact panels below their primary content and reply areas.
- Unified forum and subforum headings with the Space Cadet glow and gradient treatment.
- Restyled Help Documents as responsive reading panels with clearer typography and usable content tables.

## 1.0.2 - 2026-10-12

- Updated the theme baseline and import compatibility for MyBB 1.8.41.
- Restyled post attachments and separated attached images from downloadable files.
- Hid image attachment thumbnails only when the same attachment is embedded in its post.
- Replaced the attachment usage sentence with a responsive remaining-quota indicator that follows stock AJAX uploads and removals.
- Added accessible quota status colors and secured attachment links that open in new tabs.

## 1.0.1 - 2026-09-18

- Removed crawler-visible hidden moderation and account status text from postbit, forum thread row, and header templates.
- Kept visible moderation and account status labels through state-based CSS pseudo-elements.
- Consolidated the index activity panels into ten recent items and added an RSS fallback with thread creator names when Portal is unavailable.
- Rebuilt `space-cadet-theme.xml` for the 1.0.1 theme release.
