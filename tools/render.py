"""
render.py — HTML layout and reusable components for the VPN-Pick.com static site.

Everything here returns plain strings. Nothing depends on a third-party
library, a template engine or a network connection.
"""

from __future__ import annotations

import hashlib
import html
import json
import math
import os
from xml.sax.saxutils import quoteattr

# ---------------------------------------------------------------------------
# Escaping + small helpers
# ---------------------------------------------------------------------------


def e(value) -> str:
    """HTML-escape, coercing to string. Use for every dynamic value."""
    return html.escape(str(value), quote=True)


def favicon_key() -> str:
    """Cache key for the tab icon.

    /assets/* is served with `Cache-Control: immutable` for a year, so the
    artwork can only be replaced by changing its URL. Hashing the file makes
    that happen on its own whenever the icon is regenerated — otherwise the
    browser keeps the old tab logo long after the PNG is swapped.
    """
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "assets", "img", "vpn-pick-icon.png")
    with open(path, "rb") as fh:
        return hashlib.sha1(fh.read()).hexdigest()[:8]


def asset_key(rel: str) -> str:
    """Content hash for a versioned /assets/ URL.

    /assets/* is served immutable for a year, so any file whose content can
    change between deploys (CSS, JS) must change URL when it does — otherwise
    visitors keep the old file long after a deploy ships new markup that the
    cached file does not cover yet.
    """
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(base, "assets", rel), "rb") as fh:
        return hashlib.sha1(fh.read()).hexdigest()[:8]


def gtag_head(site: dict) -> str:
    """Google tag (gtag.js) for Analytics, consent-gated.

    Storage defaults to denied so the tag sets no cookies before the visitor
    accepts in our consent banner; assets/js/app.js lifts analytics_storage
    to granted on accept (and re-applies the stored choice on every load).
    Ad-related storage stays denied here — that consent belongs to Google's
    own signalling, not to our banner.
    """
    gid = site["gtag_id"]
    return f"""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={e(gid)}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('consent', 'default', {{
    'ad_storage': 'denied',
    'ad_user_data': 'denied',
    'ad_personalization': 'denied',
    'analytics_storage': 'denied'
  }});
  gtag('js', new Date());
  gtag('config', '{e(gid)}');
</script>"""


def icon(name: str, cls: str = "") -> str:
    """Inline <use> reference to an inlined sprite symbol."""
    classes = f' class="{e(cls)}"' if cls else ""
    return (
        f'<svg{classes} aria-hidden="true" focusable="false" width="1" height="1">'
        f'<use href="#i-{e(name)}"/></svg>'
    )


def data_attrs(attrs: dict) -> str:
    """Render a dict of data-* attributes, skipping empty values."""
    out = []
    for k, v in attrs.items():
        if v is None or v == "":
            continue
        out.append(f'{e(k)}="{e(v)}"')
    return (" " + " ".join(out)) if out else ""


# ---------------------------------------------------------------------------
# Locale-aware formatting
# ---------------------------------------------------------------------------

CURRENCY = {"sv": "SEK", "en": "USD"}
LOCALE_TAG = {"sv": "sv-SE", "en": "en-GB"}


def money(amount, lang: str, currency: str | None = None) -> str:
    """Total price, e.g. '749 kr' / '$74.16'.

    Whole amounts print without decimals for readability; anything with a
    fraction keeps them, so a quoted total is never rounded away from what the
    customer is actually charged.
    """
    v = float(amount)
    if abs(v - round(v)) >= 0.005:
        return money_prec(v, lang, currency)
    n = int(round(v))
    cur = currency or CURRENCY[lang]
    if lang == "sv":
        return f"{n:,}".replace(",", "\u00a0") + f"\u00a0{kr_suffix(cur)}"
    symbol = {"USD": "$", "SEK": "SEK\u00a0"}.get(cur, cur + "\u00a0")
    return symbol + f"{n:,}"


def money_prec(amount, lang: str, currency: str | None = None) -> str:
    """Money with two decimals, e.g. '31,21 kr' / '$3.09'."""
    cur = currency or CURRENCY[lang]
    v = float(amount)
    if lang == "sv":
        s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", "\u00a0")
        return f"{s}\u00a0{kr_suffix(cur)}"
    symbol = {"USD": "$", "SEK": "SEK\u00a0"}.get(cur, cur + "\u00a0")
    return symbol + f"{v:,.2f}"


def kr_suffix(cur: str) -> str:
    return "kr" if cur == "SEK" else cur


def alt_currency(cur: str) -> str:
    return "USD" if cur == "SEK" else "SEK"


def show_alt(lang: str) -> bool:
    """Whether the second-currency line renders on this page.

    English pages quote USD alone: a reader on /en/ has no use for a SEK
    figure next to every price. Only Swedish pages carry the converted
    alternative (USD).
    """
    return lang == "sv"


