#!/usr/bin/env python3
"""
check.py — pre-launch validator for the generated site.

    python3 tools/check.py            # run every check
    python3 tools/check.py --strict    # also fail on warnings

Exit code 0 = safe to deploy. Non-zero = do not deploy yet.

This script exists to make the boring, easy-to-forget requirements
mechanical: no broken links, no orphaned translations, no unlabelled
affiliate link, no invented speed number, no unfilled placeholder.
"""

from __future__ import annotations

import html
import json
import math
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urldefrag, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCALES = ("en", "sv")

errors: list[str] = []
warnings: list[str] = []
checks_run = 0


# In --draft mode the two deliberate pre-launch gates (unfilled affiliate
# URLs and unfilled advertiser identity) are downgraded to warnings so the
# rest of the report can be read on its own.
DRAFT = False


def err(msg: str) -> None:
    if DRAFT and ("PLACEHOLDER" in msg or "__REPLACE" in msg
                  or "no live affiliate link" in msg or "plain URL" in msg):
        warnings.append(msg)
        return
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


# ---------------------------------------------------------------------------
# Tiny HTML inspector
# ---------------------------------------------------------------------------


class Inspector(HTMLParser):
    """Collects the facts we need to verify, in one streaming pass."""

    HEADINGS = ("h1", "h2", "h3", "h4", "h5", "h6")

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links: list[dict] = []
        self.imgs_alt_missing: list[str] = []
        self.imgs: list[str] = []
        self.jsonld: list[str] = []
        self.ids: set[str] = set()
        self.id_dupes: list[str] = []
        self.lang: str | None = None
        self.canonical: str | None = None
        self.hreflangs: dict[str, str] = {}
        self.title: str = ""
        self.h1_count = 0
        self.h_levels: list[int] = []
        self.meta_description: str | None = None
        self._capture: str | None = None
        self._buf: list[str] = []
        self.tables_without_caption = 0
        self.has_main = False
        self.external_noopener: list[str] = []
        self.bad_attrs: list[str] = []
        self.heading_stack: list[str] = []
        self.heading_errors: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)

        for name, _value in attrs:
            if name and ('"' in name or "'" in name or ">" in name):
                self.bad_attrs.append(name)
        if tag in self.HEADINGS:
            self.heading_stack.append(tag)

        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "link":
            rel = (a.get("rel") or "").lower()
            if rel == "canonical":
                self.canonical = a.get("href")
            elif rel == "alternate" and a.get("hreflang"):
                self.hreflangs[a["hreflang"]] = a.get("href") or ""
        elif tag == "meta":
            if (a.get("name") or "").lower() == "description":
                self.meta_description = a.get("content")
        elif tag == "a":
            self.links.append({
                "href": a.get("href") or "",
                "rel": (a.get("rel") or "").lower(),
                "target": a.get("target"),
            })
            if a.get("target") == "_blank" and "noopener" not in (a.get("rel") or ""):
                self.external_noopener.append(a.get("href") or "")
        elif tag == "img":
            self.imgs.append(a.get("src") or "")
            if a.get("alt") is None:
                self.imgs_alt_missing.append(a.get("src") or "?")
        elif tag == "main":
            self.has_main = True
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.h_levels.append(int(tag[1]))
            if tag == "h1":
                self.h1_count += 1
        if a.get("id"):
            if a["id"] in self.ids:
                self.id_dupes.append(a["id"])
            self.ids.add(a["id"])

        if tag == "script" and (a.get("type") or "") == "application/ld+json":
            self._capture = "jsonld"
            self._buf = []

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag == "script" and self._capture == "jsonld":
            self.jsonld.append("".join(self._buf))
            self._capture = None
        if tag in self.HEADINGS:
            if self.heading_stack and self.heading_stack[-1] == tag:
                self.heading_stack.pop()
            else:
                open_tag = self.heading_stack[-1] if self.heading_stack else "nothing"
                self.heading_errors.append(f"</{tag}> closes {open_tag}")

    def handle_data(self, data):
        if self._capture == "jsonld":
            self._buf.append(data)
        if self._capture is None and not self.ids:
            pass

    def text(self):
        return "".join(self._buf)


def title_of(markup: str) -> str:
    m = re.search(r"<title>(.*?)</title>", markup, re.S | re.I)
    return m.group(1).strip() if m else ""


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


def all_pages() -> list[str]:
    pages = []
    for lang in LOCALES:
        for base, _dirs, files in os.walk(os.path.join(ROOT, lang)):
            for f in files:
                if f.endswith(".html"):
                    pages.append(os.path.relpath(os.path.join(base, f), ROOT))
    return sorted(pages)


def resolve(page_rel: str, href: str) -> str | None:
    """Resolve a relative href from a page to a repo-relative file, or None."""
    href = urldefrag(href)[0]
    href = href.split("?", 1)[0]   # ?use=... filter links point at a real file
    if not href or href.startswith(("http://", "https://", "mailto:", "tel:", "data:", "//")):
        return None
    page_dir = os.path.dirname(page_rel)
    target = os.path.normpath(os.path.join(page_dir, href))
    if target.startswith(".."):
        return None
    # Directory URL -> index.html
    if target.endswith(os.sep) or target == "":
        target = os.path.join(target, "index.html")
    elif not os.path.splitext(target)[1]:
        target = os.path.join(target, "index.html")
    return target.replace(os.sep, "/")


def check_internal_links(pages: list[str], parsed: dict) -> None:
    global checks_run
    checks_run += 1
    existing = set(pages) | {"index.html"}
    for page in pages:
        for link in parsed[page].links:
            href = link["href"]
            if not href:
                err(f"{page}: empty href")
                continue
            target = resolve(page, href)
            if target is None:
                # A pure "#fragment" link stays on this page
                if href.startswith("#") and len(href) > 1:
                    frag = urldefrag(href).fragment
                    if frag and frag not in parsed[page].ids:
                        err(f"{page}: link to #{frag} but no element has that id")
                continue
            if target not in existing:
                err(f"{page}: broken internal link -> {href}")
                continue
            frag = urldefrag(href).fragment
            if frag and target in parsed and frag not in parsed[target].ids:
                err(f"{page}: link to {href} but {target} has no id=\"{frag}\"")


def check_locale_pairs(pages: list[str]) -> None:
    """Every EN page must have an SV twin and vice versa."""
    global checks_run
    checks_run += 1
    page_set = set(pages)
    for page in pages:
        lang, rel = page.split("/", 1)
        other = "sv" if lang == "en" else "en"
        twin = f"{other}/{rel}"
        if twin not in page_set:
            err(f"{page}: no counterpart at {twin}")


def check_hreflang(pages: list[str], parsed: dict) -> None:
    global checks_run
    checks_run += 1
    for page in pages:
        p = parsed[page]
        if "x-default" not in p.hreflangs:
            err(f"{page}: missing hreflang x-default")
        for lang in ("en", "sv"):
            if lang not in p.hreflangs:
                err(f"{page}: missing hreflang={lang}")
        # The alternate must point at the same page in the other locale
        want = p.hreflangs.get("x-default", "")
        others = [h for lg, h in p.hreflangs.items() if lg != "x-default"]
        if want and want not in others:
            err(f"{page}: x-default {want} does not match any hreflang alternate")


