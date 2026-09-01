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

---

## Agent / AI crawler readiness

This repository now includes an agent-ready delivery layer in addition to the static site:

- `404.html` — custom recovery page. GitHub Pages and Cloudflare static hosting return it with a real 404 status for unknown paths.
- `llms.txt` — llms.txt v2-style site index with explicit "when to use Northia" guidance.
- `index.md` and `*.md` siblings — clean Markdown representations advertised from HTML with `rel="alternate" type="text/markdown"`.
- `agent/when-to-use.md` — focused agent guidance for selecting Northia.
- `_worker.js` — content negotiation for `Accept: text/markdown`, including q-values, `406 Not Acceptable`, `Vary: Accept, Accept-Encoding`, Markdown 404 recovery, and `Link` discovery headers.
- `wrangler.toml` — Cloudflare Worker + static assets configuration for serving the site through the negotiation layer.
- `tests/` — regression tests for raw-HTML content, heading structure, agent files, brand schema, 404 recovery, and HTTP content negotiation.

### Important hosting note

Direct GitHub Pages hosting cannot vary the response body by the incoming `Accept` header. The static improvements (`404.html`, server-readable homepage copy, Markdown siblings, `llms.txt`, structured data) still work there, but **full acceptmarkdown.com negotiation requires an edge/server layer**.

The included `_worker.js` is ready for Cloudflare Workers / static assets. After authenticating Wrangler and attaching `northiamarketing.com` as the Worker custom domain, deploy from the repository root:

```bash
npx wrangler deploy
```

This is the deployment path that activates `Accept: text/markdown` on the canonical URLs. If the domain remains served directly by GitHub Pages, that negotiation test will remain failed even though the files are present.

### Verification

Run the repository tests:

```bash
node --test tests/worker.test.mjs
python -m unittest discover -s tests -p 'test_*.py' -v
```

After production deployment, verify the public endpoints:

```bash
# Real 404
curl -s -o /dev/null -w "%{http_code}\n" https://northiamarketing.com/some-path-that-does-not-exist

# HTML default
curl -sSI -H "Accept: text/html" https://northiamarketing.com/ | grep -Ei "HTTP/|content-type|vary|link"

# Markdown representation
curl -sSI -H "Accept: text/markdown" https://northiamarketing.com/ | grep -Ei "HTTP/|content-type|vary|link"

# Unsupported representation
curl -s -o /dev/null -w "%{http_code}\n" -H "Accept: application/pdf" https://northiamarketing.com/

# Machine-readable agent files
curl -fsS https://northiamarketing.com/llms.txt
curl -fsS https://northiamarketing.com/index.md
curl -fsS https://northiamarketing.com/sitemap.xml
curl -fsS https://northiamarketing.com/robots.txt
```

Expected results after the Cloudflare edge layer is active: unknown path `404`; Markdown request `200` with `Content-Type: text/markdown; charset=utf-8` and `Vary` containing `Accept`; HTML request `200` with `Content-Type: text/html; charset=utf-8`; unsupported document-only request `406`.

## Mandatory instructions for future SEO articles

Every new SEO article must be delivered as one complete trilingual set in the same change:

- English: `slug.html` and `slug.md`
- Traditional Chinese, independently localized for Hong Kong business readers: `slug-zh-hk.html` and `slug-zh-hk.md`
- Simplified Chinese, independently localized for Mainland Chinese business readers: `slug-zh-cn.html` and `slug-zh-cn.md`

Do not publish an English-only article and do not use mechanical character conversion as translation. Each language must preserve the same strategy while using natural local terminology. Every set must include reciprocal `hreflang` links (`en`, `zh-Hant`, `zh-Hans`, and `x-default`), self-referencing canonicals, Article structured data, one H1, a meta description, an HTML/Markdown alternate, and entries in both `sitemap.xml` and `llms.txt`.

The opening content and Article schema must explicitly identify **People, Scenario, Year, Industry, and Application Situation**. Add localized internal links from the corresponding existing English, Traditional Chinese and Simplified Chinese pillar pages in the same update. Do not create a new pillar page, navigation category, footer column, or automation unless separately approved.