def long_date(iso: str, lang: str) -> str:
    """'2026-10-04' -> '4 October 2026' / '4 oktober 2026'."""
    if not iso:
        return ""
    try:
        y, m, d = (int(x) for x in iso.split("-"))
    except ValueError:
        return iso
    months = (
        ["januari", "februari", "mars", "april", "maj", "juni",
         "juli", "augusti", "september", "oktober", "november", "december"]
        if lang == "sv" else
        ["January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"]
    )
    if lang == "sv":
        return f"{d} {months[m - 1]} {y}"
    return f"{months[m - 1]} {d}, {y}"


# ---------------------------------------------------------------------------
# Domain model helpers
# ---------------------------------------------------------------------------


def weighted_score(provider: dict, weights: dict) -> float:
    """Apply the published scoring model. Never reimplemented elsewhere."""
    s = provider["scores"]
    return round(sum(s[k] * w for k, w in weights.items()), 2)


def ranked(providers: list, weights: dict) -> list:
    """Providers sorted by weighted score, ties broken by editorial rank."""
    return sorted(
        providers,
        key=lambda p: (-weighted_score(p, weights), p["rank"]),
    )


def by_rank(providers: list) -> list:
    return sorted(providers, key=lambda p: p["rank"])


def cheapest_plan(p: dict) -> dict:
    """Longest term = best effective monthly price."""
    return min(p["pricing"], key=lambda pl: pl["monthlySEK"])


def affiliate_url(ctx: dict, provider_id: str) -> tuple[str, bool]:
    """
    Return (url, is_affiliate_link).

    While any affiliate URL is still a PLACEHOLDER_ we fall back to the
    provider's own plain URL and mark the link as non-affiliate, so the site
    never claims a commission it cannot earn.
    """
    entry = ctx["affiliates"]["providers"].get(provider_id, {})
    raw = entry.get("url") or ""
    if raw.startswith("PLACEHOLDER_"):
        return entry.get("plainUrl", "#"), False
    return raw, True


def affiliate_label(ctx: dict, lang: str) -> str:
    return ctx["affiliates"]["settings"]["affiliateLabel"][lang]


# ---------------------------------------------------------------------------
# Scoring display components
# ---------------------------------------------------------------------------

SCORE_META = {
    "privacy":   {"en": "Privacy", "sv": "Integritet",        "icon": "shield"},
    "speed":     {"en": "Speed",  "sv": "Hastighet",         "icon": "bolt"},
    "price":     {"en": "Value",  "sv": "Pris",              "icon": "tag"},
    "streaming": {"en": "Streaming", "sv": "Streaming",       "icon": "tv"},
    "easeOfUse": {"en": "Ease of use", "sv": "Användarvänlighet", "icon": "tool"},
}


def score_ring(score: float, size: str = "", lang: str = "en") -> str:
    """Gauge ring: a rounded-cap SVG arc over a soft track, starting at 12
    o'clock. The arc length is set as SVG presentation attributes (dasharray +
    dashoffset) because CSS refuses unitless numbers for them — in CSS the arc
    silently drew a full circle. Scores that display as 9.0+ go gold."""
    pct = max(0, min(100, round(score * 10)))
    circ = 2 * math.pi * 20          # r=20 in the 48×48 viewBox
    offset = circ * (100 - pct) / 100
    # Gold only when the number shown in the middle is 9.0 or better, so the
    # colour and the figure never disagree.
    cls = ("ring " + size + (" ring--top" if pct >= 90 else "")).strip()
    out_of = "av 10" if lang == "sv" else "of 10"
    return (
        f'<div class="{e(cls)}" '
        f'role="img" aria-label="{score:.1f} {out_of}">'
        f'<svg class="ring__svg" viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
        f'<g transform="rotate(-90 24 24)">'
        f'<circle class="ring__track" cx="24" cy="24" r="20"/>'
        f'<circle class="ring__arc" cx="24" cy="24" r="20"'
        f' stroke-dasharray="{circ:.4f}" stroke-dashoffset="{offset:.4f}"/>'
        f"</g>"
        f"</svg>"
        f'<span class="ring__val">{score:.1f}</span></div>'
    )


def score_bars(ctx: dict, lang: str, p: dict) -> str:
    weights = ctx["providers_meta"]["scoringModel"]["weights"]
    keys = sorted(weights, key=lambda k: -weights[k])
    rows = []
    for k in keys:
        val = p["scores"][k]
        meta = SCORE_META[k]
        rows.append(
            f'<div class="bar__row">'
            f'<span class="bar__label">{e(meta[lang])}'
            f'<span class="faint"> ({int(weights[k] * 100)}%)</span></span>'
            f'<span class="bar__track"><span class="bar__fill" '
            f'style="width:{val * 10:.0f}%"></span></span>'
            f'<span class="bar__val">{val:.1f}</span>'
            f"</div>"
        )
    return f'<div class="bars">{"".join(rows)}</div>'


# ---------------------------------------------------------------------------
# Document head
# ---------------------------------------------------------------------------