def check_document_basics(pages: list[str], parsed: dict) -> None:
    global checks_run
    checks_run += 1
    for page in pages:
        p = parsed[page]
        if not p.lang:
            err(f"{page}: missing <html lang>")
        if page.startswith("en/") and p.lang != "en":
            err(f"{page}: html lang is {p.lang!r}, expected 'en'")
        if page.startswith("sv/") and p.lang != "sv":
            err(f"{page}: html lang is {p.lang!r}, expected 'sv'")
        if not p.canonical:
            err(f"{page}: no canonical URL")
        if not p.meta_description:
            err(f"{page}: no meta description")
        elif not (50 <= len(p.meta_description) <= 320):
            warn(f"{page}: meta description is {len(p.meta_description)} chars")
        if p.h1_count != 1:
            err(f"{page}: expected exactly one <h1>, found {p.h1_count}")
        if not p.has_main:
            err(f"{page}: no <main id=\"main\"> landmark")
        # Heading order must not skip a level
        for a, b in zip(p.h_levels, p.h_levels[1:]):
            if b - a > 1:
                warn(f"{page}: heading jumps h{a} -> h{b}")
        if p.imgs_alt_missing:
            err(f"{page}: {len(p.imgs_alt_missing)} <img> without alt")
        for dup in p.id_dupes:
            err(f"{page}: duplicate id=\"{dup}\" — #anchors and aria wiring "
                "resolve to the first element only")
        for bad in p.bad_attrs:
            err(f"{page}: stray quote inside an attribute name ({bad!r}) — "
                "the value is malformed")
        for he in p.heading_errors:
            err(f"{page}: heading tag mismatch — {he}")
        for h in p.heading_stack:
            err(f"{page}: <{h}> opened but never closed")
        for href in p.external_noopener:
            err(f"{page}: target=_blank without rel=noopener -> {href}")
        for raw in p.jsonld:
            try:
                json.loads(raw)
            except json.JSONDecodeError as exc:
                err(f"{page}: invalid JSON-LD ({exc})")
            for m in re.finditer(r'https://[^"\s]*?/\.\./', raw):
                err(f"{page}: JSON-LD URL has an unresolved ../ segment "
                    f"({m.group(0)!r})")
        # A translation helper that already escapes, escaped again at the call
        # site, renders entities literally: "don&#x27;t" instead of "don't".
        with open(os.path.join(ROOT, page), encoding="utf-8") as fh:
            src = fh.read()
        for bad in ("&amp;#", "&amp;lt;", "&amp;gt;", "&amp;quot;", "&amp;amp;"):
            n = src.count(bad)
            if n:
                err(f"{page}: {n} double-escaped entity(ies) ({bad}) — "
                    "the string is escaped twice and will show as markup")


def check_affiliate_labels(pages: list[str]) -> None:
    """
    Swedish law (marknadsföringslagen) plus the industry recommendation from
    Sveriges Tidskrifter requires the advertiser to be identifiable next to
    every affiliate link, and a disclosure bar on pages that carry them.
    """
    global checks_run
    checks_run += 1
    for page in pages:
        markup = read(page)
        rel_sponsored = len(re.findall(r'rel="sponsored', markup))
        rel_plain = len(re.findall(r'rel="nofollow noopener"', markup))
        monetised = rel_sponsored + rel_plain
        if monetised == 0:
            continue

        if not re.search(r'<aside class="aff-bar"', markup):
            err(f"{page}: has {monetised} outbound commercial link(s) but no disclosure bar")
        # Every commercial CTA block must carry an Ad/Annons label
        tags = len(re.findall(r'<span class="cta-tag"[^>]*>', markup))
        if tags < monetised:
            err(f"{page}: {monetised} commercial link(s) but only {tags} 'Ad'/'Annons' label(s)")
        for match in re.findall(r'<span class="cta-tag"[^>]*>([^<]*)</span>', markup):
            if match.strip() not in ("Ad", "Annons", "Annonslänk", "External", "Extern"):
                err(f"{page}: unexpected cta-tag label {match!r}")


unreplaced: list[str] = []


def check_sort_keys(pages: list[str]) -> None:
    """
    Sorting fails silently in two ways: a header or dropdown option whose
    data-key matches no cell, and a column whose cells all carry the same
    data-sort value, so the click reorders nothing. The devices column shipped
    that way — `max(devices, 99)` returns 99 for every provider.
    """
    global checks_run
    checks_run += 1
    for page in pages:
        markup = read(page)
        if "cmp-sort" not in markup:
            continue
        values: dict[str, list[str]] = {}
        for td in re.findall(r"<td[^>]*>", markup):
            key = re.search(r'\bdata-key="([^"]+)"', td)
            if not key:
                continue
            sort = re.search(r'\bdata-sort="([^"]*)"', td)
            values.setdefault(key.group(1), []).append(
                sort.group(1) if sort else "")
        keys = set(values)
        # compare.js also falls back to a row-level data-<key> attribute
        for row_tag in re.findall(r"<tr[^>]*>", markup):
            keys |= set(re.findall(r'\bdata-([a-z]+)="', row_tag))
        for option in re.findall(r'<option value="([a-z_]+:(?:asc|desc))"', markup):
            key = option.split(":", 1)[0]
            if key not in keys:
                err(f"{page}: sort option {option!r} has no td[data-key={key!r}] to sort by")
        for key in re.findall(r'<th[^>]*class="sortable"[^>]*\bdata-key="([^"]+)"', markup):
            vals = values.get(key, [])
            if not vals:
                err(f"{page}: sortable header {key!r} has no td[data-key={key!r}] to sort by")
            elif len(set(vals)) == 1:
                err(f"{page}: sortable column {key!r} gives every row the same "
                    f"data-sort {vals[0]!r}, so clicking it never changes the order")


def check_rank_order(pages: list[str]) -> None:
    """
    The '#' column is the ranking this site claims to publish, so it must read
    1..N straight down the table (and the mobile cards must agree). A table
    that jumps 6,8,10,7,9 tells the reader the scores and the ranks disagree.
    """
    global checks_run
    checks_run += 1
    for page in pages:
        markup = read(page)
        nums = [int(n) for n in re.findall(
            r'<td[^>]*\bdata-key="rank"[^>]*>#(\d+)</td>', markup)]
        if not nums:
            continue
        if nums != list(range(1, len(nums) + 1)):
            err(f"{page}: rank column reads {nums}, expected 1..{len(nums)} "
                f"in order")
        cards = [int(n) for n in re.findall(
            r'class="cmp-card__rank">#(\d+)</div>', markup)]
        if cards and cards != nums:
            err(f"{page}: mobile cards are ranked {cards} but the table is "
                f"ranked {nums}")


