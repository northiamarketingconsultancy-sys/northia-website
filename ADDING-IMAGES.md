# Adding & replacing images

The site now has a real asset folder. Photos and logos are wired in through a small
map in `index.html` — so adding a picture is: **drop the file in a folder, then add one line.**

## Folder structure

```
assets/
├── northia-mark.png          the compass logo (header, footer, watermark)
├── partners/                 partner + client logos
│   ├── liuyishou-hotpot.png
│   ├── winggrove.png
│   └── excohk.png
└── team/                     founder / team photos
    └── maureen-ng.jpg
├── about/
│   └── northia-why-exists.png
```

## What's already wired

| Image | Where it shows |
|---|---|
| `partners/winggrove.png` | logo carousel + WingGrove proof card |
| `partners/liuyishou-hotpot.png` | logo carousel + Liuyishou proof card |
| `partners/excohk.png` | logo carousel + excohk proof card |
| `about/northia-why-exists.png` | "Why Northia exists" feature image |
| `team/maureen-ng.jpg` | Maureen's founder card |

Anything not yet supplied (the **4evercare** logo, **Aka Chung**'s photo) keeps a dashed
placeholder until you add it.

---

## How to add a partner / client logo

1. Save the logo into `assets/partners/`. Use a lowercase, hyphenated name, e.g.
   `4evercare.png`. **Transparent PNG** is best; aim for roughly 400–800 px wide.
2. Open `index.html`, find the `ASSETS` block near the top of the `<script>`:

   ```js
   const ASSETS={
     partners:{
       'Liuyishou Hotpot':'assets/partners/liuyishou-hotpot.png',
       'WingGrove':'assets/partners/winggrove.png',
       'excohk':'assets/partners/excohk.png'
     },
     ...
   ```
3. Add one line, matching the partner name **exactly** as it appears in the deck's
   Partners sheet:

   ```js
   '4evercare':'assets/partners/4evercare.png'
   ```
   (Remember a comma after the line above it.)

That's it — the logo now shows in the carousel. To show it in the **proof card** too,
find the `4evercare` proof card in `index.html` and swap its placeholder:

```html
<!-- from -->
<div class="proof-asset" data-i18n="tst.pic">[ Photo ]</div>
<!-- to -->
<div class="proof-asset has-img"><img src="assets/partners/4evercare.png" alt="4evercare"></div>
```

## How to add / replace a founder photo

1. Save the photo into `assets/team/` (e.g. `aka-chung.jpg`). A portrait crop around
   760 px wide is plenty; JPG keeps the file small.
2. In the same `ASSETS` block, under `founders`, add:

   ```js
   'Aka Chung':'assets/team/aka-chung.jpg'
   ```
3. To put Aka's photo on her founder card, find her card in `index.html` and swap:

   ```html
   <!-- from -->
   <div class="pf" data-i18n="about.photo">[ Photo ]</div>
   <!-- to -->
   <div class="pf has-img"><img src="assets/team/aka-chung.jpg" alt="Aka Chung"></div>
   ```

To **replace** Maureen's photo, just overwrite `assets/team/maureen-ng.jpg` with a new
file of the same name — no code change needed.

---

## Notes

- **Why these live in code, not the Excel deck:** the deck (`content.xlsx`) controls
  *wording*. Images are wired in `index.html` so they load fast and reliably. The two are
  independent — editing copy won't touch your images, and vice-versa.
- **Formats:** logos → transparent PNG (or SVG); photos → JPG. Keep photos under ~300 KB
  so pages stay fast (Maureen's was resized from 1.8 MB to ~75 KB).
- **Alt text:** the `alt="…"` on each image is read by screen readers and search engines —
  keep it as the brand or person's name.
- **Preview:** run `python -m http.server` and open `http://localhost:8000`; images load
  over http (double-clicking the file also works for images).