def head(ctx: dict, lang: str, *, title: str, description: str,
         path: str, og_type: str = "website", noindex: bool = False,
         jsonld: list | None = None) -> str:
    site = ctx["site"]
    origin = site["origin"].rstrip("/")

    # index.html is addressed as a directory URL, everything else keeps its path
    def canonical_url(lg: str) -> str:
        # A folder page (best-vpn-for/streaming/index.html) publishes its
        # directory URL, exactly as the top-level index.html does — otherwise
        # the canonical advertises .../index.html while the site links to /.
        suffix = path[:-len("index.html")] if path.endswith("index.html") else path
        return f"{origin}/{lg}/{suffix}"

    canonical = canonical_url(lang)
    other_lang = "sv" if lang == "en" else "en"
    alts = (
        f'<link rel="alternate" hreflang="{e(lang)}" href="{e(canonical)}">\n'
        f'  <link rel="alternate" hreflang="{e(other_lang)}" '
        f'href="{e(canonical_url(other_lang))}">\n'
        f'  <link rel="alternate" hreflang="x-default" '
        f'href="{e(canonical_url("en"))}">'
    )

    noindex_tag = "\n  <meta name=\"robots\" content=\"noindex,nofollow\">" if noindex else ""
    ld = ""
    if jsonld:
        blocks = "\n".join(
            f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False, separators=(",", ":"))}</script>'
            for b in jsonld
        )
        ld = "\n  " + blocks

    css = ctx["asset"]("css/site.css") + f"?v={asset_key('css/site.css')}"

    return f"""<!DOCTYPE html>
<html lang="{e(lang)}" data-theme="dark">
<head>
  {gtag_head(site)}
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <link rel="canonical" href="{e(canonical)}">
  {alts}
  <meta property="og:type" content="{e(og_type)}">
  <meta property="og:site_name" content="{e(site['name'])}">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:url" content="{e(canonical)}">
  <meta property="og:image" content="{e(origin)}/assets/img/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{e(site['name'])}">
  <meta property="og:locale" content="{'sv_SE' if lang == 'sv' else 'en_GB'}">
  <meta property="og:locale:alternate" content="{'en_GB' if lang == 'sv' else 'sv_SE'}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(title)}">
  <meta name="twitter:description" content="{e(description)}">
  <meta name="twitter:image" content="{e(origin)}/assets/img/og-image.png">
  <meta name="theme-color" content="#080b14" media="(prefers-color-scheme: dark)">
  <meta name="theme-color" content="#f7f9fc" media="(prefers-color-scheme: light)">
  <meta name="color-scheme" content="dark light">
  <link rel="icon" href="{ctx["asset"]("img/vpn-pick-icon.png")}?v={favicon_key()}" type="image/png">
  <link rel="apple-touch-icon" href="{ctx["asset"]("img/vpn-pick-touch.png")}">
  <link rel="stylesheet" href="{css}">{noindex_tag}{ld}
  <!-- Google AdSense account script: enables ad serving/review site-wide.
       Ad slots themselves are placed separately; this tag alone sets no
       targeting cookies beyond what Google's own consent handling governs. -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={e(site["adsense_client"])}"
     crossorigin="anonymous"></script>
  <script>/* theme before first paint, so a light-mode visitor never sees a dark flash */
  (function () {{
    var t = null;
    try {{ t = localStorage.getItem('vpnpick:theme'); }} catch (e) {{}}
    if (t !== 'light' && t !== 'dark') {{
      t = (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches)
        ? 'light' : 'dark';
    }}
    document.documentElement.setAttribute('data-theme', t);
  }})();</script>
  <script src="{ctx["asset"]("js/app.js")}?v={asset_key('js/app.js')}" defer></script>
</head>"""


# ---------------------------------------------------------------------------
# Affiliate disclosure bar — legal requirement, never remove
# ---------------------------------------------------------------------------


def aff_bar(ctx: dict, lang: str) -> str:
    s = ctx["affiliates"]["settings"]
    text = s["disclosureBar"][lang].replace(
        "LINK_HOW", ctx["path"]("how-we-test.html", lang)
    )
    label = {"en": "Affiliate disclosure", "sv": "Annonsinformation"}[lang]
    return f"""<aside class="aff-bar" role="note" aria-label="{e(label)}">
  <div class="wrap">
    <span class="aff-bar__icon">{icon("info")}</span>
    <p>{text}</p>
  </div>
</aside>"""


# ---------------------------------------------------------------------------
# Header + navigation
# ---------------------------------------------------------------------------

NAV_ITEMS = [
    ("compare.html",      {"en": "Compare", "sv": "Jämför"}),
    ("best-vpn-for/",     {"en": "Best VPN for", "sv": "Bäst VPN för"}),
    ("vpn-explained/",    {"en": "Explained", "sv": "Förklaringar"}),
    ("reviews.html",      {"en": "Reviews", "sv": "Recensioner"}),
    ("how-we-test.html",  {"en": "How we test", "sv": "Så testar vi"}),
    ("faq.html",          {"en": "FAQ", "sv": "Frågor"}),
    ("about.html",        {"en": "About", "sv": "Om oss"}),
]