def check_outbound_links(pages: list[str]) -> None:
    """
    Every outbound link must be rel-tagged (sponsored when tracked) and must
    carry an Ad/Annons label immediately before it — marknadsföringslagen.
    """
    global checks_run
    checks_run += 1
    for page in pages:
        markup = read(page)
        for m in re.finditer(r"<a\b[^>]*target=\"_blank\"[^>]*>", markup):
            tag = m.group(0)
            before = markup[max(0, m.start() - 320):m.start()]
            rel_m = re.search(r'rel="([^"]*)"', tag)
            rel = (rel_m.group(1) if rel_m else "").lower()
            if "noopener" not in rel:
                err(f"{page}: outbound link without rel=noopener -> {tag[:90]}")
            if "sponsored" not in rel and "nofollow" not in rel:
                err(f"{page}: outbound link is neither sponsored nor nofollow "
                    f"-> {tag[:90]}")
            if 'data-affiliate="true"' in tag and "sponsored" not in rel:
                err(f"{page}: data-affiliate=true but rel is not sponsored -> {tag[:90]}")
            if "cta-tag" not in before:
                err(f"{page}: outbound link without an Ad/Annons label next to it "
                    f"-> {tag[:90]}")


def check_usecase_links(pages: list[str], doc: dict) -> None:
    """A ?use= deep link must name a use case that actually exists."""
    global checks_run
    checks_run += 1
    ids = {u["id"] for u in doc["useCases"]}
    for page in pages:
        for value in re.findall(r'\?use=([a-z0-9-]+)"', read(page)):
            if value not in ids:
                err(f"{page}: deep link ?use={value} is not a known use case")


def check_identity_disclosure(pages: list[str]) -> None:
    """marknadsföringslagen 4 §: you must be able to identify the advertiser."""
    global checks_run
    checks_run += 1
    from build import SITE

    required = (
        (SITE["legal_name"], "advertiser name"),
        (SITE["address"], "postal address"),
        (SITE["email"], "email address"),
    )
    for page in pages:
        markup = read(page)
        m = re.search(r'class="identity[^"]*"[^>]*>(.*?)</(?:dl|div)>',
                      markup, re.S)
        if not m:
            err(f"{page}: no advertiser identification block")
        else:
            block = m.group(1)
            for value, label in required:
                if value not in block:
                    err(f"{page}: identification is missing the {label}")
            if f'mailto:{SITE["email"]}' not in block:
                err(f"{page}: identification has no mailto link to "
                    f"{SITE['email']}")
        if "__REPLACE" in markup:
            unreplaced.append(page)


def check_placeholders(pages: list[str]) -> None:
    global checks_run
    checks_run += 1
    for page in pages:
        markup = read(page)
        for hit in set(re.findall(r"PLACEHOLDER_[A-Z_]+", markup)):
            err(f"{page}: affiliate URL still a placeholder: {hit}")


def check_affiliate_data() -> dict:
    global checks_run
    checks_run += 1
    path = os.path.join(ROOT, "assets", "data", "affiliates.json")
    with open(path, encoding="utf-8") as fh:
        aff = json.load(fh)
    placeholders = [
        pid for pid, v in aff["providers"].items()
        if v.get("url", "").startswith("PLACEHOLDER_")
    ]
    if placeholders:
        err(
            "affiliates.json: no live affiliate link yet for "
            + ", ".join(sorted(placeholders))
            + "\n           Site currently links to each provider's plain URL, so it works "
              "but earns nothing. Paste your tracking links to go live."
        )
    return aff


def check_provider_data() -> dict:
    global checks_run
    checks_run += 1
    with open(os.path.join(ROOT, "assets", "data", "providers.json"), encoding="utf-8") as fh:
        doc = json.load(fh)

    providers = doc["providers"]
    weights = doc["_meta"]["scoringModel"]["weights"]

    if abs(sum(weights.values()) - 1.0) > 1e-9:
        err(f"providers.json: scoring weights sum to {sum(weights.values())}, must be 1.0")

    seen_ranks = set()
    for p in providers:
        pid = p["id"]
        if p["rank"] in seen_ranks:
            err(f"providers.json: duplicate rank {p['rank']}")
        seen_ranks.add(p["rank"])

        for key in ("privacy", "speed", "price", "streaming", "easeOfUse"):
            v = p["scores"].get(key)
            if v is None or not (0 <= v <= 10):
                err(f"providers.json: {pid} has invalid {key} score {v!r}")

        if not p.get("lastPriceVerified") and False:
            pass

        if not p.get("pricing"):
            err(f"providers.json: {pid} has no pricing")
        for plan in p.get("pricing", []):
            # A price quote without the total is not compliant advertising
            for cur in ("SEK", "USD"):
                if plan.get(f"total{cur}") is None:
                    err(f"providers.json: {pid} plan missing total{cur} (total price is legally required)")
                if plan.get(f"monthly{cur}") is None:
                    err(f"providers.json: {pid} plan missing monthly{cur}")
            # monthly x term must reconcile with the total within rounding
            for cur in ("SEK", "USD"):
                expected = plan[f"total{cur}"] / plan["termMonths"]
                if abs(expected - plan[f"monthly{cur}"]) > 1.0:
                    warn(
                        f"providers.json: {pid} {plan['termMonths']}m {cur} "
                        f"total {plan[f'total{cur}']} does not reconcile with "
                        f"monthly {plan[f'monthly{cur}']} (expected ~{expected:.0f})"
                    )

        if not p.get("scoreBasis"):
            err(f"providers.json: {pid} has no scoreBasis explanation")
        if p.get("bestFor") is None:
            err(f"providers.json: {pid} has no bestFor list")

    if doc["_meta"]["benchmarking"].startswith("We have NOT") and \
            any(p.get("speedTestedByUs") for p in providers):
        err("providers.json: speedTestedByUs is true somewhere but methodology says we have not benchmarked")

    return doc


def check_no_fabricated_metrics(pages: list[str]) -> None:
    """
    The site claims it has not run throughput benchmarks. Any 'Mbps' or
    'ping' figure in the output would contradict that disclosure.
    """
    global checks_run
    checks_run += 1
    pattern = re.compile(r"\b\d{2,4}\s?(?:Mbps|mbps|Mbit|ping(?:s)?\b(?! ball))", re.I)
    for page in pages:
        markup = read(page)
        hit = pattern.search(markup)
        if hit:
            err(f"{page}: contains a throughput figure we never measured: {hit.group(0)!r}")


def check_assets(pages: list[str]) -> None:
    global checks_run
    checks_run += 1
    for page in pages:
        src = read(page)
        for ref in set(re.findall(r'(?:href|src)="((?:\.\./)*assets/[^"#?]+)"', src)):
            target = resolve(page, ref)
            if target and not os.path.exists(os.path.join(ROOT, target)):
                err(f"{page}: missing asset {ref}")
        # og:image / twitter:image are absolute URLs back to our own origin
        for meta in set(re.findall(r'content="https?://[^"]+?/assets/([^"?#]+)"', src)):
            if not os.path.exists(os.path.join(ROOT, "assets", meta)):
                err(f"{page}: missing social image assets/{meta}")
        # CSS and JS are served immutable for a year, so every reference must
        # carry a ?v= content hash — otherwise a deploy ships markup the
        # visitor's cached stylesheet does not cover yet.
        for ref in set(re.findall(r'(?:href|src)="((?:\.\./)*assets/(?:css|js)/[^"]+)"', src)):
            if "?v=" not in ref:
                err(f"{page}: immutable-cached asset without a version: {ref}")


