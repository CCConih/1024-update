"""Rebuild preview/<page>.html from the kit files after you edit them.
Run from anywhere:  python build-preview.py
"""
import pathlib

kit = pathlib.Path(__file__).resolve().parent
out = kit / 'preview'
out.mkdir(exist_ok=True)
read = lambda n: (kit / n).read_text(encoding='utf-8')

PAGES = {  # preview file -> (page title, kit file)
    'index': ('Home', '02-home-hero.html'),
    'music': ('Music', '03-audio-release.html'),
    'videos': ('Videos', '04-music-videos.html'),
    'shows': ('Shows', '05-concerts-festivals.html'),
    'merch': ('Merch', '06-official-merch.html'),
    'postcards': ('Postcards', '07-postcard-from.html'),
    'news': ('News', '08-news-press.html'),
    'about': ('About', '09-about-hindia.html'),
}

# Preview only: the kit links to site pages like /music; locally those are music.html.
REWRITE = """<script>/* LOCAL PREVIEW ONLY: /music -> music.html */
document.querySelectorAll('a[href^="/"]:not([href^="//"])').forEach(function(a){
  var h = a.getAttribute("href"), i = h.indexOf("#"), path = i < 0 ? h : h.slice(0, i), hash = i < 0 ? "" : h.slice(i);
  a.setAttribute("href", (path === "/" ? "index" : path.slice(1)) + ".html" + hash);
});
</script>
"""

hdr = read('01-header-FOOTER-injection.html')
# Preview only: page addresses end in .html, the home video is a local copy, Music gets a test background.
liquid = (read('01c-liquid-bg-FOOTER-injection.html')
          .replace(r'var cfg = BACKGROUNDS[location.pathname.replace(/\/$/, "")]',
                   r'var cfg = BACKGROUNDS[location.pathname.replace(/(\/|\.html)$/, "")]')
          .replace('"/music":     { img: ""', '"/music":     { img: "test-bg.jpg"'))
cut = hdr.rindex('<script>')
wrap = lambda html: '<section class="page-section"><div class="content-wrapper">' + html + '</div></section>\n'

for name, (title, src) in PAGES.items():
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>Hindia — {title} (local preview)</title>\n'
            + read('00-global-HEADER-injection.html')
            + '</head><body>\n<!-- LOCAL PREVIEW ONLY. Not for Squarespace. -->\n'
            + wrap(read(src).replace('VIDEO_URL', 'home-video.mp4')) + wrap(read('10-footer.html'))
            + hdr[:cut] + REWRITE + hdr[cut:]
            + read('01b-guestbook-FOOTER-injection.html')
            + liquid
            + '</body></html>\n')
    (out / f'{name}.html').write_text(page, encoding='utf-8', newline='\n')
print('built', len(PAGES), 'pages in', out)