def header(ctx: dict, lang: str, path: str, active: str) -> str:
    site = ctx["site"]
    items = []
    for href, labels in NAV_ITEMS:
        cur = ' aria-current="page"' if href == active else ""
        items.append(f'<a href="{ctx["path"](href, lang)}"{cur}>{e(labels[lang])}</a>')

    other = "sv" if lang == "en" else "en"
    switch_href = ctx["switch"](other)

    en_cur = ' aria-current="true"' if lang == "en" else ""
    sv_cur = ' aria-current="true"' if lang == "sv" else ""

    return f"""<header class="site-header">
  <div class="wrap site-header__inner">
    <a class="brand" href="{ctx["path"]("index.html", lang)}">
      <span class="brand__mark"><img src="{ctx["asset"]("img/vpn-pick-shield-sm.png")}"
           width="24" height="27" alt=""></span>
      <span>{e(site["name"])}<span class="brand__sep"> / </span><span class="brand__sub">{e(site["tagline"][lang])}</span></span>
    </a>
    <nav class="nav" id="site-nav" aria-label="{ctx["t"]("primary_nav", lang)}">
      {"".join(items)}
    </nav>
    <div class="header-tools">
      <div class="lang" role="group" aria-label="{ctx["t"]("language", lang)}">
        <a href="{e(switch_href)}" hreflang="en" lang="en"{en_cur}>EN</a>
        <a href="{e(switch_href)}" hreflang="sv" lang="sv"{sv_cur}>SV</a>
      </div>
      <button class="icon-btn" type="button" data-theme-toggle
              aria-label="{ctx["t"]("toggle_theme", lang)}">
        {icon("moon", "i-moon")}{icon("sun", "i-sun")}
      </button>
      <button class="icon-btn nav-toggle" type="button" data-nav-toggle
              aria-expanded="false" aria-controls="site-nav"
              aria-label="{ctx["t"]("menu", lang)}">
        {icon("menu")}
      </button>
    </div>
  </div>
</header>"""


# ---------------------------------------------------------------------------
# Footer — carries the mandatory advertiser identity disclosure
# ---------------------------------------------------------------------------


def footer(ctx: dict, lang: str) -> str:
    site = ctx["site"]
    t = ctx["t"]
    year = ctx["build_year"]

    providers = ctx["providers"]
    top = by_rank(providers)[:5]

    prov_links = "".join(
        f'<li><a href="{ctx["path"]("vpn/" + p["slug"] + ".html", lang)}">{e(p["name"])}</a></li>'
        for p in top
    )
    prov_links += (
        f'<li><a href="{ctx["path"]("reviews.html", lang)}">'
        f'{t("all_reviews", lang)} {icon("chevron-right")}</a></li>'
    )

    return f"""<footer class="site-footer">
  <div class="wrap">
    <a class="footer-brand" href="{ctx["path"]("index.html", lang)}">
      <img src="{ctx["asset"]("img/vpn-pick-shield-sm.png")}" width="34" height="39"
           alt="" loading="lazy" decoding="async">
      <span class="footer-brand__text">
        <strong>{e(site["name"])}</strong>
        <span>{e(site["tagline"][lang])}</span>
      </span>
    </a>
    <div class="footer-grid">
      <div class="footer-col">
        <h2>{t("footer_about", lang)}</h2>
        <p>{ctx["th"]("footer_blurb", lang)}</p>
        <p style="margin-top:1rem">
          <a href="{ctx["path"]("about.html", lang)}">{t("footer_about_link", lang)} →</a>
        </p>
      </div>
      <div class="footer-col">
        <h2>{t("footer_reviews", lang)}</h2>
        <ul>{prov_links}</ul>
      </div>
      <div class="footer-col">
        <h2>{t("footer_guides", lang)}</h2>
        <ul>
          <li><a href="{ctx["path"]("compare.html", lang)}">{t("nav_compare", lang)}</a></li>
          <li><a href="{ctx["path"]("best-vpn-for/", lang)}">{t("bfv_hub_link", lang)}</a></li>
          <li><a href="{ctx["path"]("vpn-explained/", lang)}">{t("explained_hub_link", lang)}</a></li>
          <li><a href="{ctx["path"]("how-we-test.html", lang)}">{t("nav_how", lang)}</a></li>
          <li><a href="{ctx["path"]("faq.html", lang)}">{t("nav_faq", lang)}</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h2>{t("footer_legal", lang)}</h2>
        <ul>
          <li><a href="{ctx["path"]("about.html#disclosure", lang)}">{t("footer_disclosure", lang)}</a></li>
          <li><a href="{ctx["path"]("legal/privacy.html", lang)}">{t("footer_privacy", lang)}</a></li>
          <li><a href="{ctx["path"]("legal/cookies.html", lang)}">{t("footer_cookies", lang)}</a></li>
          <li><a href="{ctx["path"]("legal/terms.html", lang)}">{t("footer_terms", lang)}</a></li>
        </ul>
      </div>
    </div>

    <dl class="identity">
      <dt>{t("identity_heading", lang)}</dt>
      <dd>{ctx["th"]("identity_body", lang)}</dd>
      <dd>{e(site["legal_name"])}</dd>
      <dd>
        {t("identity_label_email", lang)}:
        <a href="mailto:{e(site["email"])}">{e(site["email"])}</a> ·
        {t("identity_label_address", lang)}: {e(site["address"])}
      </dd>
    </dl>

    <div class="footer-bottom">
      <p>© {year} {e(site["legal_name"])}. {t("footer_rights", lang)}</p>
      <p>{t("footer_noindependence", lang)}</p>
    </div>
  </div>
</footer>"""