def check_adsense(pages: list[str]) -> None:
    """
    The AdSense account script must be present in the <head> of every content
    page (Google verifies the site by fetching it), and the Content-Security-
    Policy must actually permit the AdSense hosts — otherwise the tag is dead
    markup that only slows the page down.
    """
    global checks_run
    checks_run += 1
    tag = ("pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"
           "?client=ca-pub-5225967374919408")
    for page in pages:
        if tag not in read(page):
            err(f"{page}: AdSense account script missing from <head>")
    with open(os.path.join(ROOT, "_headers"), encoding="utf-8") as fh:
        headers = fh.read()
    for host in ("pagead2.googlesyndication.com",
                 "googleads.g.doubleclick.net",
                 "tpc.googlesyndication.com"):
        if host not in headers:
            err(f"_headers: Content-Security-Policy does not allow {host} — "
                f"ads from that host would be blocked")
    # ads.txt authorizes this seller ID to Google's crawlers. Wrong ID (or no
    # file) means approval stalls even with the tag in place.
    try:
        with open(os.path.join(ROOT, "ads.txt"), encoding="utf-8") as fh:
            ads = fh.read()
    except OSError:
        ads = ""
    if "google.com, pub-5225967374919408, DIRECT, f08c47fec0942fa0" not in ads:
        err("ads.txt: missing or wrong google.com DIRECT line for "
            "pub-5225967374919408")


def check_gtag(pages: list[str]) -> None:
    """
    The Google tag must open every page (Analytics is configured from it),
    storage must default to denied so nothing is measured before the visitor
    accepts, and the Content-Security-Policy must permit the tag hosts —
    otherwise the tag is dead markup that only slows the page down.
    """
    global checks_run
    checks_run += 1
    tag = "googletagmanager.com/gtag/js?id=G-3X91TTYPWR"
    for page in pages:
        markup = read(page)
        if tag not in markup:
            err(f"{page}: Google tag missing from <head>")
        if "gtag('consent', 'default'" not in markup:
            err(f"{page}: Google tag has no consent-denied defaults")
    with open(os.path.join(ROOT, "_headers"), encoding="utf-8") as fh:
        headers = fh.read()
    for host in ("www.googletagmanager.com", "www.google-analytics.com"):
        if host not in headers:
            err(f"_headers: Content-Security-Policy does not allow {host} — "
                f"the Google tag would be blocked")
    if tag not in read("index.html"):
        err("index.html: Google tag missing — it must open every page, "
            "including the root picker")


def check_sitemap(pages: list[str]) -> None:
    global checks_run
    checks_run += 1
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path):
        err("sitemap.xml missing")
        return
    with open(path, encoding="utf-8") as fh:
        xml = fh.read()
    locs = re.findall(r"<loc>([^<]+)</loc>", xml)
    for page in pages:
        if not any(l.endswith(page.replace(".html", "") + ".html") or
                   l.endswith("/" + page.split("/", 1)[1].replace("index.html", ""))
                   for l in locs):
            warn(f"sitemap.xml: no entry for {page}")


def check_css_coverage(pages: list[str]) -> None:
    """
    Any class used in the markup must exist in site.css, otherwise the element
    renders unstyled and nobody notices until it looks broken.
    """
    global checks_run
    checks_run += 1
    with open(os.path.join(ROOT, "assets", "css", "site.css"), encoding="utf-8") as fh:
        defined = set(re.findall(r"\.([a-zA-Z][a-zA-Z0-9_-]*)", fh.read()))
    # Classes defined in a page-local <style> block are exempt.
    local = {"picks"}
    used: dict[str, str] = {}
    for page in pages:
        for group in re.findall(r'class="([^"]+)"', read(page)):
            for name in group.split():
                if name not in defined and name not in local:
                    used.setdefault(name, page)
    for name, page in sorted(used.items()):
        err(f"{page}: class .{name} is used but not defined in site.css")


def check_score_ring(pages: list[str]) -> None:
    """
    The gauge arc is drawn with SVG presentation attributes (dasharray and
    dashoffset). CSS drops unitless numbers for those properties and any rule
    for them overrides the attributes, so both mistakes render a full circle
    instead of a partial gauge — silently, on every ring.
    """
    global checks_run
    checks_run += 1
    circ = 2 * math.pi * 20          # r=20 in the 48×48 viewBox
    with open(os.path.join(ROOT, "assets", "css", "site.css"), encoding="utf-8") as fh:
        css = fh.read()
    if re.search(r"\.ring__arc[^}]*stroke-dash", css, re.S):
        err("site.css: .ring__arc sets stroke-dash*, which overrides the ring's "
            "SVG attributes and draws a full circle instead of the score arc")
    for page in pages:
        markup = read(page)
        arcs = re.findall(r'<circle class="ring__arc"[^>]*>', markup)
        if not arcs:
            continue
        vals = markup.count('class="ring__val"')
        if vals != len(arcs):
            err(f"{page}: {vals} score values but {len(arcs)} arcs — a ring "
                f"renders without its number or vice versa")
        for tag in arcs:
            a = re.search(r'stroke-dasharray="([\d.]+)"', tag)
            o = re.search(r'stroke-dashoffset="([\d.]+)"', tag)
            if not a or not o:
                err(f"{page}: score ring arc is missing stroke-dasharray/"
                    f"stroke-dashoffset, so it draws a full circle")
                break
            if abs(float(a.group(1)) - circ) > 0.01 or not 0 <= float(o.group(1)) <= circ:
                err(f"{page}: score ring dash values are out of range "
                    f"(array={a.group(1)}, offset={o.group(1)}, expected "
                    f"array={circ:.4f} and 0 <= offset <= {circ:.4f})")
                break


def check_score_breakdown(pages: list[str]) -> None:
    """
    Every review breaks its score into one line per weighted category. Two
    silent failures: a review that skips the breakdown, and a fill left as an
    inline <span> — width and height do not apply to inline boxes, so the
    reader sees empty grey tracks with no score line in them.
    """
    global checks_run
    checks_run += 1
    with open(os.path.join(ROOT, "assets", "data", "providers.json"), encoding="utf-8") as fh:
        doc = json.load(fh)
    weights = doc["_meta"]["scoringModel"]["weights"]
    fill_rule = re.search(r"\.bar__fill\s*\{([^}]*)\}", read_css())
    if not fill_rule:
        err("site.css: no .bar__fill rule — score lines have no height or colour")
    elif not re.search(r"display\s*:\s*(?:block|flow-root|inline-block|flex|grid)",
                       fill_rule.group(1)):
        err("site.css: .bar__fill has no block-level display, so its inline <span> "
            "ignores width/height and draws no score line")
    for page in pages:
        if "/vpn/" not in page:
            continue
        markup = read(page)
        widths = re.findall(r'class="bar__fill"[^>]*\bstyle="width:(\d+)%"', markup)
        if not widths:
            err(f"{page}: review has no score breakdown lines")
            continue
        if len(widths) != len(weights):
            err(f"{page}: {len(widths)} score lines, expected one per weighted "
                f"category ({len(weights)})")
            continue
        pid = os.path.splitext(os.path.basename(page))[0]
        p = next((x for x in doc["providers"] if x["id"] == pid), None)
        if not p:
            continue
        want = sorted(f"{p['scores'][k] * 10:.0f}" for k in weights)
        got = sorted(widths)
        if want != got:
            err(f"{page}: score lines draw {got}% but providers.json scores "
                f"{p['scores']} give {want}%")


