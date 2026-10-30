# VPN-Pick.com

A bilingual (English / Swedish) VPN comparison site that ranks providers using
affiliate programmes. Static HTML, CSS and vanilla JavaScript — no framework, no
build toolchain, no runtime dependencies.

```
en/            44 English pages
sv/            44 Swedish pages (same structure, translated, separate URLs)
assets/
  css/         one stylesheet, dark + light
  js/          progressive enhancement only
  data/        providers.json + affiliates.json + topics.json + explained.json  <- the source of truth
  img/         icon sprite, logo artwork, social image
  logos/       source logo artwork (VPN-Pick logotyp.png + provider logos)
tools/
  build.py     regenerates every page from the data files
  check.py     pre-launch validator
index.html     language picker at the site root
```

## Quick start

```bash
python3 tools/build.py      # generate the site
python3 tools/check.py      # validate it (--draft to skip the go-live gates)
python3 -m http.server 8000 # preview at http://localhost:8000
```

Python 3.9+ is the only requirement. Nothing else is needed to run the site.

## How it fits together

`assets/data/providers.json` is the single source of truth. Every price, server
count, audit name and score lives there. `build.py` reads it and renders both
language versions of all 88 pages, so the English and Swedish sites cannot drift
apart and no fact can be stated on one page but forgotten on another.

**Change the data, not the pages.** Adding a provider means adding one object to
`providers.json` and re-running the build.

```
providers.json  ──►  build.py  ──►  en/*.html + sv/*.html  ──►  check.py  ──►  deploy
     (facts)              (pages)        (two languages)        (gates)
```

## Go-live checklist

The build will not let you deploy with placeholder data. Work through this:

### 1. Affiliate links

Open `assets/data/affiliates.json` and replace every `"url": "PLACEHOLDER_..."`
with your real tracking link from Impact, CJ, Awin, Tradedoubler or the
provider's in-house programme. Set `lastChecked` to today's date.

While a URL is still a placeholder the site renders a plain outbound link to the
provider's own homepage and marks it as non-commercial, so it is fully browsable
and never claims a commission it has not earned.

### 2. Advertiser identity

Edit the `SITE` block at the top of `tools/build.py`:

```python
"origin":     "https://vpn-pick.com",
"legal_name": "Daniel Vilhelmsson",
"email":      "daniel@vpn-pick.com",
"address":    "Tessingatan 1C, 46141 Trollhättan",
```

Swedish marketing law (marknadsföringslagen 4 §) requires that a consumer can
identify who is behind the advertising and how to reach them. This block is
printed in the footer of all 88 pages and on the about page. The validator
checks name, address, email and a `mailto:` link on every page.

### 3. Verify the check passes

```bash
python3 tools/build.py && python3 tools/check.py
```

Zero errors means ready to deploy. Run with `--strict` to also fail on warnings.

### 4. Deploy

Static output, so any of these work with no configuration:

- **Cloudflare Pages** — build command `python3 tools/build.py`, output directory `.`
- **Netlify** — build command `python3 tools/build.py`, publish directory `.`
- **GitHub Pages** — push, then Pages serves from the branch root

`_headers` already sets cache rules, HSTS, a Content-Security-Policy and
`X-Content-Type-Options`. `_redirects` normalises `/en` to `/en/`.

## What the validator enforces

`check.py` runs 27 checks and refuses to pass while any of these fail:

| Check | Why it matters |
|---|---|
| Internal links and `#fragments` resolve | Broken links lose rankings and trust |
| Every page has a counterpart in the other language | Orphaned translations |
| `hreflang` correct, `x-default` matches a real alternate | Hreflang must be reciprocal |
| Exactly one `<h1>`, no skipped heading levels, balanced tags, unique ids | Accessibility + SEO |
| `<meta name="description">` on every page | Search snippets |
| No double-escaped entities (`&amp;#x27;`) | Escaping twice shows markup to readers |
| `target="_blank"` always carries `rel="noopener"` | Reverse tabnabbing |
| Outbound `rel`/`data-affiliate` match the real link type | Never claim commission on a plain link |
| Sortable headers and sort options have a matching cell whose values differ | Sorting that silently does nothing |
| `#` column reads 1..N straight down the table | The ranking must be the score order the weights produce |
| Use-case links deep-link to a filter that exists | The "start from what you need" tiles |
| JSON-LD parses | Rich results break silently on bad JSON |
| Disclosure bar on any page with a commercial link | **Legal requirement** |
| An "Ad"/"Annons" label next to *every* commercial link | **Legal requirement** |
| Advertiser identification in the footer (name, email, address) | **Legal requirement** |
| No `PLACEHOLDER_` affiliate URLs | No dead links at launch |
| No `__REPLACE` identity strings | **Legal requirement** |
| Prices quote a total, not just a monthly rate | **marknadsföringslagen 10 §** |
| Currency follows the page language (English USD only, Swedish SEK + converted USD) | SEK on an English page makes the reader do the exchange rate |
| No unmeasured Mbps/ping figures anywhere | The site claims not to benchmark |
| CSS classes used in HTML all exist in `site.css` | Catches styling that does nothing |
| Score rings carry their SVG dash values and `site.css` leaves them alone | A gauge that silently draws a full circle |
| Every review draws one score line per weighted category, at the right length | An inline `<span>` sizes nothing: empty grey tracks |
| Icon references all resolve to a defined symbol | Catches blank icons |
| Every referenced asset and sitemap entry exists | Missing asset = unstyled page |
| AdSense account script in every page `<head>`, CSP permits its hosts | Google verifies the site by fetching the tag; a blocking CSP makes it dead markup |
| Google tag (gtag.js) in every page `<head>` with consent-denied defaults, CSP permits its hosts, banner lifts analytics on accept | Analytics without prior consent breaks GDPR and our own cookie policy |
| Root language picker: favicon, theme, `noindex` | First URL a visitor can hit |
| Money pages: picks are real providers, criteria sum to 100, clean folder canonicals, hub linked from every page | The `/best-vpn-for/` section is three files that must agree: picks, copy and URL |
| Copy carries no uncheckable superlative (`in the industry`, `fastest`, `more than any other provider`) | The speed score is an estimate and the table covers eleven providers, so industry-wide claims cannot be defended |
| Explainers: slug/icon/date valid, both languages present and structurally mirrored, 750-1500 words, link tokens resolve, hub links every article and every page links the hub, `Article` + `FAQPage` + `BreadcrumbList` JSON-LD, clean folder canonicals | `/vpn-explained/` is one JSON file holding both languages, so drift or a broken token fails the build |