# ---------------------------------------------------------------------------
# Consent banner
# ---------------------------------------------------------------------------


def consent(ctx: dict, lang: str) -> str:
    t = ctx["t"]
    return f"""<div class="consent" id="consent-banner" role="dialog"
     data-saved="{t("consent_saved", lang)}"
     aria-labelledby="consent-title" aria-describedby="consent-desc">
  <h3 id="consent-title">{icon("cookie")} {t("consent_title", lang)}</h3>
  <p id="consent-desc">{ctx["th"]("consent_body", lang)}</p>
  <div class="consent__actions">
    <button class="btn btn--primary" type="button" data-consent="accepted">
      {t("consent_accept", lang)}
    </button>
    <button class="btn btn--ghost" type="button" data-consent="necessary">
      {t("consent_necessary", lang)}
    </button>
  </div>
</div>"""


# ---------------------------------------------------------------------------
# Components
# ---------------------------------------------------------------------------


LOGO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "assets", "logos")


def monogram(ctx: dict, p: dict, size: str = "") -> str:
    """Provider mark: the vendor's own logo on a light plate where the file
    exists, otherwise the original letter badge. The plate keeps dark-ink
    artwork legible on the dark theme (same rule as .logo-plate, smaller)."""
    if os.path.exists(os.path.join(LOGO_DIR, p["slug"] + ".png")):
        variant = "brand-logo--lg" if size == "mono-badge--lg" else "brand-logo--sm"
        eager = ' fetchpriority="high"' if variant == "brand-logo--lg" else ""
        return (
            f'<span class="brand-logo {variant}" aria-hidden="true">'
            f'<img src="{ctx["asset"]("logos/" + p["slug"] + ".png")}" alt="" '
            f'decoding="async"{eager}></span>'
        )
    cls = ("mono-badge " + size).strip()
    return (
        f'<span class="{e(cls)}" style="--brand:{e(p["color"])}" '
        f'aria-hidden="true">{e(p["monogram"])}</span>'
    )


def brand_logo(ctx: dict, slug: str, size: str = "brand-logo--sm") -> str:
    """Standalone vendor logo plate for non-provider use (spotlight boxes).

    Returns an empty string when no logo file exists, so callers can simply
    omit the mark. Same plate rules as provider logos.
    """
    if not os.path.exists(os.path.join(LOGO_DIR, slug + ".png")):
        return ""
    return (
        f'<span class="brand-logo {e(size)}" aria-hidden="true">'
        f'<img src="{ctx["asset"]("logos/" + slug + ".png")}" alt="" '
        f'decoding="async"></span>'
    )


def plan_models(ctx: dict, lang: str, p: dict) -> list[dict]:
    """Every purchasable plan of a provider, ready for the interactive picker.

    Prices are pre-formatted here so the browser only swaps strings around —
    no money is ever calculated in JavaScript.
    """
    cur = CURRENCY[lang]
    o_cur = alt_currency(cur)
    per = ctx["t"]("per_month", lang)
    for_term = ctx["t"]("for_term", lang)
    cheapest = cheapest_plan(p)
    models = []
    for plan in sorted(p["pricing"], key=lambda pl: -pl["termMonths"]):
        monthly = plan["monthlySEK"] if cur == "SEK" else plan["monthlyUSD"]
        total = plan["totalSEK"] if cur == "SEK" else plan["totalUSD"]
        o_monthly = plan["monthlyUSD"] if cur == "SEK" else plan["monthlySEK"]
        o_total = plan["totalUSD"] if cur == "SEK" else plan["totalSEK"]
        term = plan["term"][lang]
        line = f"{money(total, lang, cur)} {for_term.format(term=term)}"
        if show_alt(lang):
            line += (f" · {money(o_total, lang, o_cur)}"
                     f" · {money_prec(o_monthly, lang, o_cur)}{per}")
        models.append({
            "i": len(models),
            "term": term,
            "monthly": money_prec(monthly, lang, cur),
            "line": line,
            "best": plan is cheapest,
        })
    return models