def check_price_currency(pages: list[str]) -> None:
    """
    Currency follows the page language: English quotes USD on its own,
    Swedish quotes SEK plus the converted USD line (S["alt_currency"]).

    Two ways to break it: a SEK figure leaking into an English page, which
    forces the reader to do the exchange-rate arithmetic the page exists to
    avoid; and the whole second-currency line disappearing from Swedish,
    which removes the comparison Swedish visitors read prices against.
    """
    global checks_run
    checks_run += 1
    for page in pages:
        lang = page.split("/", 1)[0]
        markup = read(page)
        if lang == "en":
            if "SEK" in markup:
                err(f"{page}: quotes SEK on an English page — English quotes USD only")
            if 'class="price-alt"' in markup:
                err(f"{page}: carries a second-currency price line; that is a "
                    f"Swedish-page extra")
            if "Also in USD" in markup:
                err(f"{page}: price table has the second-currency column; it is "
                    f"Swedish-only (and on English it would show SEK)")
        else:
            if page == "sv/compare.html" and 'class="price-alt"' not in markup:
                err(f"{page}: compare table lost its converted USD price line")
            if "/vpn/" in page and "Även i USD" not in markup:
                err(f"{page}: review price table lost its converted USD column")


def check_best_vpn_for(pages: list[str], parsed: dict) -> None:
    """
    The money pages are the section most likely to drift, because three files
    have to agree: the curated picks and re-weighted criteria live in
    topics.json, the copy lives in content.py, and the URL is a clean folder
    path. A pick that stops being a real provider, criteria that stop summing
    to 100, a missing translation, or a canonical that leaks index.html are all
    silent failures — nobody notices until the page is live and wrong.
    """
    global checks_run
    checks_run += 1

    with open(os.path.join(ROOT, "assets", "data", "topics.json"),
              encoding="utf-8") as fh:
        topics = json.load(fh)["topics"]
    with open(os.path.join(ROOT, "assets", "data", "providers.json"),
              encoding="utf-8") as fh:
        prov_doc = json.load(fh)
    by_id = {p["id"]: p for p in prov_doc["providers"]}

    import content as C

    try:
        with open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8") as fh:
            sitemap = fh.read()
    except OSError:
        sitemap = ""

    component_keys = {"privacy", "speed", "price", "streaming", "easeOfUse"}
    slugs = [t["slug"] for t in topics]
    if not slugs:
        err("topics.json: no topics — the money pages would be an empty section")
    if len(set(slugs)) != len(slugs):
        err("topics.json: duplicate topic slugs")

    for t in topics:
        slug = t["slug"]
        crit = t.get("criteria") or {}
        unknown = set(crit) - component_keys
        if unknown:
            err(f"topics.json: {slug} re-weights unknown components "
                f"{sorted(unknown)}")
        total = sum(crit.values())
        if total != 100:
            err(f"topics.json: {slug} criteria sum to {total}, expected 100 — "
                f"a guide whose weights do not add up cannot be compared "
                f"with the others")
        picks = t.get("picks") or []
        if len(picks) != 3 or len(set(picks)) != 3:
            err(f"topics.json: {slug} needs three distinct picks, has {picks}")
        for pid in picks:
            if pid not in by_id:
                err(f"topics.json: {slug} pick {pid!r} is not a provider id")

    for lang in LOCALES:
        copy = C.BEST_VPN_FOR.get(lang)
        if not copy:
            err(f"content.py: no BEST_VPN_FOR copy for {lang}")
            continue
        if "hub" not in copy:
            err(f"content.py: {lang} has no hub copy for best-vpn-for/")
        if f"/{lang}/best-vpn-for/" not in sitemap:
            err(f"sitemap.xml: no entry for {lang}/best-vpn-for/")
        for t in topics:
            slug = t["slug"]
            g = copy.get(slug)
            if not g:
                err(f"content.py: {lang} has no copy for best-vpn-for/{slug}/")
                continue
            missing = {"label", "h1", "desc", "lede", "intro", "why",
                       "guide_title", "guide", "picks", "faq"} - set(g)
            if missing:
                err(f"content.py: {lang}/{slug} copy is missing {sorted(missing)}")
                continue
            if list(g["picks"]) != t["picks"]:
                err(f"content.py: {lang}/{slug} picks {list(g['picks'])} do not "
                    f"match topics.json {t['picks']}")
            desc = g["desc"]
            if not (50 <= len(desc) <= 320):
                err(f"{lang}/{slug}: meta description is {len(desc)} chars "
                    f"(need 50-320)")

            hub_page = f"{lang}/best-vpn-for/index.html"
            page = f"{lang}/best-vpn-for/{slug}/index.html"
            if page not in pages:
                err(f"{page}: page was not built")
                continue
            markup = read(page)

            # Clean folder URL: the canonical must end with the directory, and
            # must never name the file the directory would redirect away from.
            canon = (parsed[page].canonical or "")
            expect = f"/{lang}/best-vpn-for/{slug}/"
            if not canon.endswith(expect):
                err(f"{page}: canonical is {canon!r}, expected to end with "
                    f"{expect!r}")
            if "index.html" in canon:
                err(f"{page}: canonical leaks index.html ({canon}) — the "
                    f"sitemap and the canonical then disagree about the URL")

            # An unranked-product spotlight must be structurally complete,
            # point at a live affiliate entry, and actually render — otherwise
            # a paid box silently disappears (or renders unlinkable).
            sp = g.get("spotlight")
            if sp is not None:
                if set(sp) != {"eyebrow", "title", "body", "note", "cta",
                               "affiliate_id"}:
                    err(f"content.py: {lang}/{slug} spotlight keys are "
                        f"{sorted(sp)}, expected eyebrow/title/body/note/cta/"
                        f"affiliate_id")
                with open(os.path.join(ROOT, "assets", "data",
                                       "affiliates.json"),
                          encoding="utf-8") as fh:
                    aff_entry = json.load(fh)["providers"].get(
                        sp.get("affiliate_id", ""), {})
                if (not aff_entry
                        or aff_entry.get("url", "").startswith("PLACEHOLDER_")):
                    err(f"content.py: {lang}/{slug} spotlight "
                        f"{sp.get('affiliate_id')!r} has no live affiliate entry")
                if 'id="spotlight"' not in markup:
                    err(f"{page}: spotlight copy exists but the box did not "
                        f"render")
                elif ("gearupbooster.com" not in markup
                      and "jdoqocy.com" not in markup):
                    err(f"{page}: spotlight box rendered without its link")

            # The three curated picks must actually be linked from the page.
            for pid in t["picks"]:
                if pid not in by_id:
                    continue
                if f'vpn/{by_id[pid]["slug"]}.html' not in markup:
                    err(f"{page}: does not link the review of its own pick "
                        f"{by_id[pid]['name']}")

            # Sitemap entry for the clean URL.
            if f"/{lang}/best-vpn-for/{slug}/" not in sitemap:
                err(f"sitemap.xml: no entry for {lang}/best-vpn-for/{slug}/")

            if hub_page in pages:
                if f'best-vpn-for/{slug}/' not in read(hub_page):
                    err(f"{hub_page}: hub does not link best-vpn-for/{slug}/")

    # Every page in the site must reach the section (footer link), otherwise
    # the money pages are invisible from the rest of the site.
    for page in pages:
        if "best-vpn-for/" not in read(page):
            err(f"{page}: no link to the best-VPN-for guides")


