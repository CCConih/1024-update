# Hindia 1024 — Squarespace custom code kit (multi-page)

Plan note: Code Injection and code blocks that run JavaScript need a Squarespace plan above Personal.

The site is split into separate pages, like an artist site with its own page per menu item:
the home page is one full-window video, and Music, Videos, Shows, Merch, Postcards, News and About
each have their own page.

## Site-wide code (every page)

| File | Where it goes |
|---|---|
| `00-global-HEADER-injection.html` | Settings → Advanced → Code Injection → **Header** |
| `01-header-FOOTER-injection.html` | Settings → Advanced → Code Injection → **Footer** (hides the native header) |
| `01b-guestbook-FOOTER-injection.html` | Same **Footer** box, pasted right after 01 (guest book pop-up on every page) |
| `01c-liquid-bg-FOOTER-injection.html` | Same **Footer** box, pasted after 01b (liquid background) |
| `10-footer.html` | Edit **site footer** → Code Block |
| `guestbook-apps-script.gs` | Google Sheet → Extensions → Apps Script (deploy as Web app) |

## Pages

Create these in **Pages**, each with the URL slug shown (Page settings → URL slug).
Each page gets one blank section with one Code Block holding the file.

| Page | URL slug | File |
|---|---|---|
| Home | (homepage) | `02-home-hero.html` |
| Music | `/music` | `03-audio-release.html` |
| Videos | `/videos` | `04-music-videos.html` |
| Shows | `/shows` | `05-concerts-festivals.html` |
| Merch | `/merch` | `06-official-merch.html` |
| Postcards | `/postcards` | `07-postcard-from.html` |
| News | `/news` | `08-news-press.html` |
| About | `/about` | `09-about-hindia.html` |

**Postcards blog:** the Postcards page reads posts from a Squarespace **Blog** page. Because the Postcards
page already uses `/postcards`, give the blog its own slug, `/letters` (that's the default `BLOG_PATH` in 07),
and keep it out of the navigation. Posts open at `/letters/post-name`.

The menu, footer and home "Listen now" button link to these slugs. If you change a slug,
search the files for the old one (e.g. `/music`) and change it there too.

## Section setup (each page's code block)

1. Add a blank section, add one Code Block, stretch it across the full grid width.
2. Section Color Theme doesn't matter; the kit paints the section dark itself.
3. In the Code Block, turn **Display source** off.
4. The global CSS strips Squarespace's section padding automatically (`:has()` selector).

## The look: dark framed window

The whole site sits inside a dark, rounded "window". The logo hangs from the top bar in a tab,
the menu runs along the top right (a Menu button on phones) and underlines the page you're on,
and a short logo loader shows while each page loads.

**Every colour, font and size of the look is in the `:root` block at the top of `00-global-HEADER-injection.html`**
(`--hx-frame`, `--hx-bg`, `--hx-surface`, `--hx-text`, `--hx-heading`, `--hx-accent`, `--hx-font`, frame and corner sizes).
Change them there; Squarespace's Site Styles and section Color Themes no longer affect these blocks.
The font is Archivo from Google Fonts, loaded by the same file.

## Liquid background

Like linkinpark.com, the background slowly ripples like liquid (WebGL, in `01c`).

- **Home:** uses the home video (`VIDEO_URL` in 02). Upload the MP4 as a Squarespace file
  (add a link → File → upload, 20 MB max). The effect needs a host that allows cross-site use,
  and Squarespace's does.
- **Other pages:** set one image per page in `BACKGROUNDS` at the top of 01c
  (desktop 2560×1440 under ~500 KB, optional phone crop 1080×1920 under ~250 KB).
  A page left `""` keeps the plain dark background.
- `DIM_PAGES` darkens page images so text stays readable; `AMOUNT` sets how strong the ripple is.
- Visitors with no WebGL, or who asked for reduced motion, get the still image / plain video.
- Also part of the look: content comes into focus as each page loads (00), and the phone menu
  and guest book blur the page behind them (frosted glass).

## What to fill in (search for these placeholders)

`LOGO_1024_URL`, `LOGO_HINDIA_URL`, `VIDEO_URL`, `POSTER_URL`, `PRIVACY_URL`,
`RELEASE_COVER_URL`, `RELEASE_TITLE`, `FOLLOW_URL` (home release card and Follow button),
`GUESTBOOK_ENDPOINT` (in 01b), page images in `BACKGROUNDS` (01c), `SPOTIFY_ALBUM_ID`, `YOUTUBE_ID_*`, `YOUTUBE_CHANNEL_URL`,
`BIT_APP_ID`, `STORE_URL`, `KV_IMAGE_URL`, `BLOG_PATH`, `ARCHIVE_URL`, `PHOTO_URL`,
platform URLs in About, press/booking emails.

## Language toggle

Static text uses `data-en` / `data-id` attributes. Data lists accept `{en:"…", id:"…"}`
wherever a label is shown. The choice is remembered per visitor, across pages.

## Guest book link

Add `#guestbook` to any page address (e.g. `hindia1024.com/#guestbook`) to open the guest book directly —
good for IG bio links.

## Local preview

Open `preview/index.html` in a browser and click through the menu. It's built from the files above,
so after editing any of them, rebuild it with:

    python build-preview.py

Not for Squarespace.