def plan_picker(ctx: dict, lang: str, p: dict) -> str:
    """Term selector. Every price in it is rendered server-side."""
    models = plan_models(ctx, lang, p)
    if len(models) < 2:
        return ""
    chips = []
    for m in models:
        pressed = "true" if m["best"] else "false"
        cls = "plan-chip is-active" if m["best"] else "plan-chip"
        chips.append(
            f'<button class="{cls}" type="button" data-plan="{m["i"]}" '
            f'aria-pressed="{pressed}">'
            f'<span class="plan-chip__term">{e(m["term"])}</span>'
            f'<span class="plan-chip__price">{e(m["monthly"])}</span>'
            f"</button>"
        )
    return f"""<div class="plan-picker" data-plan-picker>
  <p class="plan-picker__label">{icon("tag")} {ctx["t"]("plan_choose", lang)}</p>
  <div class="plan-picker__chips" role="group"
       aria-label="{ctx["t"]("plan_choose", lang)}">{"".join(chips)}</div>
</div>"""


def price_block(ctx: dict, lang: str, p: dict, plan: dict | None = None,
                with_plans: bool = False) -> str:
    """Shows the TOTAL price first, then the monthly equivalent.

    Showing the total alongside the per-month figure is a legal requirement
    for price advertising in Sweden (marknadsföringslagen 10 §).
    """
    plan = plan or cheapest_plan(p)
    cur = CURRENCY[lang]
    other = alt_currency(cur)
    monthly = plan["monthlySEK"] if cur == "SEK" else plan["monthlyUSD"]
    total = plan["totalSEK"] if cur == "SEK" else plan["totalUSD"]
    o_monthly = plan["monthlyUSD"] if cur == "SEK" else plan["monthlySEK"]
    o_total = plan["totalUSD"] if cur == "SEK" else plan["totalSEK"]
    o_cur = "USD" if cur == "SEK" else "SEK"

    term = plan["term"][lang]
    plans_attr = ""
    if with_plans:
        payload = json.dumps(plan_models(ctx, lang, p), ensure_ascii=False)
        plans_attr = f" data-plans={quoteattr(payload)}"
    alt_line = ""
    if show_alt(lang):
        alt_line = (
            f'\n    &middot; <span class="mono">{e(money(o_total, lang, o_cur))}</span>'
            f'\n    &middot; <span class="mono">'
            f'{e(money_prec(o_monthly, lang, o_cur))}{ctx["t"]("per_month", lang)}</span>'
        )
    return f"""<div class="price-block" data-plan-price{plans_attr}>
  <div class="price">
    <span class="price__now">{e(money_prec(monthly, lang, cur))}</span>
    <span class="price__per">{ctx["t"]("per_month", lang)}</span>
  </div>
  <div class="price__total">
    {e(money(total, lang, cur))} {e(ctx["t"]("for_term", lang).format(term=term))}{alt_line}
  </div>
</div>"""


def cta(ctx: dict, lang: str, p: dict, label: str | None = None,
        block: bool = False) -> str:
    """
    Affiliate call-to-action.

    The 'Ad' / 'Annons' label sits directly adjacent to the link, as required
    for affiliate links in editorial content under Swedish marketing law.
    """
    url, is_aff = affiliate_url(ctx, p["id"])
    s = ctx["affiliates"]["settings"]
    # A plain, untracked outbound link must never be tagged as a sponsored one.
    rel = s["relAttribute"] if is_aff else "nofollow noopener"
    label = label or s["ctaLabelWithPrice"][lang]
    tag = affiliate_label(ctx, lang) if is_aff else ctx["t"]("external_link", lang)
    cls = ("btn btn--primary" + (" btn--block" if block else ""))

    return f"""<div class="cta-wrap">
  <span class="cta-tag">{e(tag)}</span>
  <a class="{e(cls)}" href="{e(url)}" target="_blank" rel="{e(rel)}"
     data-provider="{e(p["id"])}" data-affiliate="{str(is_aff).lower()}">
    {e(label)} {icon("external")}
  </a>
</div>"""