def check_superlative_claims() -> None:
    """
    No claim in the copy may rest on measurement or market knowledge the
    site does not have. "The most independently audited VPN in the
    industry" cannot be defended — we publish a table of ten, not a survey
    of the industry, and two of the ten carry more audits than the provider
    that claim was written for. "Fastest" cannot be defended either: the
    speed component is an architectural estimate, and the method page says
    so.

    The phrase list below is what a marketing rewrite keeps reaching for.
    Scoped, checkable phrasing stays allowed — "our highest speed score",
    "of any provider we list", "in our comparison", "second-largest network
    in our table" — because every figure quoted in the copy is one the
    table prints.
    """
    global checks_run
    checks_run += 1

    banned = (
        # industry-wide scope nobody can verify from our data
        "in the industry", "i branschen",
        # speed claims, when we never measure throughput
        "fastest speeds", "snabbast hastigheter", "the fastest", "den snabbaste",
        # audit counts that are false even inside our own table
        "more than any other provider", "fler än någon annan leverantör",
        "highest audit count in our list", "högst antal revisioner i vår lista",
        "longest published audit streak", "längsta publicerade svit",
        # exclusivity claims that contradict another row of the table
        "the only provider in this list", "den enda leverantören i listan",
        "only free tier worth recommending", "enda gratisnivån värd att rekommendera",
        "the only one of the ten", "enda av de tio",
        "no other provider here does", "ingen annan leverantör här gör",
        "only major provider with", "endast huvudleverantören med",
        # comparative claims a reader cannot tie to a printed number
        "cheapest 2-year commitment", "billigaste 2-åriga bindningen",
        "largest server network of any", "störst servernätverk av alla",
        "the most consistent speeds", "de mest konsekventa hastigheterna",
        "most reliable streaming unblocking", "mest tillförlitliga upplåsningen",
        "widest and most consistent", "bredast och mest konsekvent",
        "handle netflix most consistently", "hanterar netflix konsekventast",
        "most honest design available", "mest ärliga konstruktionen som finns",
        "best-in-class", "marknadsledande",
    )
    sources = (
        os.path.join(ROOT, "assets", "data", "providers.json"),
        os.path.join(ROOT, "tools", "content.py"),
        os.path.join(ROOT, "assets", "data", "explained.json"),
    )
    for path in sources:
        with open(path, encoding="utf-8") as fh:
            text = fh.read().lower()
        for phrase in banned:
            if phrase.lower() in text:
                err(f"{os.path.relpath(path, ROOT)}: copy makes the "
                    f"uncheckable claim {phrase!r} — scope it to this "
                    f"comparison, or replace it with the published score")


