# Northia — Website

Interactive, trilingual (EN / 繁體中文 / 简体中文) marketing site for **Northia Marketing Consultancy**.
Static HTML/CSS/JS — no build step, no framework, no dependencies. Ready to host on GitHub Pages.

**Tagline:** Asia ⇄ Overseas | Branding & Community Consultancy that Helps Expanding New Markets & Communities

---

## What's in here

```
northia-website/
├── index.html              The whole site (HTML + CSS + JS in one file)
├── content.json            All wording, loaded by the site at runtime
├── content.xlsx            Editable copy deck → regenerates content.json
├── assets/
│   └── northia-mark.png     Compass logo mark
├── scripts/
│   └── build_content.py     Turns content.xlsx into content.json
├── .gitignore
└── README.md
```

The page renders from the copy **embedded in `index.html`** as a fallback, and — when
served over HTTP (GitHub Pages or a local server) — it loads `content.json` and uses that
instead. So you change wording by editing `content.xlsx`, not the code.

---

## Edit the wording (no coding)

1. Open **`content.xlsx`** and edit the text in the `EN`, `繁體中文`, `简体中文` columns.
   The **How to edit** sheet explains each sheet and the rules.
2. Regenerate the site copy:
   ```bash
   pip install openpyxl        # first time only
   python scripts/build_content.py
   ```
   This rewrites `content.json`.
3. Commit both `content.xlsx` and `content.json`.

Do **not** change the `Key`, `id`, `Variant`, `x`, `y`, or `slug` values — those wire copy
to the page. Only edit the text columns. Keep tags like `<br>` and `&amp;` intact.

> The `Variant` column: blank = one version shown everywhere. `a2w` = shown in the
> **Asia → World** view, `w2a` = shown in the **World → Asia** view.

---

## Preview locally

`content.json` only loads over HTTP (browsers block `fetch` from `file://`), so:

```bash
python -m http.server 8000
# open http://localhost:8000
```

Double-clicking `index.html` still works, but it will show the embedded fallback copy
rather than your latest `content.json` edits.

---

## Publish on GitHub Pages

1. Create a repo and push this folder:
   ```bash
   git init
   git add .
   git commit -m "Northia website"
   git branch -M main
   git remote add origin https://github.com/<you>/<repo>.git
   git push -u origin main
   ```
2. On GitHub: **Settings → Pages → Build and deployment → Source: Deploy from a branch**,
   pick **main** / **/ (root)**, Save.
3. Your site goes live at `https://<you>.github.io/<repo>/` in a minute or two.

For a custom domain (e.g. `northiamarketing.com`), add it under Settings → Pages and set
the DNS records GitHub shows you.

---

## Forms (audit / consultation / KOL / service request)

All form submissions post to **hello@northiamarketing.com** via
[FormSubmit](https://formsubmit.co) — a no-backend relay that works on static hosting.

**One-time activation:** the *first* time any form is submitted, FormSubmit emails
hello@northiamarketing.com a confirmation link. Click it once and submissions flow
automatically after that.

To change the destination address, edit this line near the top of the `<script>` in
`index.html`:

```js
const ENDPOINT='https://formsubmit.co/ajax/hello@northiamarketing.com';
```

**Want submissions in a Google Sheet instead?** Replace that endpoint with a Google
Apps Script Web App URL (deployed as “Anyone”) that appends the posted fields to a sheet.

---

## Notes

- Fonts (Plus Jakarta Sans + Noto Sans TC/SC) load from Google Fonts.
- The world map is a stylised SVG (positions are illustrative, not to scale).
- Placeholder frames — logo slots, `[ Photo ]`, `[ Asset slot ]`, and bracketed quotes —
  are intentional. Replace them with approved logos, portraits, results and quotes only.
- Logo lockup note: the supplied stacked lockup art reads “Marke**r**ting” (a typo in the
  source artwork) — worth fixing that file before print/production use.

© 2026 Northia Marketing Consultancy Ltd.