def pcard(ctx: dict, lang: str, p: dict, *, show_rank: bool = True) -> str:
    total_score = weighted_score(p, ctx["providers_meta"]["scoringModel"]["weights"])
    is_top = p["rank"] == 1
    plan = cheapest_plan(p)

    chips = []
    if p["ramOnly"]:
        chips.append(f'<span class="chip chip--good">{icon("check")}{ctx["t"]("ram_only", lang)}</span>')
    if p["openSourceApps"]:
        chips.append(f'<span class="chip chip--good">{icon("code")}{ctx["t"]("open_source", lang)}</span>')
    if p["devices"] == -1:
        chips.append(f'<span class="chip chip--neutral">{icon("infinity")}{ctx["t"]("unlimited_devices", lang)}</span>')
    if p["freeTier"]:
        chips.append(f'<span class="chip chip--good">{icon("check")}{ctx["t"]("has_free_tier", lang)}</span>')
    if p["anonymousSignup"]:
        chips.append(f'<span class="chip chip--neutral">{icon("ghost")}{ctx["t"]("anon_signup", lang)}</span>')
    if p["courtTested"]:
        chips.append(f'<span class="chip chip--good">{icon("scale")}{ctx["t"]("court_tested", lang)}</span>')
    if p["audit"]["count"]:
        chips.append(
            f'<span class="chip chip--neutral">{icon("award")}'
            f'{p["audit"]["count"]}× {e(p["audit"]["firm"].split(",")[0].split(" and ")[0])}</span>'
        )

    rank_badge = (
        f'<span class="pcard__rank">#{p["rank"]}</span>' if show_rank else ""
    )

    return f"""<article class="pcard{' pcard--top' if is_top else ''}" data-key="{e(p["id"])}">
  <div class="pcard__head">
    {rank_badge}
    {monogram(ctx, p)}
    <div class="pcard__id">
      <div class="pcard__name">
        <a href="{ctx["path"]("vpn/" + p["slug"] + ".html", lang)}">{e(p["name"])}</a>
      </div>
      <div class="chip-row" style="margin-top:6px">
        <span class="badge{' badge--gold' if is_top else ''}">{e(p["badge"][lang])}</span>
      </div>
    </div>
    {score_ring(total_score, "ring--sm", lang)}
  </div>
  <div class="pcard__body">
    <p class="pcard__tagline">{e(p["tagline"][lang])}</p>
    <div class="chip-row">{"".join(chips[:4])}</div>
    {price_block(ctx, lang, p, plan)}
  </div>
  <div class="pcard__foot">
    {cta(ctx, lang, p)}
    <p class="faint" style="text-align:center;margin:0">
      {e(ctx["t"]("money_back_fmt", lang).format(days=p["moneyBackDays"]))}
    </p>
  </div>
</article>"""


def usecase_tiles(ctx: dict, lang: str) -> str:
    t = ctx["t"]
    picks = ctx["use_case_picks"]
    tiles = []
    for pick in picks:
        uc = ctx["use_case_by_id"][pick["use"]]
        # Real links: with JS off they still land on the compare page, and
        # compare.js picks up ?use= to apply the filter when JS is on.
        href = ctx["path"]("compare.html", lang) + "?use=" + pick["use"]
        tiles.append(f"""<a class="usecase" href="{href}" data-use-pick="{e(pick["use"])}">
  <span class="usecase__top">{icon(pick["icon"])}{e(uc[lang])}</span>
  <span class="usecase__who">{t("pick_for", lang)}
    <strong>{e(pick["provider"][lang])}</strong></span>
  <span class="usecase__go">{t("compare_cta_arrow", lang)} {icon("arrow-right")}</span>
</a>""")
    return f'<div class="card-grid">{"".join(tiles)}</div>'


def pros_cons(ctx: dict, lang: str, p: dict) -> str:
    t = ctx["t"]
    pros = "".join(f"<li>{e(x[lang])}</li>" for x in p["pros"])
    cons = "".join(f"<li>{e(x[lang])}</li>" for x in p["cons"])
    return f"""<div class="proscons">
  <div class="pc-pros">
    <h2>{icon("check-circle")} {t("pros", lang)}</h2>
    <ul>{pros}</ul>
  </div>
  <div class="pc-cons">
    <h2>{icon("alert")} {t("cons", lang)}</h2>
    <ul>{cons}</ul>
  </div>
</div>"""


def callout(ctx: dict, lang: str, kind: str, title: str, body: str) -> str:
    icon_name = "info"
    if kind == "warn":
        icon_name = "alert"
    cls = "callout callout--warn" if kind == "warn" else "callout"
    return f"""<div class="{e(cls)}">
  {icon(icon_name)}
  <div><strong>{e(title)}</strong>{body}</div>
</div>"""


def faq_block(items: list, *, first_open: bool = False) -> str:
    out = []
    for i, (q, a) in enumerate(items):
        open_attr = " open" if (first_open and i == 0) else ""
        out.append(
            f'<details class="faq__item"{open_attr}>'
            f'<summary>{e(q)}<span class="faq__chev">{icon("chevron-down")}</span></summary>'
            f'<div class="faq__a">{a}</div>'
            f"</details>"
        )
    return f'<div class="faq">{"".join(out)}</div>'


def breadcrumbs(ctx: dict, lang: str, trail: list) -> str:
    """
    trail: [(label, locale_relative_path|None), ...]
    Hrefs are resolved through ctx["path"] so they work from any directory
    depth (a review lives at en/vpn/<slug>.html, its index at en/reviews.html).
    """
    parts = []
    for i, (label, href) in enumerate(trail):
        last = i == len(trail) - 1
        if href and not last:
            parts.append(f'<a href="{e(ctx["path"](href, lang))}">{e(label)}</a>')
        else:
            parts.append(f'<span aria-current="page">{e(label)}</span>')
    return (
        f'<nav class="crumbs" aria-label="{ctx["t"]("breadcrumb", lang)}">'
        + f'<span class="divider-dot">/</span>'.join(parts)
        + "</nav>"
    )