def check_explained(pages: list[str], parsed: dict) -> None:
    """
    The explainers are the only section where copy lives in a JSON file with
    both languages side by side, so most of its failures are structural
    rather than editorial: a slug that is not unique, a translation with
    fewer paragraphs than the article it translates, a link token the build
    would choke on, an icon the sprite does not have, or a canonical that
    leaks index.html. Everything a reader would notice — a missing hub link,
    an FAQ page with no FAQPage schema, an article that never mentions a
    single review — is checked here too, because these pages are what a
    cold search visitor lands on first.
    """
    global checks_run
    checks_run += 1

    with open(os.path.join(ROOT, "assets", "data", "explained.json"),
              encoding="utf-8") as fh:
        topics = json.load(fh).get("topics") or []
    with open(os.path.join(ROOT, "assets", "data", "providers.json"),
              encoding="utf-8") as fh:
        by_id = {p["id"]: p for p in json.load(fh)["providers"]}
    with open(os.path.join(ROOT, "assets", "data", "topics.json"),
              encoding="utf-8") as fh:
        guide_slugs = {t["slug"] for t in json.load(fh)["topics"]}
    with open(os.path.join(ROOT, "assets", "img", "icons.svg"),
              encoding="utf-8") as fh:
        sprite = fh.read()
    with open(os.path.join(ROOT, "tools", "build.py"),
              encoding="utf-8") as fh:
        build_src = fh.read()
    icons = set(re.findall(r'<symbol id="i-([a-z0-9-]+)"', sprite))
    icons |= set(re.findall(r'<symbol id="i-([a-z0-9-]+)"', build_src))
    try:
        with open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8") as fh:
            sitemap = fh.read()
    except OSError:
        sitemap = ""

    import content as C

    token_re = re.compile(r"\{\{([a-z]+)(?::([a-z0-9-]+))?(?:\|[^}]*)?\}\}")
    fixed_tokens = {"compare", "method", "faq", "hub", "bfv"}
    slugs = [t.get("slug") for t in topics]
    if not slugs:
        err("explained.json: no topics — /vpn-explained/ would be an empty section")
    if len(set(slugs)) != len(slugs):
        err("explained.json: duplicate topic slugs")
    slugset = set(s for s in slugs if s)

    for hub_lang in LOCALES:
        hub = C.EXPLAINED_HUB.get(hub_lang)
        if not hub:
            err(f"content.py: no EXPLAINED_HUB copy for {hub_lang}")
            continue
        missing = {"h1", "desc", "lede", "intro", "faq"} - set(hub)
        if missing:
            err(f"content.py: EXPLAINED_HUB[{hub_lang}] is missing {sorted(missing)}")
            continue
        if not (50 <= len(hub["desc"]) <= 160):
            err(f"content.py: EXPLAINED_HUB[{hub_lang}] desc is "
                f"{len(hub['desc'])} chars (need 50-160)")
        if len(hub.get("intro") or []) < 2:
            err(f"content.py: EXPLAINED_HUB[{hub_lang}] needs two intro paragraphs")
        if len(hub.get("faq") or []) < 2:
            err(f"content.py: EXPLAINED_HUB[{hub_lang}] needs two FAQ entries")

    hub_page_missing = [l for l in LOCALES
                        if f"{l}/vpn-explained/index.html" not in pages]
    for lang in hub_page_missing:
        err(f"{lang}/vpn-explained/index.html: hub was not built")
    for lang in LOCALES:
        if f"/{lang}/vpn-explained/" not in sitemap:
            err(f"sitemap.xml: no entry for {lang}/vpn-explained/")

    for t in topics:
        slug = t.get("slug") or "?"
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
            err(f"explained.json: slug {slug!r} is not a clean URL segment")
        icon = t.get("icon")
        if icon not in icons:
            err(f"explained.json: {slug} icon {icon!r} is not in the sprite")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(t.get("published", ""))):
            err(f"explained.json: {slug} published {t.get('published')!r} "
                f"is not an ISO date")
        reviews = t.get("reviews") or []
        if not reviews:
            err(f"explained.json: {slug} links no review — an explainer with "
                f"nothing to read next is a dead end")
        for pid in reviews:
            if pid not in by_id:
                err(f"explained.json: {slug} review {pid!r} is not a provider id")
        guides = t.get("guides") or []
        if not guides:
            err(f"explained.json: {slug} links no money page")
        for g in guides:
            if g not in guide_slugs:
                err(f"explained.json: {slug} guide {g!r} is not a topics.json slug")

        copy = {}
        for lang in LOCALES:
            a = t.get(lang)
            if not a:
                err(f"explained.json: {slug} has no {lang} copy")
                continue
            copy[lang] = a
            missing = {"title", "desc", "lede", "sections", "faq"} - set(a)
            if missing:
                err(f"explained.json: {slug}/{lang} is missing {sorted(missing)}")
                continue
            if not (50 <= len(a["desc"]) <= 160):
                err(f"explained.json: {slug}/{lang} desc is {len(a['desc'])} "
                    f"chars (need 50-160)")
            if not (50 <= len(a["lede"]) <= 300):
                err(f"explained.json: {slug}/{lang} lede is {len(a['lede'])} "
                    f"chars (need 50-300)")
            sections = a["sections"]
            if len(sections) < 4:
                err(f"explained.json: {slug}/{lang} has {len(sections)} sections "
                    f"(a guide needs at least four)")
            h2s = []
            words = 0
            for i, sec in enumerate(sections):
                h2 = (sec.get("h2") or "").strip()
                if not h2:
                    err(f"explained.json: {slug}/{lang} section {i} has no h2")
                h2s.append(h2)
                paras = [p for p in (sec.get("p") or []) if p.strip()]
                if len(paras) < 2:
                    err(f"explained.json: {slug}/{lang} section {i} "
                        f"({h2[:40]!r}) has {len(paras)} paragraphs, needs 2")
                items = sec.get("list") or []
                if sec.get("list") and len(items) < 3:
                    err(f"explained.json: {slug}/{lang} section {i} list has "
                        f"{len(items)} items, needs 3")
                if any("<" in p or ">" in p for p in paras):
                    err(f"explained.json: {slug}/{lang} section {i} contains "
                        f"markup — copy is plain text, the template adds tags")
                words += sum(len(p.split()) for p in paras)
                words += sum(len(x.split()) for x in items)
            if len(set(h2s)) != len(h2s):
                err(f"explained.json: {slug}/{lang} repeats an h2")
            faq = a["faq"]
            if not (3 <= len(faq) <= 4):
                err(f"explained.json: {slug}/{lang} has {len(faq)} FAQ entries "
                    f"(need 3 or 4)")
            questions = [q for q, _ans in faq]
            for q, ans in faq:
                if not q.endswith("?"):
                    err(f"explained.json: {slug}/{lang} FAQ question {q!r} "
                        f"does not end with ?")
                if len(ans) < 60:
                    err(f"explained.json: {slug}/{lang} FAQ answer {q[:40]!r} "
                        f"is {len(ans)} chars (need 60+)")
            if len(set(questions)) != len(questions):
                err(f"explained.json: {slug}/{lang} repeats an FAQ question")
            words += sum(len(q.split()) + len(a.split()) for q, a in faq)
            if not (750 <= words <= 1500):
                err(f"explained.json: {slug}/{lang} is {words} words "
                    f"(a guide needs 750-1500)")
            if "__REPLACE" in json.dumps(a):
                err(f"explained.json: {slug}/{lang} still contains __REPLACE")

            # link tokens must all resolve, or the build dies on this entry
            raw = json.dumps(a, ensure_ascii=False)
            for m in token_re.finditer(raw):
                kind, arg = m.group(1), m.group(2)
                if kind in fixed_tokens:
                    if arg:
                        err(f"explained.json: {slug}/{lang} token {m.group(0)!r} "
                            f"takes no argument")
                elif kind == "review":
                    if arg not in by_id:
                        err(f"explained.json: {slug}/{lang} token {m.group(0)!r} "
                            f"names no provider")
                elif kind == "guide":
                    if arg not in guide_slugs:
                        err(f"explained.json: {slug}/{lang} token {m.group(0)!r} "
                            f"names no money page")
                elif kind == "explain":
                    if arg not in slugset:
                        err(f"explained.json: {slug}/{lang} token {m.group(0)!r} "
                            f"names no explainer")
                else:
                    err(f"explained.json: {slug}/{lang} has unknown token "
                        f"{m.group(0)!r}")

        if len(copy) == len(LOCALES):
            en, sv = copy["en"], copy["sv"]
            if [len(s["p"]) for s in en["sections"]] != \
               [len(s["p"]) for s in sv["sections"]]:
                err(f"explained.json: {slug} sv paragraphs do not mirror en — "
                    f"the two languages are one entry, they cannot drift")
            if [len(s.get("list") or []) for s in en["sections"]] != \
               [len(s.get("list") or []) for s in sv["sections"]]:
                err(f"explained.json: {slug} sv list lengths do not mirror en")
            if len(en["faq"]) != len(sv["faq"]):
                err(f"explained.json: {slug} sv FAQ does not mirror en")
            if en["lede"] == sv["lede"]:
                err(f"explained.json: {slug} sv lede is still the English one")

        for lang in LOCALES:
            if lang not in copy:
                continue
            a = copy[lang]
            page = f"{lang}/vpn-explained/{slug}/index.html"
            if page not in pages:
                err(f"{page}: page was not built")
                continue
            markup = read(page)
            canon = parsed[page].canonical or ""
            expect = f"/{lang}/vpn-explained/{slug}/"
            if not canon.endswith(expect):
                err(f"{page}: canonical is {canon!r}, expected to end with "
                    f"{expect!r}")
            if "index.html" in canon:
                err(f"{page}: canonical leaks index.html ({canon})")
            h1 = re.search(r"<h1[^>]*>(.*?)</h1>", markup, re.S)
            h1_text = html.unescape(re.sub(r"<[^>]+>", "", h1.group(1))).strip() \
                if h1 else ""
            if h1_text != a["title"]:
                err(f"{page}: h1 {h1_text!r} does not match the copy title "
                    f"{a['title']!r}")
            if "{{" in markup:
                err(f"{page}: unresolved link token left in the page")
            types = set()
            for blob in parsed[page].jsonld:
                try:
                    types.add(json.loads(blob).get("@type"))
                except ValueError:
                    err(f"{page}: unparseable JSON-LD block")
            for need in ("Article", "FAQPage", "BreadcrumbList"):
                if need not in types:
                    err(f"{page}: no {need} JSON-LD")
            if f"/{lang}/vpn-explained/{slug}/" not in sitemap:
                err(f"sitemap.xml: no entry for {lang}/vpn-explained/{slug}/")
            # the page has to lead somewhere useful in both directions
            if "vpn-explained/" not in markup:
                err(f"{page}: no link back to the explainer hub")
            linked = {l["href"] for l in parsed[page].links}
            for pid in t.get("reviews", []):
                if pid in by_id and not any(
                        h.endswith(f"vpn/{by_id[pid]['slug']}.html") for h in linked):
                    err(f"{page}: does not link the review {by_id[pid]['name']}")
            for g in t.get("guides", []):
                if not any(f"best-vpn-for/{g}/" in h for h in linked):
                    err(f"{page}: does not link money page {g!r}")

    # hub must reach every explainer, and every page must reach the hub
    for lang in LOCALES:
        hub_page = f"{lang}/vpn-explained/index.html"
        if hub_page not in pages:
            continue
        for slug in slugset:
            if f"vpn-explained/{slug}/" not in read(hub_page):
                err(f"{hub_page}: hub does not link vpn-explained/{slug}/")
    for page in pages:
        if "vpn-explained/" not in read(page):
            err(f"{page}: no link to the VPN-explained section")


