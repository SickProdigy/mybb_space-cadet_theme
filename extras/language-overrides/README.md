# Optional Space Cadet Help text

The English example updates profile navigation, login/logout, new threads and
replies for Space Cadet. Importing the theme XML does not install this resource.

1. Back up `inc/languages/english/customhelpdocs.lang.php` in your forum.
2. Check **Admin CP → Configuration → Help Documents**: the example assumes
   default IDs 2 (profile), 4 (login), 5 (new thread), and 6 (reply). Adjust the
   `d{ID}_name`, `d{ID}_desc`, and `d{ID}_document` keys to your local IDs.
3. Review `english/customhelpdocs.space-cadet.example.php` and merge only the
   desired assignments into your existing `customhelpdocs.lang.php`. Keep one
   opening PHP tag; replace any matching assignments deliberately and preserve
   unrelated phrases. Never upload the example over the existing customization
   file or change stock `helpdocs.lang.php`.
4. Adapt wording to enabled controls and test the public Help pages. This language
   customization applies to all themes using that language, so review wording if
   your forum offers other themes.

For translations, merge translated assignments into that language's own
`customhelpdocs.lang.php`. MyBB loads stock `helpdocs` and `helpsections` before
`customhelpdocs` and `customhelpsections`, allowing these phrases to override
stock text. The corresponding documents must use translation-backed content.

For documents with `usetranslation=1`, MyBB's AdminCP editor displays fallback
text from the database, rather than the effective language phrases, and submits
`usetranslation` as a hidden field. Saving fallback text may therefore leave the
public page unchanged without a warning. Edit the custom language phrases for
these documents. This is a MyBB editor limitation; this resource changes no core
files or database flags.

After theme upgrades, compare the example with your merged phrases, review any
changed controls, and merge intentionally. Keep your backup and local wording;
never overwrite custom phrases automatically. Check language customizations again
after MyBB or language-pack upgrades.