## Scoring model

Published in full on `/how-we-test.html` and `/sv/how-we-test.html`, because
Swedish law requires comparison services to disclose ranking criteria and their
relative weight.

| Component | Weight |
|---|---|
| Privacy and logging | 30 % |
| Speed and reliability | 25 % |
| Value for money | 20 % |
| Streaming and TV unblocking | 15 % |
| Apps and ease of use | 10 % |

Weights live in `providers.json` under `_meta.scoringModel.weights` and sum to
1.0 (the checker enforces this). `weighted_score()` in `render.py` is the only
place the calculation exists, so the cards, tables, rings and JSON-LD can never
disagree.

**We have not run our own throughput benchmarks.** The speed score is a disclosed
architectural estimate, and every review says so. If you later add real
benchmarks, set `"speedTestedByUs": true` on that provider, replace the estimate
text in `REVIEW`/`_meta.benchmarking`, and the validator will stop flagging the
situation.

## Editing content

| What | Where |
|---|---|
| Interface strings (labels, buttons, table headers) | `S` in `tools/content.py` |
| Page prose (home, compare, methodology, about, FAQ) | `HOME`, `COMPARE`, `HOW_WE_TEST`, `ABOUT`, `FAQ_GENERAL` in `tools/content.py` |
| Legal pages | `LEGAL` in `tools/content.py` |
| Provider facts, prices, scores, pros and cons | `assets/data/providers.json` |
| Affiliate URLs and terms | `assets/data/affiliates.json` |
| Colours, spacing, components | `assets/css/site.css` |
| Design tokens at the top of `site.css` | `Dark palette` / `Light palette` blocks |

Every string in `S` needs both `en` and `sv`. The checker does not verify this
directly, so when you add a key, add both languages in the same edit.

## Design system

Dark by default with a full light theme, both driven by CSS custom properties
and switched by `[data-theme]`. The theme choice persists in `localStorage`.

```css
--c-accent   accent colour      --r-md   10px radius
--c-gold     rank-1 highlight   --s-4    16px spacing step
--c-good     positive signal    --maxw   1200px content width
--c-warn     caution            --maxw-prose  68ch reading measure
```

- Provider logos are the vendors' own marks in `assets/logos/`, shown
  nominatively to identify the service being compared (the terms page states no
  ownership is claimed). Each sits on a light plate so dark ink survives the
  dark theme; a letter-badge fallback in code covers any provider without a
  logo file.
- All icons come from one inlined sprite (`assets/img/icons.svg`), so there is no
  extra network request and no icon-font dependency.
- Accessibility: skip link, landmarks, focus-visible rings, `<details>`-based
  FAQ, real `<table>` markup, `aria-sort` on sortable headers, colour contrast
  checked in both themes.
- Respects `prefers-reduced-motion` and `prefers-color-scheme`, and prints
  cleanly (the comparison table and price tables survive a print-out).
- Fully usable with JavaScript disabled. The comparison table renders as a
  complete server-side `<table>`; JS only adds filtering and sorting.

## Privacy posture

Deliberately minimal, because the site is about privacy:

- Display advertising via Google AdSense (account script in `<head>`, ad slots
  placed separately). Google is an independent controller for ad data; our own
  cookies stay opt-in as below.
- Analytics is Google Analytics behind Consent Mode: denied and cookieless
  until the visitor accepts in the banner; no tracking pixels of our own,
  no fingerprinting.
- One strictly-necessary first-party cookie for the consent choice.
- Consent banner defaults to off for our own cookies; Google's ad consent is
  governed by Google's own signalling (non-personalised ads without consent).
  For EEA visitors, enable Google Funding Choices in the AdSense account.
- Local storage is used only for theme and sort preference, never transmitted.
- Full policy in `LEGAL['privacy']`, ad details in `LEGAL['cookies']`.

If you later add analytics, add it to `LEGAL['cookies']` at the same time.

## Content and accuracy policy

- Only facts traceable to a provider's own documentation or a named audit go into
  `providers.json`.
- Where something is not published, the field is `null` and renders as "not
  published" rather than being estimated.
- Server counts and prices are the providers' own published figures, dated.
- Every price on every page carries the date it was last verified.
- Corrections are made in place and dated, never silently deleted.

Suggested re-verification rhythm: prices monthly, audit and ownership facts
quarterly, and immediately when a provider announces a change.