def check_svg_sprite() -> None:
    global checks_run
    checks_run += 1
    used = set()
    for page in all_pages():
        used.update(re.findall(r'<use href="#i-([a-z0-9-]+)"', read(page)))
    js_dir = os.path.join(ROOT, "assets", "js")
    for f in os.listdir(js_dir) if os.path.isdir(js_dir) else []:
        if f.endswith(".js"):
            with open(os.path.join(js_dir, f), encoding="utf-8") as fh:
                used.update(re.findall(r'#i-([a-z0-9-]+)', fh.read()))
    with open(os.path.join(ROOT, "assets", "img", "icons.svg"), encoding="utf-8") as fh:
        sprite = fh.read()
    with open(os.path.join(ROOT, "tools", "build.py"), encoding="utf-8") as fh:
        extra = fh.read()
    defined = set(re.findall(r'<symbol id="i-([a-z0-9-]+)"', sprite))
    defined |= set(re.findall(r'<symbol id="i-([a-z0-9-]+)"', extra))
    missing = used - defined
    if missing:
        err("icon sprite: referenced but not defined: " + ", ".join(sorted(missing)))
    unused = defined - used
    if unused:
        warn("icon sprite: defined but never used: " + ", ".join(sorted(unused)))


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def check_root_index() -> None:
    """The root language picker is excluded from the per-page checks."""
    global checks_run
    checks_run += 1
    if not os.path.exists(os.path.join(ROOT, "index.html")):
        err("index.html: root language picker is missing")
        return
    src = read("index.html")
    if 'rel="icon"' not in src:
        err("index.html: no favicon link")
    if "vpnpick:theme" not in src:
        err("index.html: theme is not applied before first paint "
            "(light-mode visitors would get a dark flash)")
    if 'content="noindex' not in src:
        err("index.html: language picker must be noindex, follow")
    if "css/site.css?v=" not in src:
        err("index.html: stylesheet has no ?v= version — returning visitors "
            "would keep the stale cached CSS")
    if "adsbygoogle.js?client=ca-pub-5225967374919408" not in src:
        err("index.html: AdSense account script missing — Google verifies "
            "the site at the domain root")
    head = re.sub(r"<script.*?</script>", "", src.split("</head>")[0], flags=re.S)
    for m in re.finditer(r"&(?!(?:amp|lt|gt|quot|apos|nbsp|#\d+|#x[0-9a-fA-F]+);)", head):
        err(f"index.html: raw '&' in the document head — escape it as &amp; "
            f"({head[m.start():m.start() + 40]!r})")


_cache: dict[str, str] = {}


def read(page: str) -> str:
    if page not in _cache:
        with open(os.path.join(ROOT, page), encoding="utf-8") as fh:
            _cache[page] = fh.read()
    return _cache[page]


def read_css() -> str:
    if "css" not in _cache:
        with open(os.path.join(ROOT, "assets", "css", "site.css"), encoding="utf-8") as fh:
            _cache["css"] = fh.read()
    return _cache["css"]


def main() -> int:
    global DRAFT
    strict = "--strict" in sys.argv
    DRAFT = "--draft" in sys.argv

    doc = check_provider_data()
    check_affiliate_data()

    pages = all_pages()
    parsed: dict[str, Inspector] = {}
    for page in pages:
        insp = Inspector()
        insp.feed(read(page))
        parsed[page] = insp

    check_internal_links(pages, parsed)
    check_locale_pairs(pages)
    check_hreflang(pages, parsed)
    check_document_basics(pages, parsed)
    check_affiliate_labels(pages)
    check_outbound_links(pages)
    check_sort_keys(pages)
    check_rank_order(pages)
    check_usecase_links(pages, doc)
    check_identity_disclosure(pages)
    check_placeholders(pages)
    check_no_fabricated_metrics(pages)
    check_assets(pages)
    check_adsense(pages)
    check_gtag(pages)
    check_sitemap(pages)
    check_svg_sprite()
    check_score_ring(pages)
    check_score_breakdown(pages)
    check_price_currency(pages)
    check_best_vpn_for(pages, parsed)
    check_superlative_claims()
    check_explained(pages, parsed)
    check_css_coverage(pages)
    check_root_index()

    if unreplaced:
        err(
            f"advertiser identity still contains __REPLACE on {len(unreplaced)} page(s) "
            f"(e.g. {unreplaced[0]}). Set SITE in tools/build.py: legal name, "
            f"email, postal address."
        )

    # ---------------------------------------------------------------- report
    total_providers = len(doc["providers"])
    print("\n  VPN-Pick.com pre-launch check")
    print(f"  {len(pages)} pages ({LOCALES[0]}/{LOCALES[1]}), "
          f"{total_providers} providers, {checks_run} checks")
    if DRAFT:
        print("  mode: DRAFT — affiliate and identity gates downgraded to warnings")
    print()

    if warnings:
        print(f"  {len(warnings)} warning(s):")
        for w in warnings:
            print(f"    ~ {w}")
        print()

    if errors:
        print(f"  {len(errors)} error(s):")
        for e in errors:
            print(f"    x {e}")
        print()
        if any("placeholder" in e or "PLACEHOLDER" in e for e in errors):
            print("  \033[1mAffiliates are not wired up yet.\033[0m The site is fully browsable")
            print("  and every link currently goes to the provider's plain homepage, so no")
            print("  commission is claimed. Paste your tracking URLs into")
            print("  assets/data/affiliates.json and re-run to go live.\n")
        print("  DO NOT DEPLOY YET.\n")
        return 1

    print("  All checks passed.\n")
    if DRAFT and warnings:
        print("  Draft mode: the warnings above are what still blocks launch "
              "(affiliate links / identity placeholders).\n")
    if DRAFT:
        print("  Finish the go-live checklist in README.md, then re-run without --draft.\n")
    if not strict and warnings:
        print("  Warnings above do not block deployment.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())