def sticky_bar(ctx: dict, lang: str, p: dict) -> str:
    plan = cheapest_plan(p)
    cur = CURRENCY[lang]
    monthly = plan["monthlySEK"] if cur == "SEK" else plan["monthlyUSD"]
    url, is_aff = affiliate_url(ctx, p["id"])
    label = ctx["affiliates"]["settings"]["ctaLabel"][lang]
    tag = affiliate_label(ctx, lang) if is_aff else ctx["t"]("external_link", lang)
    rel = (ctx["affiliates"]["settings"]["relAttribute"] if is_aff
           else "nofollow noopener")
    return f"""<div class="sticky-bar">
  <div class="sticky-bar__txt">
    <strong>{e(p["name"])}</strong>
    {e(money_prec(monthly, lang, cur))}{ctx["t"]("per_month", lang)}
    · {ctx["t"]("best_label", lang)}
  </div>
  <span class="cta-tag" style="align-self:center">{e(tag)}</span>
  <a class="btn btn--primary" href="{e(url)}" target="_blank"
     rel="{e(rel)}"
     data-provider="{e(p["id"])}" data-affiliate="{str(is_aff).lower()}">
    {e(label)} {icon("arrow-right")}
  </a>
</div>"""


# ---------------------------------------------------------------------------
# JSON-LD builders
# ---------------------------------------------------------------------------


def ld_breadcrumbs(ctx: dict, lang: str, trail: list) -> dict:
    items = [{"@type": "ListItem", "position": 1,
              "name": trail[0][0], "item": ctx["absolute"](ctx["path"](trail[0][1], lang))}]
    for i, (label, href) in enumerate(trail[1:], start=2):
        items.append({"@type": "ListItem", "position": i, "name": label})
        if href:
            items[-1]["item"] = ctx["absolute"](ctx["path"](href, lang))
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def ld_faqpage(items: list) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
            for q, a in items
        ],
    }


def ld_itemlist(ctx: dict, lang: str, providers: list, name: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": name,
        "numberOfItems": len(providers),
        "itemListOrder": "https://schema.org/ItemListOrderDescending",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i,
                "url": ctx["absolute"](ctx["path"]("vpn/" + p["slug"] + ".html", lang)),
                "name": p["name"],
            }
            for i, p in enumerate(providers, start=1)
        ],
    }


def ld_review(ctx: dict, lang: str, p: dict) -> dict:
    weights = ctx["providers_meta"]["scoringModel"]["weights"]
    total = weighted_score(p, weights)
    return {
        "@context": "https://schema.org",
        "@type": "Review",
        "name": f"{p['name']} — {ctx['t']('review_headline_fmt', lang).format(name=p['name'])}",
        "reviewBody": strip_tags(p["verdict"][lang]),
        "datePublished": ctx["build_date"],
        "dateModified": ctx["build_date"],
        "publisher": {"@type": "Organization", "name": ctx["site"]["name"]},
        "itemReviewed": {
            "@type": "SoftwareApplication",
            "name": p["name"],
            "applicationCategory": "SecurityApplication",
            "operatingSystem": "Windows, macOS, Linux, iOS, Android",
        },
        "reviewRating": {
            "@type": "Rating",
            "ratingValue": f"{total:.1f}",
            "bestRating": "10",
            "worstRating": "0",
        },
    }


def ld_article(ctx: dict, lang: str, *, title: str, description: str,
               rel: str, published: str, modified: str) -> dict:
    """Editorial article: byline is the natural person behind the site, which
    is what Google's E-E-A-T signals expect on informational pages."""
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "inLanguage": lang,
        "datePublished": published,
        "dateModified": modified,
        "mainEntityOfPage": ctx["absolute"](ctx["path"](rel, lang)),
        "author": {
            "@type": "Person",
            "name": ctx["site"]["legal_name"],
            "url": ctx["absolute"](ctx["path"]("about.html", lang)),
        },
        "publisher": {
            "@type": "Organization",
            "name": ctx["site"]["name"],
            "url": ctx["site"]["origin"],
        },
    }


def ld_org(ctx: dict) -> dict:
    s = ctx["site"]
    bits = [b.strip() for b in s["address"].split(",") if b.strip()]
    street = bits[0] if bits else s["address"]
    tail = " ".join(bits[1:]) if len(bits) > 1 else ""
    head, _, rest = tail.partition(" ")
    postal, city = (head, rest) if head.isdigit() and rest else ("", tail)
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": s["name"],
        "legalName": s["legal_name"],
        "url": s["origin"],
        "email": s["email"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": street,
            "postalCode": postal,
            "addressLocality": city,
            "addressCountry": "SE",
        },
    }


def strip_tags(html_str: str) -> str:
    import re
    text = re.sub(r"<[^>]+>", "", html_str)
    return " ".join(text.split())