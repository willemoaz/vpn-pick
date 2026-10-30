#!/usr/bin/env python3
"""
build.py — generates the entire static site into ./en, ./sv and the root.

    python3 tools/build.py

Output is plain static HTML with no runtime dependencies. This script exists
so the 64 pages of bilingual content cannot drift out of sync with each other
or with assets/data/providers.json — change the data, re-run, and every page
in both languages updates at once.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import content as C  # noqa: E402
import render as R  # noqa: E402
from content import BENEFITS, ABOUT, COMPARE, COMPARE_FAQ, FAQ_GENERAL  # noqa: E402
from content import HOME, HOW_WE_TEST, LEGAL, REVIEW, SCORE_DEFS  # noqa: E402
from render import affiliate_label, by_rank, cheapest_plan, e, icon, money  # noqa: E402
from render import money_prec, ranked, score_bars, score_ring  # noqa: E402
from render import weighted_score  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "assets", "data")
BUILD_DATE = date.today().isoformat()

# ---------------------------------------------------------------------------
# Site identity — printed in the footer of every page and on the about page.
# marknadsföringslagen 4 §: a reader must be able to identify who is behind
# the advertising and reach them. tools/check.py verifies that the legal name,
# postal address and email address are present on all 64 pages, and that no
# __REPLACE placeholder is left in the generated HTML.
# ---------------------------------------------------------------------------

SITE = {
    "name": "VPN-Pick.com",
    "tagline": {"en": "VPN reviews", "sv": "VPN-recensioner"},
    "origin": "https://vpn-pick.com",  # <-- set your real domain here
    "legal_name": "Daniel Vilhelmsson",
    "email": "daniel@vpn-pick.com",
    "address": "Tessingatan 1C, 46141 Trollhättan",
    "adsense_client": "ca-pub-5225967374919408",
    "gtag_id": "G-3X91TTYPWR",
    "short_description": {
        "en": "Independent VPN reviews in English and Swedish, compared with a "
              "published scoring method.",
        "sv": "Oberoende VPN-recensioner på engelska och svenska, jämförda med en "
              "publicerad betygsmetod.",
    },
}

# Home page "start from what you need" tiles.
USE_CASE_PICKS = [
    {"use": "everyone",     "icon": "star",     "provider": {"en": "NordVPN", "sv": "NordVPN"}},
    {"use": "privacy",      "icon": "shield",   "provider": {"en": "Proton VPN", "sv": "Proton VPN"}},
    {"use": "speed",        "icon": "bolt",     "provider": {"en": "ExpressVPN", "sv": "ExpressVPN"}},
    {"use": "streaming",    "icon": "tv",       "provider": {"en": "ExpressVPN", "sv": "ExpressVPN"}},
    {"use": "budget",       "icon": "wallet",   "provider": {"en": "Private Internet Access", "sv": "Private Internet Access"}},
    {"use": "devices",      "icon": "device",   "provider": {"en": "Surfshark", "sv": "Surfshark"}},
    {"use": "beginners",    "icon": "tool",     "provider": {"en": "CyberGhost", "sv": "CyberGhost"}},
    {"use": "torrenting",   "icon": "download", "provider": {"en": "Private Internet Access", "sv": "Private Internet Access"}},
    {"use": "anonymity",    "icon": "ghost",    "provider": {"en": "Mullvad", "sv": "Mullvad"}},
    {"use": "travel",       "icon": "plane",    "provider": {"en": "ExpressVPN", "sv": "ExpressVPN"}},
    {"use": "free",         "icon": "gift",     "provider": {"en": "Windscribe", "sv": "Windscribe"}},
    {"use": "transparency", "icon": "eye",      "provider": {"en": "IVPN", "sv": "IVPN"}},
]

# Extra sprite symbols needed only on a few pages are defined inline below.
EXTRA_SPRITE = """
  <symbol id="i-download" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M12 3v12M7.5 10.5 12 15l4.5-4.5M4 20h16"/>
  </symbol>
  <symbol id="i-gift" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M20 12v9H4v-9M2 8h20v4H2zM12 21V8M12 8H7.5a2.5 2.5 0 1 1 0-5C11 3 12 8 12 8zM12 8h4.5a2.5 2.5 0 1 0 0-5C13 3 12 8 12 8z"/>
  </symbol>
  <symbol id="i-play" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="9"/>
    <path d="M10 8.5l6 3.5-6 3.5z"/>
  </symbol>
  <symbol id="i-gamepad" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <rect x="2.5" y="7.5" width="19" height="9" rx="4.5"/>
    <path d="M7 10.5v3M5.5 12h3M16 11h.01M18 13h.01"/>
  </symbol>
  <symbol id="i-phone" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <rect x="7" y="2.5" width="10" height="19" rx="2.5"/>
    <path d="M11 18.5h2"/>
  </symbol>
  <symbol id="i-robot" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <rect x="4.5" y="8.5" width="15" height="10.5" rx="3"/>
    <path d="M12 4.5v4M9.5 13.5h.01M14.5 13.5h.01M9.5 16.5h5"/>
  </symbol>
  <symbol id="i-monitor" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <rect x="2.5" y="4" width="19" height="12" rx="2"/>
    <path d="M8.5 20h7M12 16v4"/>
  </symbol>
  <symbol id="i-laptop" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <rect x="4.5" y="5.5" width="15" height="10" rx="1.5"/>
    <path d="M2.5 18.5h19"/>
  </symbol>
  <symbol id="i-router" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <rect x="3" y="13" width="18" height="7" rx="2"/>
    <path d="M7 16.5h.01M11 16.5h.01M12 10V7M8.8 8.4a4.5 4.5 0 0 1 6.4 0"/>
  </symbol>
"""


# ---------------------------------------------------------------------------
# Context
# ---------------------------------------------------------------------------


def load_json(name: str):
    with open(os.path.join(DATA, name), encoding="utf-8") as fh:
        return json.load(fh)


def make_context() -> dict:
    providers_doc = load_json("providers.json")
    affiliates = load_json("affiliates.json")
    providers = providers_doc["providers"]
    weights = providers_doc["_meta"]["scoringModel"]["weights"]

    # The site claims the order comes from these published weights, so the
    # number in the "#" column has to be that same order — otherwise the table
    # reads out of order down the page. providers.json's own `rank`
    # only breaks ties between two providers with an identical score.
    for i, p in enumerate(
        sorted(providers, key=lambda q: (-weighted_score(q, weights), q["rank"])),
        start=1,
    ):
        p["rank"] = i

    with open(os.path.join(ROOT, "assets", "img", "icons.svg"), encoding="utf-8") as fh:
        sprite = fh.read()

    ctx: dict = {
        "site": SITE,
        "providers": providers,
        "providers_meta": providers_doc["_meta"],
        "affiliates": affiliates,
        "use_case_by_id": {u["id"]: u for u in providers_doc["useCases"]},
        "use_case_picks": USE_CASE_PICKS,
        "build_date": BUILD_DATE,
        "build_year": BUILD_DATE[:4],
        "sprite": sprite + EXTRA_SPRITE,
        "weights": weights,
    }

    def t(key: str, lang: str) -> str:
        return e(C.t(key, lang))

    def th(key: str, lang: str) -> str:
        """Raw, unescaped — only for strings that intentionally contain HTML."""
        return C.S[key][lang]

    def path(href: str, lang: str) -> str:
        depth = ctx["depth"]
        return ("../" * depth) + f"{lang}/{href}"

    def switch(other_lang: str) -> str:
        rel = ctx["rel_path"]
        # index.html is linked as a directory URL to match the canonical,
        # including folder pages such as best-vpn-for/streaming/index.html
        suffix = rel[:-len("index.html")] if rel.endswith("index.html") else rel
        return ("../" * ctx["depth"]) + f"{other_lang}/{suffix}"

    def alt_path(rel: str, lang: str) -> str:
        other = "sv" if lang == "en" else "en"
        return f"{other}/{rel}"

    def absolute(href: str) -> str:
        """Root-relative href → absolute URL, resolving any ../ segments."""
        out: list[str] = []
        for seg in href.split("/"):
            if seg in ("", "."):
                continue
            if seg == "..":
                if out:
                    out.pop()
                continue
            out.append(seg)
        # A directory href keeps its trailing slash, so breadcrumb URLs match
        # the canonical instead of pointing at a path the host would redirect.
        tail = "/" if href.endswith("/") and out else ""
        return SITE["origin"].rstrip("/") + "/" + "/".join(out) + tail

    def asset(rel: str) -> str:
        return ("../" * ctx["depth"]) + f"assets/{rel}"

    ctx.update({
        "t": t, "th": th, "path": path, "switch": switch,
        "alt_path": alt_path, "absolute": absolute, "asset": asset,
        "depth": 0, "rel_path": "index.html", "lang": "en",
    })
    return ctx


def enter(ctx: dict, lang: str, rel: str) -> None:
    ctx["lang"] = lang
    ctx["rel_path"] = rel
    # Paths are resolved relative to the page directory. A page at
    # en/vpn/nordvpn.html sits two directories below the site root:
    # one for the language and one for the section.
    ctx["depth"] = rel.count("/") + 1


# ---------------------------------------------------------------------------
# Shared page sections
# ---------------------------------------------------------------------------


def t(ctx, key, lang):
    return ctx["t"](key, lang)


def benefits_grid(ctx, lang: str) -> str:
    cards = []
    for icon_name, title, body in BENEFITS[lang]:
        cards.append(f"""<div class="card">
  <div class="ring-row">
    <span class="usecase__top" style="flex:none">{icon(icon_name)}</span>
    <h3 style="font-size:1rem">{e(title)}</h3>
  </div>
  <p class="muted" style="font-size:.92rem;margin-top:.6rem">{e(body)}</p>
</div>""")
    return f'<div class="card-grid">{"".join(cards)}</div>'


def weights_table(ctx, lang: str) -> str:
    rows = []
    for key, w in sorted(ctx["weights"].items(), key=lambda kv: -kv[1]):
        meta = R.SCORE_META[key]
        rows.append(f"""<tr>
  <th scope="row">{e(meta[lang])}</th>
  <td class="num">{int(w * 100)} %</td>
  <td class="muted">{e(SCORE_DEFS[key][lang][1])}</td>
</tr>""")
    return f"""<div class="table-wrap">
  <table class="cmp" style="min-width:0">
    <caption>{e(HOW_WE_TEST[lang]["weights_table_caption"])}</caption>
    <thead><tr>
      <th scope="col">{t(ctx, "col_criterion", lang)}</th>
      <th scope="col">{t(ctx, "col_weight", lang)}</th>
      <th scope="col">{t(ctx, "score_basis", lang)}</th>
    </tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</div>"""


def server_label(p: dict, lang: str) -> str:
    """Server count, or an honest 'not published' when the provider states none."""
    if p.get("servers") is None:
        return C.S["not_published"][lang]
    return f"{p['servers']:,}"


def review_index(ctx: dict, lang: str) -> str:
    weights = ctx["weights"]
    ordered = ranked(ctx["providers"], weights)
    cards = []
    for p in ordered:
        total = weighted_score(p, weights)
        plan = cheapest_plan(p)
        cur = R.CURRENCY[lang]
        monthly = plan["monthlySEK"] if cur == "SEK" else plan["monthlyUSD"]
        totalp = plan["totalSEK"] if cur == "SEK" else plan["totalUSD"]
        term = plan["term"][lang]
        cards.append(f"""<article class="card" style="display:flex;gap:1.25rem;align-items:flex-start;flex-wrap:wrap">
  <div style="flex:none">{score_ring(total, "ring--lg", lang)}</div>
  <div style="flex:1 1 260px;min-width:0">
    <div style="display:flex;gap:.9rem;align-items:center;flex-wrap:wrap">
      {R.monogram(ctx, p, "mono-badge--sm")}
      <h2 style="margin:0;font-size:1.1rem"><a href="{ctx["path"]("vpn/" + p["slug"] + ".html", lang)}"
         style="color:inherit;text-decoration:none">{e(p["name"])}</a></h2>
      <span class="badge{' badge--gold' if p["rank"] == 1 else ''}">{e(p["badge"][lang])}</span>
    </div>
    <p class="muted" style="font-size:.9rem;margin-top:.5rem">{e(p["tagline"][lang])}</p>
    <div class="chip-row" style="margin-top:.7rem">
      <span class="chip">{icon("tag")}{e(money_prec(monthly, lang, cur))}{t(ctx, "per_month", lang)}</span>
      <span class="chip">{icon("clock")}{e(money(totalp, lang, cur))} / {e(term)}</span>
      <span class="chip">{icon("globe")}{server_label(p, lang)} / {p["countries"]}</span>
    </div>
  </div>
  <div style="flex:none">{R.cta(ctx, lang, p)}</div>
</article>""")
    return f'<div class="stack">{"".join(cards)}</div>'


def compare_table(ctx, lang: str, providers: list, *, with_tools: bool = False) -> str:
    """Generate the comparison table + optional mobile card view."""
    cur = R.CURRENCY[lang]
    o_cur = R.alt_currency(cur)
    use_cases = ctx["use_case_by_id"]

    def yes(cond, lg):
        if cond:
            return (f'<span class="pill-mini pill-mini--yes">{icon("check")}'
                    f'{t(ctx, "yes", lg)}</span>')
        return (f'<span class="pill-mini pill-mini--no">{icon("minus-circle")}'
                f'{t(ctx, "no", lg)}</span>')

    eye_map = {
        "none": ("badge--good", "eye_none"),
        "none-eu": ("badge--good", "eye_none"),
        "5-eyes": ("badge--warn", "eye_5"),
        "9-eyes": ("badge--warn", "eye_9"),
        "14-eyes": ("badge--warn", "eye_14"),
    }

    # ----- TABLE ROWS -----
    rows = []
    for p in providers:
        total = weighted_score(p, ctx["weights"])
        plan = cheapest_plan(p)
        monthly = plan["monthlySEK"] if cur == "SEK" else plan["monthlyUSD"]
        totalp = plan["totalSEK"] if cur == "SEK" else plan["totalUSD"]
        o_monthly = plan["monthlyUSD"] if cur == "SEK" else plan["monthlySEK"]
        o_total = plan["totalUSD"] if cur == "SEK" else plan["totalSEK"]

        eye_cls, eye_key = eye_map.get(p["eyesAlliance"], ("", "eye_none"))

        # Compressed audit: just count + latest auditor, or "—" if none
        if p["audit"]["count"]:
            # Split on both commas and " and " to get individual firms
            import re
            firms = [f.strip() for f in re.split(r',|\s+and\s+', p["audit"]["firm"]) if f.strip()]
            latest = firms[0] if firms else p["audit"]["firm"]
            audit_cell = f'<span class="audit-badge">{p["audit"]["count"]}x</span> <span class="audit-firm">{e(latest)}</span>'
        else:
            audit_cell = f'<span class="faint audit-none">{t(ctx, "audit_none", lang)}</span>' 

        cases = " ".join(p["bestFor"])
        devices = t(ctx, "unlimited", lang) if p["devices"] == -1 else str(p["devices"])
        # Sort key for the devices column: unlimited sorts above every finite
        # count. A sentinel of 99 keeps it a plain number so the descending
        # sort puts it first and the ascending sort last.
        device_sort = 99 if p["devices"] < 0 else p["devices"]

        # Get affiliate URL for the provider
        aff_url, is_aff = R.affiliate_url(ctx, p["id"])
        aff_rel = (ctx["affiliates"]["settings"]["relAttribute"] if is_aff
                   else "nofollow noopener")
        aff_tag = (R.affiliate_label(ctx, lang) if is_aff
                   else t(ctx, "external_link", lang))

        # Swedish price advertising: the total must sit next to the per-month
        # figure, so the cell never shows a monthly price on its own.
        total_line = (f"{money(totalp, lang, cur)} "
                      + C.S["for_term"][lang].format(term=plan["term"][lang]))
        alt_frag = (f' · <span class="price-alt">{e(money(o_total, lang, o_cur))}</span>'
                    if R.show_alt(lang) else "")

        row_class = ' class="top-pick"' if p["rank"] == 1 else ''
        rows.append(
            f'<tr{row_class} data-key="{e(p["id"])}"'
            f' data-name="{e(p["name"])}"'
            f' data-rank="{p["rank"]}"'
            f' data-servers="{p["servers"] or 0}"'
            f' data-headquarters="{e(p["headquarters"])}"'
            f' data-cases="{e(" ".join(p["bestFor"]))}"'
            f' data-free="{'yes' if p["freeTier"] else 'no'}"'
            f' data-unlimited="{'yes' if p["devices"] == -1 else 'no'}"'
            f' data-opensource="{'yes' if p["openSourceApps"] else 'no'}"'
            f' data-anonymous="{'yes' if p["anonymousSignup"] else 'no'}"'
            f'>'
            f'<td class="num" data-key="rank" data-sort="{p["rank"]}">#{p["rank"]}</td>'
            f'<td class="cell-provider" data-key="provider" data-sort="0">'
            f'<span class="cta-tag">{e(aff_tag)}</span>'
            f'<a href="{e(aff_url)}" target="_blank" rel="{e(aff_rel)}" class="provider-link" data-provider="{e(p["id"])}" data-affiliate="{str(is_aff).lower()}">'
            f'{R.monogram(ctx, p, "mono-badge--sm")}'
            f'<span class="provider-name">{e(p["name"])}</span>'
            f'</a>'
            f'<span class="provider-badge badge{' badge--gold' if p["rank"] == 1 else ''}">{e(p["badge"][lang])}</span>'
            f'</td>'
            f'<td data-key="score" data-sort="{total}">'
            f'<span class="cell-score">{score_ring(total, "ring--sm", lang)}</span>'
            f'</td>'
            f'<td class="cell-price" data-key="price_month" data-sort="{monthly}">'
            f'<div class="price-wrap">'
            f'<span class="price-primary">{e(money_prec(monthly, lang, cur))}</span>'
            f'<span class="price-meta">'
            f'<span class="price-secondary">{e(total_line)}</span>'
            f'{alt_frag}'
            f'</span>'
            f'</div>'
            f'</td>'
            f'<td class="num" data-key="devices" data-sort="{device_sort}">{e(devices)}</td>'
            f'<td class="cell-jurisdiction" data-key="jurisdiction" data-sort="{'0' if p["eyesAlliance"] in ('none', 'none-eu') else '1'}">'
            f'<span class="country">{e(p["headquarters"])}</span><br>'
            f'<span class="badge {eye_cls}">{t(ctx, eye_key, lang)}</span>'
            f'</td>'
            f'<td data-key="audits" data-sort="{p["audit"]["count"]}" class="faint">{audit_cell}</td>'
            f'<td data-key="free" data-sort="{1 if p["freeTier"] else 0}">{yes(p["freeTier"], lang)}</td>'
            f'<td class="num nowrap" data-key="guarantee" data-sort="{p["moneyBackDays"]}">'
            f'{p["moneyBackDays"]} {t(ctx, "guarantee_unit", lang)}</td>'
            f'</tr>'
        )

    # ----- TABLE TOOLS -----
    tools = ""
    if with_tools:
        usecase_options = "".join(
            f'<option value="{e(u["id"])}">{e(u[lang])}</option>'
            for u in ctx["use_case_order"]
        )
        sort_options = [
            ("score:desc", t(ctx, "sort_score_desc", lang)),
            ("score:asc", t(ctx, "sort_score_asc", lang)),
            ("price_month:asc", t(ctx, "sort_price_asc", lang)),
            ("price_month:desc", t(ctx, "sort_price_desc", lang)),
            ("servers:desc", t(ctx, "sort_servers_desc", lang)),
            ("devices:desc", t(ctx, "sort_devices_desc", lang)),
            ("free:desc", t(ctx, "sort_free_desc", lang)),
            ("guarantee:desc", t(ctx, "sort_guarantee_desc", lang)),
            ("rank:asc", t(ctx, "sort_rank_asc", lang)),
        ]
        sort_opts_html = "".join(
            f'<option value="{e(v)}"{" selected" if v == "score:desc" else ""}>{e(l)}</option>'
            for v, l in sort_options
        )

        tools = f"""<div class="table-tools">
  <div class="search">
    {icon("search")}
    <label class="sr-only" for="cmp-search">{t(ctx, "filter_search", lang)}</label>
    <input id="cmp-search" type="search" placeholder="{t(ctx, "filter_search", lang)}" autocomplete="off">
  </div>
  <div class="select-wrap">
    <label class="sr-only" for="cmp-sort">{t(ctx, "sort_label", lang)}</label>
    <select class="sel" id="cmp-sort">{sort_opts_html}</select>
    <svg aria-hidden="true"><use href="#i-chevron-down"/></svg>
  </div>
  <div class="select-wrap">
    <label class="sr-only" for="cmp-usecase">{t(ctx, "filter_usecase", lang)}</label>
    <select class="sel" id="cmp-usecase">
      <option value="">{t(ctx, "filter_usecase", lang)}</option>
      {"".join(f'<option value="{e(u["id"])}">{e(u[lang])}</option>' for u in ctx["use_case_order"])}
    </select>
    <svg aria-hidden="true"><use href="#i-chevron-down"/></svg>
  </div>
  <div class="select-wrap">
    <label class="sr-only" for="cmp-free">{t(ctx, "filter_feature", lang)}</label>
    <select class="sel" id="cmp-free">
      <option value="">{t(ctx, "filter_feature", lang)}</option>
      <option value="yes">{t(ctx, "feature_free", lang)}</option>
      <option value="unlimited">{t(ctx, "feature_unlimited", lang)}</option>
      <option value="open-source">{t(ctx, "feature_open_source", lang)}</option>
      <option value="anonymous">{t(ctx, "feature_anonymous", lang)}</option>
    </select>
    <svg aria-hidden="true"><use href="#i-chevron-down"/></svg>
  </div>
  <button class="btn btn--ghost" type="button" id="cmp-reset">{t(ctx, "reset_filters", lang)}</button>
  <button class="btn btn--ghost" type="button" id="cmp-share"
          data-copied="{t(ctx, "copied", lang)}"
          aria-label="{t(ctx, "copy_link", lang)}">
    {icon("link")} {t(ctx, "copy_link", lang)}
  </button>
</div>"""

    # ----- TABLE HEAD -----
    # Single source for the header row: sortable cells carry a data-key that
    # must match a td[data-key] in the body, or sorting silently does nothing.
    columns = [
        ("#", "rank", "sortable"),
        (t(ctx, "col_provider", lang), "provider", ""),
        (t(ctx, "col_score", lang), "score", "sortable"),
        (t(ctx, "col_price", lang), "price_month", "sortable"),
        (t(ctx, "col_devices", lang), "devices", "sortable"),
        (t(ctx, "col_jurisdiction", lang), "jurisdiction", "sortable"),
        (t(ctx, "col_audit", lang), "audits", "sortable"),
        (t(ctx, "col_free", lang), "free", "sortable"),
        (t(ctx, "col_guarantee", lang), "guarantee", "sortable"),
    ]
    thead_html = "".join(
        '<th scope="col"'
        + (f' class="{cls}"' if cls else "")
        + f' data-key="{key}"'
        + (' aria-sort="none"' if cls else "")
        + f">{label}</th>"
        for label, key, cls in columns
    )

    # ----- CARD VIEW (mobile) -----
    cards = []
    for p in providers:
        total = weighted_score(p, ctx["weights"])
        plan = cheapest_plan(p)
        monthly = plan["monthlySEK"] if R.CURRENCY[lang] == "SEK" else plan["monthlyUSD"]
        totalp = plan["totalSEK"] if R.CURRENCY[lang] == "SEK" else plan["totalUSD"]
        o_monthly = plan["monthlyUSD"] if R.CURRENCY[lang] == "SEK" else plan["monthlySEK"]
        o_total = plan["totalUSD"] if R.CURRENCY[lang] == "SEK" else plan["totalSEK"]
        eye_cls, eye_key = eye_map.get(p["eyesAlliance"], ("", "eye_none"))
        # Compressed audit: just count + latest auditor, or "—" if none
        if p["audit"]["count"]:
            # Split on both commas and " and " to get individual firms
            import re
            firms = [f.strip() for f in re.split(r',|\s+and\s+', p["audit"]["firm"]) if f.strip()]
            latest = firms[0] if firms else p["audit"]["firm"]
            audit_cell = f'<span class="audit-badge">{p["audit"]["count"]}x</span> <span class="audit-firm">{e(latest)}</span>'
        else:
            audit_cell = f'<span class="faint audit-none">{t(ctx, "audit_none", lang)}</span>' 
        devices = t(ctx, "unlimited", lang) if p["devices"] == -1 else str(p["devices"])

        cur = R.CURRENCY[lang]
        o_cur = "USD" if cur == "SEK" else "SEK"
        o_monthly = plan["monthlyUSD"] if cur == "SEK" else plan["monthlySEK"]
        o_total = plan["totalUSD"] if cur == "SEK" else plan["totalSEK"]
        alt_monthly = (f' <span class="faint">({e(money_prec(o_monthly, lang, o_cur))})</span>'
                       if R.show_alt(lang) else "")

        cards.append(
            f'<article class="cmp-card" data-key="{e(p["id"])}"'
            f' data-name="{e(p["name"])}"'
            f' data-rank="{p["rank"]}"'
            f' data-servers="{p["servers"] or 0}"'
            f' data-headquarters="{e(p["headquarters"])}"'
            f' data-cases="{e(" ".join(p["bestFor"]))}"'
            f' data-free="{'yes' if p["freeTier"] else 'no'}"'
            f' data-unlimited="{'yes' if p["devices"] == -1 else 'no'}"'
            f' data-opensource="{'yes' if p["openSourceApps"] else 'no'}"'
            f' data-anonymous="{'yes' if p["anonymousSignup"] else 'no'}"'
            f'>'
            f'<div class="cmp-card__rank">#{p["rank"]}</div>'
            f'<div class="cmp-card__provider">'
            f'{R.monogram(ctx, p, "mono-badge--sm")}'
            f'<div>'
            f'<a href="{ctx["path"]("vpn/" + p["slug"] + ".html", lang)}" style="color:inherit;text-decoration:none;font-weight:700;font-size:1rem">{e(p["name"])}</a>'
            f'<span class="cmp-card__badge badge{' badge--gold' if p["rank"] == 1 else ''}">{e(p["badge"][lang])}</span>'
            f'</div>'
            f'</div>'
            f'<div class="cmp-card__score">'
            f'{score_ring(weighted_score(p, ctx["weights"]), "ring--sm", lang)}'
            f'<span class="cmp-card__score-label">{t(ctx, "our_score", lang)}</span>'
            f'</div>'
            f'<div class="cmp-card__details">'
            f'<div class="cmp-card__detail">'
            f'<span class="cmp-card__detail-label">{t(ctx, "col_price", lang)}</span>'
            f'<span class="cmp-card__detail-value">{e(money_prec(monthly, lang, cur))}{alt_monthly}</span>'
            f'</div>'
            f'<div class="cmp-card__detail">'
            f'<span class="cmp-card__detail-label">{t(ctx, "col_total", lang)}</span>'
            f'<span class="cmp-card__detail-value">{e(money(totalp, lang, cur))} '
            f'<span class="faint">{e(plan["term"][lang])}</span></span>'
            f'</div>'
            f'<div class="cmp-card__detail">'
            f'<span class="cmp-card__detail-label">{t(ctx, "col_devices", lang)}</span>'
            f'<span class="cmp-card__detail-value">{e(devices)}</span>'
            f'</div>'
            f'<div class="cmp-card__detail">'
            f'<span class="cmp-card__detail-label">{t(ctx, "col_jurisdiction", lang)}</span>'
            f'<span class="cmp-card__detail-value">{e(p["headquarters"])} <span class="badge {eye_cls}">{t(ctx, eye_key, lang)}</span></span>'
            f'</div>'
            f'<div class="cmp-card__detail">'
            f'<span class="cmp-card__detail-label">{t(ctx, "col_audit", lang)}</span>'
            f'<span class="cmp-card__detail-value">{audit_cell}</span>'
            f'</div>'
            f'<div class="cmp-card__detail">'
            f'<span class="cmp-card__detail-label">{t(ctx, "col_free", lang)}</span>'
            f'<span class="cmp-card__detail-value">{yes(p["freeTier"], lang)}</span>'
            f'</div>'
            f'<div class="cmp-card__detail">'
            f'<span class="cmp-card__detail-label">{t(ctx, "col_guarantee", lang)}</span>'
            f'<span class="cmp-card__detail-value">{p["moneyBackDays"]} {t(ctx, "guarantee_unit", lang)}</span>'
            f'</div>'
            f'</div>'
            f'<div class="cmp-card__cta">'
            f'<span class="faint">{e(money(cheapest_plan(p)["totalSEK"] if R.CURRENCY[lang]=="SEK" else cheapest_plan(p)["totalUSD"], lang, R.CURRENCY[lang]))} {e(t(ctx, "for_term", lang).format(term=plan["term"][lang]))}</span>'
            f'{R.cta(ctx, lang, p)}'
            f'</div>'
            f'</article>'
        )

    cards_html = f'<div class="cmp-cards">{"".join(cards)}</div>' if cards else ''

    return f"""{tools}
<div class="table-wrap">
  <table class="cmp" id="cmp-table">
    <caption id="cmp-count">{e(len(providers))} {t(ctx, "results", lang)}</caption>
    <thead><tr>{thead_html}</tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</div>
{cards_html}
<p class="cmp__empty" id="cmp-empty" hidden>{e(COMPARE[lang]["empty"])}</p>
<p class="faint" style="margin-top:.9rem" id="cmp-status"
   data-showing-all="{t(ctx, "showing_all", lang)}"
   data-showing="{t(ctx, "showing", lang)}"
   data-providers="{t(ctx, "results", lang)}"></p>"""

def usecase_pick_blocks(ctx, lang: str, picks: list) -> str:
    blocks = []
    for pick in picks:
        uc = ctx["use_case_by_id"][pick["use"]]
        blocks.append(f"""<div class="card">
  <div class="usecase__top" style="margin-bottom:.6rem">{icon(pick["icon"])}{e(uc[lang])}</div>
  <p class="faint">{t(ctx, "best_option", lang)}</p>
  <h3 style="font-size:1.05rem;margin-bottom:.5rem">{e(pick["provider"][lang])}</h3>
</div>""")
    return f'<div class="card-grid">{"".join(blocks)}</div>'


def cta_band(ctx, lang: str, *, title: str, body: str, label: str,
             href: str | None = None, provider: dict | None = None) -> str:
    """Closing call to action.

    `provider` renders a compliant affiliate CTA (Ad/Annons tag, target and
    rel set correctly); `href` is for an internal link such as the compare
    page and must never be an outbound commercial URL.
    """
    if provider is not None:
        action = R.cta(ctx, lang, provider, label=label, block=True)
    else:
        action = (f'<a class="btn btn--primary btn--lg" href="{e(href)}">'
                  f'{e(label)} {icon("arrow-right")}</a>')
    return f"""<section class="cta-band">
  <div class="wrap">
    <h2>{e(title)}</h2>
    <p>{e(body)}</p>
    <div class="hero__actions">
      {action}
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------


def page_home(ctx, lang):
    rel = "index.html"
    enter(ctx, lang, rel)
    h = HOME[lang]
    # Sorted by the published weighted score so the preview matches the
    # compare page exactly — two different orders on two pages reads as a bug.
    providers = ranked(ctx["providers"], ctx["weights"])
    weights = ctx["weights"]

    top3 = providers[:3]
    top3_cards = "".join(
        R.pcard(ctx, lang, p) for p in top3
    )

    trust = "".join(
        f"<span>{icon('check')}{e(item.format(date=R.long_date(ctx['build_date'], lang)))}</span>"
        for item in h["trust"]
    )

    faq_items = [(q, f"<p>{a}</p>") for q, a in FAQ_GENERAL[lang][:4]]
    general_faq_links = C.S["all_faq"][lang]
    guide_tiles = "".join(topic_tile(ctx, lang, tp) for tp in load_topics())
    explainer_tiles = "".join(explained_tile(ctx, lang, tp)
                              for tp in load_explained())

    title = f"{h['h1']} | {SITE['name']}"
    desc = h["lede"][:180]

    body = f"""<main id="main">
<section class="hero">
  <div class="wrap hero__content">
    <img class="hero__logo" src="{ctx["asset"]("img/vpn-pick-shield.png")}"
         width="226" height="260" alt="" fetchpriority="high" decoding="async">
    <span class="eyebrow">{icon("shield")} {e(h["eyebrow"])}</span>
    <h1>{e(h["h1"])}</h1>
    <p class="lede">{e(h["lede"])}</p>
    <div class="hero__trust">{trust}</div>
    <div class="hero__actions">
      <a class="btn btn--primary btn--lg" href="{ctx["path"]("compare.html", lang)}">
        {e(h["cta_primary"])} {icon("arrow-right")}
      </a>
      <a class="btn btn--ghost btn--lg" href="{ctx["path"]("how-we-test.html", lang)}">
        {e(h["cta_secondary"])}
      </a>
    </div>
  </div>
</section>

<section class="section" id="picks">
  <div class="wrap">
    <header class="section-head">
      <span class="eyebrow">{icon("star")} {e(h["top_eyebrow"])}</span>
      <h2>{e(h["top_title"])}</h2>
      <p class="lede">{e(h["top_lede"])}</p>
    </header>
    <div class="card-grid top-picks">{top3_cards}</div>
    <p class="section-footer">
      <a href="{ctx["path"]("reviews.html", lang)}" class="btn btn--ghost btn--sm">
        {e(C.S["all_reviews"][lang])} {icon("arrow-right")}
      </a>
    </p>
  </div>
</section>

<section class="section section--alt" id="compare-preview">
  <div class="wrap">
    <header class="section-head">
      <span class="eyebrow">{icon("gauge")} {e(h["compare_eyebrow"])}</span>
      <h2>{e(h["compare_title"])}</h2>
      <p class="lede">{e(h["compare_lede"])}</p>
    </header>
    {compare_table(ctx, lang, providers)}
    <p class="section-footer">
      <a class="btn btn--primary" href="{ctx["path"]("compare.html", lang)}">
        {e(h["compare_cta"])} {icon("arrow-right")}
      </a>
    </p>
  </div>
</section>

<section class="section" id="why-trust">
  <div class="wrap">
    <header class="section-head">
      <span class="eyebrow">{icon("doc")} {e(h["why_title"])}</span>
      <h2>{e(h["why_title"])}</h2>
      <p class="lede">{e(h["why_lede"])}</p>
    </header>
    {benefits_grid(ctx, lang)}
  </div>
</section>

<section class="section section--sm" id="use-cases">
  <div class="wrap">
    <header class="section-head">
      <span class="eyebrow">{icon("users")} {e(h["usecase_title"])}</span>
      <h2>{e(h["usecase_title"])}</h2>
      <p class="lede">{e(h["usecase_lede"])}</p>
    </header>
    {R.usecase_tiles(ctx, lang)}
  </div>
</section>

<section class="section section--sm" id="best-vpn-for">
  <div class="wrap">
    <header class="section-head">
      <span class="eyebrow">{icon("doc")} {e(C.S["bfv_hub_link"][lang])}</span>
      <h2>{e(C.S["home_guides_title"][lang])}</h2>
      <p class="lede">{e(C.S["home_guides_lede"][lang])}</p>
    </header>
    <div class="card-grid">{guide_tiles}</div>
    <p class="section-footer">
      <a href="{ctx["path"]("best-vpn-for/", lang)}" class="btn btn--ghost btn--sm">
        {e(C.S["bfv_hub_link"][lang])} {icon("arrow-right")}
      </a>
    </p>
  </div>
</section>

<section class="section section--sm" id="explained">
  <div class="wrap">
    <header class="section-head">
      <span class="eyebrow">{icon("info")} {e(C.S["explained_hub_link"][lang])}</span>
      <h2>{e(C.S["explained_home_title"][lang])}</h2>
      <p class="lede">{e(C.S["explained_home_lede"][lang])}</p>
    </header>
    <div class="card-grid">{explainer_tiles}</div>
    <p class="section-footer">
      <a href="{ctx["path"]("vpn-explained/", lang)}" class="btn btn--ghost btn--sm">
        {e(C.S["explained_hub_link"][lang])} {icon("arrow-right")}
      </a>
    </p>
  </div>
</section>

<section class="section section--sm" id="faq-preview">
  <div class="wrap">
    <header class="section-head">
      <span class="eyebrow">{icon("info")} {e(h["faq_title"])}</span>
      <h2>{e(h["faq_title"])}</h2>
    </header>
    <div class="wrap-tight" style="padding-inline:0">
      {R.faq_block(faq_items, first_open=True)}
      <p class="section-footer">
        <a href="{ctx["path"]("faq.html", lang)}" class="btn btn--ghost btn--sm">
          {e(general_faq_links)} {icon("arrow-right")}
        </a>
      </p>
    </div>
  </div>
</section>

{cta_band(ctx, lang,
    title=C.S["cta_home_title"][lang],
    body=C.S["cta_home_body"][lang],
    label=h["compare_cta"],
    href=ctx["path"]("compare.html", lang))}
</main>"""

    ld = [
        R.ld_org(ctx),
        R.ld_itemlist(ctx, lang, ranked(ctx["providers"], weights),
                      C.S["ld_itemlist_home"][lang]),
        R.ld_faqpage(FAQ_GENERAL[lang][:5]),
    ]
    return assemble(ctx, lang, rel, title, desc, body, jsonld=ld, nav_active="",
                    script="compare.js")


def page_compare(ctx, lang):
    rel = "compare.html"
    enter(ctx, lang, rel)
    c = COMPARE[lang]
    providers = ranked(ctx["providers"], ctx["weights"])

    notes = "".join(
        f'<article class="card note-card"><div class="note-icon">{icon(ic)}</div>'
        f'<div class="note-content"><h3>{e(title)}</h3>'
        f'<p>{e(body)}</p></div></article>'
        for ic, title, body in c["notes"]
    )

    faq_items = [(q, f"<p>{a}</p>") for q, a in COMPARE_FAQ[lang]]

    body = f"""<main id="main">
<section class="hero hero--page">
  <div class="wrap">
    <span class="eyebrow">{icon("gauge")} {e(c["eyebrow"])}</span>
    <h1>{e(c["h1"])}</h1>
    <p class="lede">{e(c["lede"])}</p>
    <p class="hero__meta">
      {icon("refresh")} {e(t(ctx, "verified_on", lang).format(
          date=R.long_date(ctx["build_date"], lang)))}
    </p>
  </div>
</section>

<section class="section" id="compare-table">
  <div class="wrap">
    {compare_table(ctx, lang, providers, with_tools=True)}
    <p class="section-footer">
      {icon("refresh")} {e(t(ctx, "verified_on", lang).format(
          date=R.long_date(ctx["build_date"], lang)))}
    </p>
  </div>
</section>

<section class="section section--alt" id="compare-notes">
  <div class="wrap">
    <header class="section-head">
      <span class="eyebrow">{icon("doc")} {e(c["notes_title"])}</span>
      <h2>{e(c["notes_title"])}</h2>
    </header>
    <div class="card-grid notes-grid">{notes}</div>
  </div>
</section>

<section class="section section--sm" id="disclosure">
  <div class="wrap wrap-tight">
    <header class="section-head"><h2>{e(c["disclosure_title"])}</h2></header>
    <p class="muted">{e(c["disclosure"])}</p>
    <p class="section-footer">
      <a href="{ctx["path"]("about.html#disclosure", lang)}" class="btn btn--ghost btn--sm">
        {e(C.S["footer_disclosure"][lang])} {icon("arrow-right")}
      </a>
    </p>
  </div>
</section>

<section class="section section--sm" id="faq">
  <div class="wrap wrap-tight">
    <header class="section-head"><h2>{e(c["faq_title"])}</h2></header>
    <div style="margin-top:1.5rem">{R.faq_block(faq_items)}</div>
    <p class="section-footer">
      <a href="{ctx["path"]("faq.html", lang)}" class="btn btn--ghost btn--sm">
        {e(C.S["all_faq"][lang])} {icon("arrow-right")}
      </a>
    </p>
  </div>
</section>
</main>"""

    ld = [
        R.ld_org(ctx),
        R.ld_itemlist(ctx, lang, providers, c["h1"]),
        R.ld_faqpage(COMPARE_FAQ[lang]),
    ]
    title = f"{c['h1']} ({ctx['build_year']}) | {SITE['name']}"
    return assemble(ctx, lang, rel, title, c["lede"][:180], body,
                    jsonld=ld, nav_active="compare.html", script="compare.js")
def page_reviews_index(ctx, lang):
    rel = "reviews.html"
    enter(ctx, lang, rel)
    providers = ranked(ctx["providers"], ctx["weights"])

    title_s = C.S["reviews_index_title"][lang]
    lede_s = C.S["reviews_index_lede"][lang]

    body = f"""<main id="main">
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">{icon("doc")} {e(C.S["reviews_index_eyebrow"][lang])}</span>
      <h1>{e(title_s)}</h1>
      <p class="lede">{e(lede_s)}</p>
    </div>
    {review_index(ctx, lang)}
    <p class="faint" style="margin-top:2rem">
      {icon("scale")} {e(C.S["score_model_foot"][lang])}
      <a href="{ctx["path"]("how-we-test.html", lang)}">{e(HOME[lang]["method_cta"])} →</a>
    </p>
  </div>
</section>
</main>"""

    ld = [R.ld_org(ctx), R.ld_itemlist(ctx, lang, providers, title_s)]
    return assemble(ctx, lang, rel, f"{title_s} | {SITE['name']}",
                    lede_s[:180], body, jsonld=ld, nav_active="reviews.html")


def page_review(ctx, lang, p):
    rel = f"vpn/{p['slug']}.html"
    enter(ctx, lang, rel)
    r = REVIEW[lang]
    weights = ctx["weights"]
    total = weighted_score(p, weights)

    cur = R.CURRENCY[lang]
    o_cur = R.alt_currency(cur)

    def yesno(cond, lg):
        if cond:
            return (f'<span class="pill-mini pill-mini--yes">{icon("check")}'
                    f'{t(ctx, "yes", lg)}</span>')
        return (f'<span class="pill-mini pill-mini--no">{icon("minus")}'
                f'{t(ctx, "no", lg)}</span>')

    # ---- privacy facts
    eye_map = {
        "none": ("badge--good", "eye_none"),
        "none-eu": ("badge--good", "eye_none"),
        "5-eyes": ("badge--warn", "eye_5"),
        "9-eyes": ("badge--warn", "eye_9"),
        "14-eyes": ("badge--warn", "eye_14"),
    }
    eye_cls, eye_key = eye_map.get(p["eyesAlliance"], ("", "eye_none"))

    privacy_rows = [
        (t(ctx, "facet_jurisdiction", lang), p["headquarters"]),
        (t(ctx, "facet_alliance", lang),
         f'<span class="badge {eye_cls}">{t(ctx, eye_key, lang)}</span>'),
        (t(ctx, "facet_owner", lang), p["owner"]),
        (t(ctx, "facet_launched", lang), str(p["launchYear"])),
        (t(ctx, "facet_ram", lang), yesno(p["ramOnly"], lang)),
        (t(ctx, "facet_opensource", lang),
         yesno(p["openSourceApps"], lang)),
        (t(ctx, "facet_audit", lang),
         f'{p["audit"]["count"]}× {e(p["audit"]["firm"])} · {e(p["audit"]["latest"])}'
         if p["audit"]["count"] else t(ctx, "audit_none", lang)),
        (t(ctx, "facet_court", lang),
         yesno(p["courtTested"], lang)),
        (t(ctx, "facet_anon_signup", lang),
         yesno(p["anonymousSignup"], lang)),
        (t(ctx, "facet_crypto", lang),
         yesno(p["cryptoPayment"], lang)),
        (t(ctx, "facet_transparency", lang),
         yesno(p["transparencyReport"], lang)),
    ]
    privacy_stats = "".join(
        f'<div class="stats__row"><span class="stats__k">{e(k)}</span>'
        f'<span class="stats__v">{v}</span></div>'
        for k, v in privacy_rows
    )

    court_note = ""
    if p.get("courtTestedNote"):
        court_note = R.callout(
            ctx, lang, "good" if p["courtTested"] else "",
            t(ctx, "facet_court_evidence", lang), p["courtTestedNote"][lang]
        )

    # ---- network facts
    network_rows = [
        (t(ctx, "facet_servers", lang), server_label(p, lang)),
        (t(ctx, "facet_countries", lang), str(p["countries"])),
        (t(ctx, "facet_protocols", lang), ", ".join(p["protocols"])),
        (t(ctx, "facet_devices", lang),
         t(ctx, "unlimited", lang) if p["devices"] == -1 else str(p["devices"])),
        (t(ctx, "facet_guarantee", lang),
         f'{p["moneyBackDays"]} {t(ctx, "guarantee_unit", lang)}'),
        (t(ctx, "facet_free", lang),
         (f'{p.get("freeGbPerMonth", 0)} GB / {t(ctx, "per_month", lang)}'
          if p["freeTier"] else t(ctx, "no", lang))),
        (t(ctx, "facet_trial", lang),
         t(ctx, "yes", lang) if p.get("freeTrial") else t(ctx, "no", lang)),
    ]
    network_stats = "".join(
        f'<div class="stats__row"><span class="stats__k">{e(k)}</span>'
        f'<span class="stats__v">{v}</span></div>'
        for k, v in network_rows
    )

    # ---- price table (row order matches R.plan_models, so the interactive
    # plan picker can highlight the row it has selected)
    price_rows = []
    for plan_i, plan in enumerate(sorted(p["pricing"], key=lambda pl: -pl["termMonths"])):
        monthly = plan["monthlySEK"] if cur == "SEK" else plan["monthlyUSD"]
        totalp = plan["totalSEK"] if cur == "SEK" else plan["totalUSD"]
        o_monthly = plan["monthlyUSD"] if cur == "SEK" else plan["monthlySEK"]
        o_total = plan["totalUSD"] if cur == "SEK" else plan["totalSEK"]
        best = plan is cheapest_plan(p)
        row_cls = ' class="is-active"' if best else ''
        # English pages quote USD alone, so the second-currency column is a
        # Swedish-only extra (SEK is the primary there, USD the conversion).
        alt_td = (f'  <td class="num faint">{e(money_prec(o_monthly, lang, o_cur))}'
                  f' / {e(money(o_total, lang, o_cur))}</td>'
                  if R.show_alt(lang) else "")
        price_rows.append(f"""<tr{row_cls} data-plan-row="{plan_i}">
  <th scope="row">{e(plan['term'][lang])}{' <span class="badge badge--gold">' + t(ctx, "best_value", lang) + '</span>' if best else ''}</th>
  <td class="num">{e(money_prec(monthly, lang, cur))}</td>
  <td class="num">{e(money(totalp, lang, cur))}</td>
  {alt_td}</tr>""")

    alt_th = (f'      <th scope="col">{e(C.S["alt_currency"][lang])}</th>'
              if R.show_alt(lang) else "")
    price_table = f"""<div class="table-wrap">
  <table class="cmp" style="min-width:0">
    <thead><tr>
      <th scope="col">{t(ctx, "term", lang)}</th>
      <th scope="col">{t(ctx, "col_price", lang)}</th>
      <th scope="col">{t(ctx, "col_total", lang)}</th>
      {alt_th}
    </tr></thead>
    <tbody>{"".join(price_rows)}</tbody>
  </table>
</div>"""

    renew = R.callout(
        ctx, lang, "warn",
        t(ctx, "renew_price", lang),
        C.S["renew_explainer"][lang].format(name=p["name"]),
    )

    # ---- alternatives
    others = [q for q in ctx["providers"] if q["id"] != p["id"]]
    alts = sorted(others, key=lambda q: abs(q["rank"] - p["rank"]))[:2]
    alt_cards = ""
    for a in alts:
        alt_cards += f"""<div class="card">
  <div style="display:flex;gap:.9rem;align-items:center">
    {R.monogram(ctx, a, "mono-badge--sm")}
    <h3 style="font-size:1.05rem;margin:0">
      <a href="{ctx["path"]("vpn/" + a["slug"] + ".html", lang)}"
         style="color:inherit;text-decoration:none">{e(a["name"])}</a>
    </h3>
    {score_ring(weighted_score(a, weights), "ring--sm", lang)}
  </div>
  <p class="muted" style="font-size:.88rem;margin-top:.7rem">{e(a["tagline"][lang])}</p>
  <div class="chip-row" style="margin-top:.8rem">
    <span class="chip">{icon("tag")}{e(money_prec(cheapest_plan(a)["monthlySEK"] if cur == "SEK"
        else cheapest_plan(a)["monthlyUSD"], lang, cur))}{t(ctx, "per_month", lang)}</span>
    <span class="chip">{icon("globe")}{server_label(a, lang)}</span>
  </div>
</div>"""

    # ---- provider FAQ
    faq_items = [(q, f"<p>{a}</p>") for q, a in provider_faq(p, lang)]

    title_s = C.S["review_title_fmt"][lang].format(name=p["name"])
    h1 = C.S["review_h1_fmt"][lang].format(name=p["name"])

    trail = [
        (C.S["nav_reviews"][lang], "reviews.html"),
        (p["name"], None),
    ]

    audit_source_html = (
        f'<p class="muted prose" style="margin-top:1.25rem">'
        f'{e(C.S["audit_source"][lang].format(firm=p["audit"]["firm"]))}</p>'
        if p["audit"]["count"] else
        f'<p class="muted prose" style="margin-top:1.25rem">'
        f'{e(C.S["audit_source_none"][lang])}</p>'
    )

    body = f"""<main id="main">
<section class="rev-hero">
  <div class="wrap">
    {R.breadcrumbs(ctx, lang, trail)}
    <div class="rev-head">
      <div>
        <div class="rev-head__id">
          {R.monogram(ctx, p, "mono-badge--lg")}
          <div>
            <div class="chip-row">
              <span class="badge{' badge--gold' if p['rank'] == 1 else ''}">{e(p["badge"][lang])}</span>
              <span class="badge">#{p["rank"]} {t(ctx, "of_ten", lang)}</span>
            </div>
            <h1 style="margin-top:.6rem">{e(h1)}</h1>
          </div>
        </div>
        <p class="rev-head__lede">{e(p["tagline"][lang])}</p>
        {R.pros_cons(ctx, lang, p)}
      </div>

      <aside class="rev-side">
        <div class="rev-side__score">
          {score_ring(total, "ring--lg", lang)}
          <p class="ring-row__label" style="margin-top:.7rem">{t(ctx, "our_score", lang)}</p>
        </div>
        {R.plan_picker(ctx, lang, p)}
        {R.price_block(ctx, lang, p, with_plans=True)}
        <div class="rev-side__price" style="margin-top:1.25rem">
          {R.cta(ctx, lang, p, block=True)}
          <p class="faint" style="text-align:center;margin:0">
            {e(t(ctx, "money_back_fmt", lang).format(days=p["moneyBackDays"]))}
          </p>
        </div>
      </aside>
    </div>
  </div>
</section>

<section class="section section--sm">
  <div class="wrap">
    <div class="card card--pad-lg">
      <p class="verdict__label">{e(r["verdict_label"])}</p>
      <p style="font-size:1.06rem;line-height:1.65">{e(p["verdict"][lang])}</p>
      <p class="faint" style="margin-top:1rem">
        {icon("refresh")} {e(r["update_note"])} {e(R.long_date(ctx["build_date"], lang))}
      </p>
    </div>
  </div>
</section>

<section class="section section--sm">
  <div class="wrap">
    <div class="prose">
      <h2>{e(r["scores_title"])}</h2>
      <p class="lede">{e(r["scores_lede"])}</p>
    </div>
    <div class="card card--pad-lg" style="margin-top:1.5rem">
      {score_bars(ctx, lang, p)}
      <div class="rule"></div>
      <p class="verdict__label">{e(r["basis_label"])}</p>
      <p class="muted">{e(p["scoreBasis"][lang])}</p>
    </div>
    {R.callout(ctx, lang, "", r["bench_title"], f'<span>{e(r["bench_body"])}</span>')}
  </div>
</section>

<section class="section section--sm">
  <div class="wrap">
    <div class="section-head"><h2>{icon("lock")} {e(r["privacy_title"])}</h2></div>
    <div class="stats">{privacy_stats}</div>
    {court_note}
{audit_source_html}
  </div>
</section>

<section class="section section--sm">
  <div class="wrap">
    <div class="section-head"><h2>{e(r["network_title"])}</h2></div>
    <div class="stats">{network_stats}</div>
  </div>
</section>

<section class="section section--sm">
  <div class="wrap">
    <div class="section-head"><h2>{e(r["price_title"])}</h2></div>
    {price_table}
    {renew}
    <p class="faint" style="margin-top:.75rem">
      {icon("info")} {e(C.S["price_caveat"][lang])}
    </p>
  </div>
</section>

<section class="section section--sm">
  <div class="wrap wrap-tight">
    <h2>{e(r["who_title"])}</h2>
    <p class="muted" style="margin-top:1rem;font-size:1.02rem">{e(p["idealFor"][lang])}</p>
    <div class="callout" style="margin-top:1.5rem">
      {icon("tv")}
      <div>
        <strong>{e(C.S["streaming_heading"][lang])}</strong>
        <span>{e(p["streamingScoreNote"][lang])}</span>
      </div>
    </div>
  </div>
</section>

<section class="section section--sm">
  <div class="wrap">
    <div class="section-head">
      <h2>{e(r["alternatives_title"])}</h2>
      <p class="lede">{e(r["alternatives_lede"])}</p>
    </div>
    <div class="card-grid">{alt_cards}</div>
  </div>
</section>

<section class="section section--sm">
  <div class="wrap wrap-tight">
    <h2>{e(r["faq_title"].format(name=p["name"]))}</h2>
    <div style="margin-top:1.5rem">{R.faq_block(faq_items)}</div>
  </div>
</section>

{cta_band(ctx, lang,
    title=r["cta_title"].format(name=p["name"]),
    body=r["cta_body"],
    label=C.S["cta_label"][lang],
    provider=p)}
</main>"""

    ld = [
        R.ld_org(ctx),
        R.ld_breadcrumbs(ctx, lang, trail),
        R.ld_review(ctx, lang, p),
        R.ld_faqpage(provider_faq(p, lang)),
    ]
    return assemble(ctx, lang, rel, f"{title_s} | {SITE['name']}",
                    p["tagline"][lang][:180], body, jsonld=ld,
                    nav_active="reviews.html", sticky=ctx["path"]("vpn/" + p["slug"] + ".html", lang))


# ---------------------------------------------------------------------------
# Money pages — en|sv/best-vpn-for/<slug>/  (published as clean folder URLs)
# ---------------------------------------------------------------------------


def load_topics() -> list[dict]:
    """Curated picks + per-task weights; see assets/data/topics.json."""
    with open(os.path.join(ROOT, "assets", "data", "topics.json"),
              encoding="utf-8") as fh:
        return json.load(fh)["topics"]


def topic_tile(ctx, lang: str, topic: dict) -> str:
    """A `.usecase` link-card pointing at one best-VPN-for guide."""
    g = C.BEST_VPN_FOR[lang][topic["slug"]]
    by_id = {p["id"]: p for p in ctx["providers"]}
    picks = " · ".join(by_id[pid]["name"] for pid in topic["picks"])
    title = f'{C.S["bfv_eyebrow"][lang]} {g["label"]}'
    href = ctx["path"](f'best-vpn-for/{topic["slug"]}/', lang)
    return f"""<a class="usecase" href="{e(href)}">
  <span class="usecase__top">{icon(topic["icon"])}{e(title)}</span>
  <span class="usecase__who">{e(picks)}</span>
  <span class="usecase__go">{e(C.S["bfv_read"][lang])} {icon("arrow-right")}</span>
</a>"""


def spotlight_box(ctx, lang: str, g: dict) -> str:
    """An affiliate box for a product that is NOT a ranked provider.

    Rendered only when the guide copy carries a "spotlight" key. It states
    plainly that the product is unranked, and the link follows the same
    affiliate pattern as every other commercial CTA (Ad label, sponsored
    rel, data-affiliate flag) so the outbound-link check covers it.
    """
    sp = g.get("spotlight")
    if not sp:
        return ""
    url, is_aff = R.affiliate_url(ctx, sp["affiliate_id"])
    settings = ctx["affiliates"]["settings"]
    rel = settings["relAttribute"] if is_aff else "nofollow noopener"
    tag = (R.affiliate_label(ctx, lang) if is_aff
           else t(ctx, "external_link", lang))
    return f"""<section class="section" id="spotlight">
  <div class="wrap wrap-tight">
    <div class="card card--pad-lg">
      <span class="eyebrow">{icon("gamepad")} {e(sp["eyebrow"])}</span>
      <div class="spotlight__head">{R.brand_logo(ctx, sp["affiliate_id"])}<h2>{e(sp["title"])}</h2></div>
      <p class="lede">{e(sp["body"])}</p>
      <p class="muted">{e(sp["note"])}</p>
      <div class="cta-wrap">
        <span class="cta-tag">{e(tag)}</span>
        <a class="btn btn--primary" href="{e(url)}" target="_blank" rel="{e(rel)}"
           data-provider="{e(sp["affiliate_id"])}" data-affiliate="{str(is_aff).lower()}">
          {e(sp["cta"])} {icon("external")}
        </a>
      </div>
    </div>
  </div>
</section>
"""


def criteria_table(ctx, lang: str, criteria: dict, caption: str) -> str:
    """Same five published components, re-weighted for one task."""
    rows = []
    for key, w in sorted(criteria.items(), key=lambda kv: -kv[1]):
        meta = R.SCORE_META[key]
        rows.append(f"""<tr>
  <th scope="row">{e(meta[lang])}</th>
  <td class="num">{int(w)} %</td>
  <td class="muted">{e(SCORE_DEFS[key][lang][1])}</td>
</tr>""")
    return f"""<div class="table-wrap">
  <table class="cmp" style="min-width:0">
    <caption>{e(caption)}</caption>
    <thead><tr>
      <th scope="col">{t(ctx, "col_criterion", lang)}</th>
      <th scope="col">{t(ctx, "col_weight", lang)}</th>
      <th scope="col">{t(ctx, "score_basis", lang)}</th>
    </tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</div>"""


def page_best_vpn_for_hub(ctx, lang):
    rel = "best-vpn-for/index.html"
    enter(ctx, lang, rel)
    hub = C.BEST_VPN_FOR[lang]["hub"]
    topics = load_topics()

    intro = "".join(f"<p>{e(p)}</p>" for p in hub["intro"])
    tiles = "".join(topic_tile(ctx, lang, tp) for tp in topics)
    faq_items = [(q, f"<p>{e(a)}</p>") for q, a in hub["faq"]]
    trail = [(C.S["nav_home"][lang], "index.html"), (hub["h1"], None)]

    body = f"""<main id="main">
<section class="section">
  <div class="wrap">
    <div class="wrap-tight" style="padding-inline:0">
      {R.breadcrumbs(ctx, lang, trail)}
      <span class="eyebrow">{icon("doc")} {e(hub["eyebrow"])}</span>
      <h1>{e(hub["h1"])}</h1>
      <p class="lede">{e(hub["lede"])}</p>
      <div class="prose" style="margin-top:1.75rem">{intro}</div>
    </div>
  </div>
</section>

<section class="section section--alt" id="guides">
  <div class="wrap">
    <header class="section-head">
      <span class="eyebrow">{icon("star")} {e(C.S["bfv_eyebrow"][lang])}</span>
      <h2>{e(C.S["bfv_hub_link"][lang])}</h2>
      <p class="lede">{e(C.S["bfv_related_lede"][lang])}</p>
    </header>
    <div class="card-grid">{tiles}</div>
  </div>
</section>

<section class="section section--sm" id="faq">
  <div class="wrap wrap-tight">
    <header class="section-head"><h2>{e(C.S["bfv_hub_faq_title"][lang])}</h2></header>
    <div style="margin-top:1.5rem">{R.faq_block(faq_items)}</div>
    <p class="section-footer">
      <a href="{ctx["path"]("faq.html", lang)}" class="btn btn--ghost btn--sm">
        {e(C.S["all_faq"][lang])} {icon("arrow-right")}
      </a>
    </p>
  </div>
</section>

{cta_band(ctx, lang,
    title=C.S["cta_home_title"][lang],
    body=C.S["cta_home_body"][lang],
    label=HOME[lang]["compare_cta"],
    href=ctx["path"]("compare.html", lang))}
</main>"""

    ld = [R.ld_org(ctx), R.ld_faqpage(hub["faq"]),
          R.ld_breadcrumbs(ctx, lang, trail)]
    title = f"{hub['h1']} | {SITE['name']}"
    return assemble(ctx, lang, rel, title, hub["desc"], body,
                    jsonld=ld, nav_active="best-vpn-for/")


def page_best_vpn_for(ctx, lang, topic: dict):
    slug = topic["slug"]
    rel = f"best-vpn-for/{slug}/index.html"
    enter(ctx, lang, rel)
    g = C.BEST_VPN_FOR[lang][slug]
    label = g["label"]
    by_id = {p["id"]: p for p in ctx["providers"]}
    # The ranking this site publishes is the ranking every table shows, so the
    # full comparison stays in global rank order and reads 1..N down the page.
    providers = ranked(ctx["providers"], ctx["weights"])
    topics = load_topics()

    intro = "".join(f"<p>{e(p)}</p>" for p in g["intro"])
    why = "".join(f"<p>{e(p)}</p>" for p in g["why"])
    guide = "".join(f"<p>{e(p)}</p>" for p in g["guide"])
    faq_items = [(q, f"<p>{e(a)}</p>") for q, a in g["faq"]]

    picks_html = "".join(
        f'<div>{R.pcard(ctx, lang, by_id[pid])}'
        f'<p class="muted" style="margin:.75rem 0 0">{e(g["picks"][pid])}</p></div>'
        for pid in topic["picks"]
    )
    related = "".join(topic_tile(ctx, lang, tp) for tp in topics
                      if tp["slug"] != slug)

    trail = [
        (C.S["nav_home"][lang], "index.html"),
        (C.S["bfv_hub_link"][lang], "best-vpn-for/"),
        (g["h1"], None),
    ]

    body = f"""<main id="main">
<section class="section">
  <div class="wrap">
    <div class="wrap-tight" style="padding-inline:0">
      {R.breadcrumbs(ctx, lang, trail)}
      <span class="eyebrow">{icon(topic["icon"])} {e(C.S["bfv_eyebrow"][lang])} {e(label)}</span>
      <h1>{e(g["h1"])}</h1>
      <p class="lede">{e(g["lede"])}</p>
      <div class="prose" style="margin-top:1.75rem">{intro}</div>
    </div>
  </div>
</section>

<section class="section section--alt" id="top-3">
  <div class="wrap">
    <header class="section-head">
      <span class="eyebrow">{icon("star")} {e(HOME[lang]["top_eyebrow"])}</span>
      <h2>{e(C.S["bfv_picks_title"][lang].format(topic=label))}</h2>
      <p class="lede">{e(C.S["bfv_picks_note"][lang])}</p>
    </header>
    <div class="stack">{picks_html}</div>
  </div>
</section>

{spotlight_box(ctx, lang, g)}
<section class="section" id="how-we-chose">
  <div class="wrap wrap-tight">
    <div class="prose">
      <h2>{e(C.S["bfv_why_title"][lang])}</h2>
      {why}
      <h2 style="margin-top:2rem">{e(C.S["bfv_criteria_title"][lang])}</h2>
    </div>
    {criteria_table(ctx, lang, topic["criteria"], C.S["bfv_criteria_caption"][lang])}
  </div>
</section>

<section class="section section--alt" id="all-providers">
  <div class="wrap">
    <header class="section-head">
      <h2>{e(C.S["bfv_table_title"][lang])}</h2>
      <p class="lede">{e(C.S["bfv_table_lede"][lang])}</p>
    </header>
    {compare_table(ctx, lang, providers)}
    <p class="section-footer">
      {icon("refresh")} {e(t(ctx, "verified_on", lang).format(
          date=R.long_date(ctx["build_date"], lang)))}
    </p>
  </div>
</section>

<section class="section" id="guide">
  <div class="wrap wrap-tight">
    <div class="prose">
      <h2>{e(g["guide_title"])}</h2>
      {guide}
    </div>
  </div>
</section>

<section class="section section--sm" id="faq">
  <div class="wrap wrap-tight">
    <header class="section-head">
      <h2>{e(C.S["bfv_faq_title"][lang].format(topic=label))}</h2>
    </header>
    <div style="margin-top:1.5rem">{R.faq_block(faq_items)}</div>
    <p class="section-footer">
      <a href="{ctx["path"]("faq.html", lang)}" class="btn btn--ghost btn--sm">
        {e(C.S["all_faq"][lang])} {icon("arrow-right")}
      </a>
    </p>
  </div>
</section>

<section class="section section--sm" id="more-guides">
  <div class="wrap">
    <header class="section-head">
      <h2>{e(C.S["bfv_related_title"][lang])}</h2>
      <p class="lede">{e(C.S["bfv_related_lede"][lang])}</p>
    </header>
    <div class="card-grid">{related}</div>
    <p class="section-footer">
      <a href="{ctx["path"]("best-vpn-for/", lang)}" class="btn btn--ghost btn--sm">
        {e(C.S["bfv_hub_link"][lang])} {icon("arrow-right")}
      </a>
    </p>
  </div>
</section>

{cta_band(ctx, lang,
    title=C.S["bfv_cta_title"][lang].format(topic=label),
    body=C.S["bfv_cta_body"][lang],
    label=HOME[lang]["compare_cta"],
    href=ctx["path"]("compare.html", lang))}
</main>"""

    ld = [
        R.ld_org(ctx),
        R.ld_breadcrumbs(ctx, lang, trail),
        R.ld_faqpage(g["faq"]),
        R.ld_itemlist(ctx, lang, [by_id[pid] for pid in topic["picks"]],
                      g["h1"]),
    ]
    title = f"{g['h1']} ({ctx['build_year']}) | {SITE['name']}"
    return assemble(ctx, lang, rel, title, g["desc"], body,
                    jsonld=ld, nav_active="best-vpn-for/",
                    script="compare.js")


# ---------------------------------------------------------------------------
# Explainers — en|sv/vpn-explained/<slug>/  (informational, non-commercial)
# Copy lives in assets/data/explained.json: one entry per slug holding both
# languages, so the hreflang pair cannot drift the way two independent files
# would.
# ---------------------------------------------------------------------------


def load_explained() -> list[dict]:
    """Editorial explainers; see assets/data/explained.json."""
    with open(os.path.join(ROOT, "assets", "data", "explained.json"),
              encoding="utf-8") as fh:
        return json.load(fh)["topics"]


TOKEN_RE = re.compile(r"\{\{([a-z]+)(?::([a-z0-9-]+))?(?:\|([^}]*))?\}\}")

TOKEN_DEFAULTS = {
    "compare": lambda ctx, lang: (ctx["path"]("compare.html", lang),
                                  C.S["nav_compare"][lang]),
    "method": lambda ctx, lang: (ctx["path"]("how-we-test.html", lang),
                                 C.S["nav_how"][lang]),
    "faq": lambda ctx, lang: (ctx["path"]("faq.html", lang),
                              C.S["nav_faq"][lang]),
    "hub": lambda ctx, lang: (ctx["path"]("vpn-explained/", lang),
                              C.S["explained_hub_link"][lang]),
    "bfv": lambda ctx, lang: (ctx["path"]("best-vpn-for/", lang),
                              C.S["bfv_hub_link"][lang]),
}


def resolve_tokens(text: str, ctx: dict, lang: str, *, html: bool) -> str:
    """Expand the inline link tokens used in explainer copy.

        {{compare}} {{method}} {{faq}} {{hub}} {{bfv}}
        {{review:nordvpn}}  {{review:nordvpn|our NordVPN review}}
        {{guide:streaming}} {{guide:streaming|the streaming guide}}
        {{explain:are-vpns-safe}} {{explain:are-vpns-safe|our safety guide}}

    With html=True the surrounding text is escaped and each token becomes an
    anchor; with html=False the tokens collapse to their labels, which is what
    the FAQPage JSON-LD wants (schema.org answers are plain text). An unknown
    token raises, so a typo fails the build instead of shipping literal braces.
    """
    by_id = {p["id"]: p for p in ctx["providers"]}
    out: list[str] = []
    pos = 0
    for m in TOKEN_RE.finditer(text):
        out.append(e(text[pos:m.start()]) if html else text[pos:m.start()])
        kind, arg, label = m.group(1), m.group(2), m.group(3)
        if kind in TOKEN_DEFAULTS:
            href, default = TOKEN_DEFAULTS[kind](ctx, lang)
        elif kind == "review":
            p = by_id[arg]
            href = ctx["path"](f"vpn/{p['slug']}.html", lang)
            default = p["name"]
        elif kind == "guide":
            g = C.BEST_VPN_FOR[lang][arg]
            href = ctx["path"](f"best-vpn-for/{arg}/", lang)
            default = f'{C.S["bfv_eyebrow"][lang]} {g["label"]}'
        elif kind == "explain":
            by_slug = {x["slug"]: x for x in load_explained()}
            href = ctx["path"](f"vpn-explained/{arg}/", lang)
            default = by_slug[arg][lang]["title"]
        else:
            raise ValueError(f"unknown link token {m.group(0)!r} in explainer copy")
        anchor_label = label or default
        if html:
            out.append(f'<a href="{e(href)}">{e(anchor_label)}</a>')
        else:
            out.append(anchor_label)
        pos = m.end()
    out.append(e(text[pos:]) if html else text[pos:])
    return "".join(out)


def linkify(text: str, ctx: dict, lang: str) -> str:
    return resolve_tokens(text, ctx, lang, html=True)


def explained_tile(ctx, lang: str, topic: dict) -> str:
    """A `.usecase` link-card pointing at one explainer."""
    a = topic[lang]
    href = ctx["path"](f'vpn-explained/{topic["slug"]}/', lang)
    head = a["lede"].split(". ")[0]
    if len(head) > 130:
        head = head[:130].rsplit(" ", 1)[0].rstrip(",;—") + "…"
    return f"""<a class="usecase" href="{e(href)}">
  <span class="usecase__top">{icon(topic["icon"])}{e(a["title"])}</span>
  <span class="usecase__who">{e(head)}</span>
  <span class="usecase__go">{e(C.S["explained_read"][lang])} {icon("arrow-right")}</span>
</a>"""


def review_tile(ctx, lang: str, p: dict) -> str:
    """A `.usecase` link-card pointing at one provider review."""
    href = ctx["path"](f'vpn/{p["slug"]}.html', lang)
    return f"""<a class="usecase" href="{e(href)}">
  <span class="usecase__top">{icon("star")}{e(p["name"])}</span>
  <span class="usecase__who">{e(p["badge"][lang])}</span>
  <span class="usecase__go">{e(C.S["bfv_review_link"][lang])} {icon("arrow-right")}</span>
</a>"""


def page_explained_hub(ctx, lang):
    rel = "vpn-explained/index.html"
    enter(ctx, lang, rel)
    hub = C.EXPLAINED_HUB[lang]
    topics = load_explained()

    intro = "".join(f"<p>{linkify(p, ctx, lang)}</p>" for p in hub["intro"])
    tiles = "".join(explained_tile(ctx, lang, tp) for tp in topics)
    faq_html = [(q, linkify(a, ctx, lang)) for q, a in hub["faq"]]
    faq_items = [(q, f"<p>{a}</p>") for q, a in faq_html]
    trail = [(C.S["nav_home"][lang], "index.html"), (hub["h1"], None)]

    body = f"""<main id="main">
<section class="section">
  <div class="wrap">
    <div class="wrap-tight" style="padding-inline:0">
      {R.breadcrumbs(ctx, lang, trail)}
      <span class="eyebrow">{icon("info")} {e(C.S["explained_eyebrow"][lang])}</span>
      <h1>{e(hub["h1"])}</h1>
      <p class="lede">{e(hub["lede"])}</p>
      <div class="prose" style="margin-top:1.75rem">{intro}</div>
    </div>
  </div>
</section>

<section class="section section--alt" id="explainers">
  <div class="wrap">
    <header class="section-head">
      <span class="eyebrow">{icon("doc")} {e(C.S["explained_hub_link"][lang])}</span>
      <h2>{e(C.S["explained_hub_title"][lang])}</h2>
      <p class="lede">{e(C.S["explained_hub_lede"][lang])}</p>
    </header>
    <div class="card-grid">{tiles}</div>
  </div>
</section>

<section class="section section--sm" id="faq">
  <div class="wrap wrap-tight">
    <header class="section-head"><h2>{e(C.S["explained_faq_title"][lang])}</h2></header>
    <div style="margin-top:1.5rem">{R.faq_block(faq_items)}</div>
    <p class="section-footer">
      <a href="{ctx["path"]("faq.html", lang)}" class="btn btn--ghost btn--sm">
        {e(C.S["all_faq"][lang])} {icon("arrow-right")}
      </a>
    </p>
  </div>
</section>

{cta_band(ctx, lang,
    title=C.S["cta_home_title"][lang],
    body=C.S["cta_home_body"][lang],
    label=HOME[lang]["compare_cta"],
    href=ctx["path"]("compare.html", lang))}
</main>"""

    ld = [
        R.ld_org(ctx),
        R.ld_faqpage([(q, resolve_tokens(a, ctx, lang, html=False))
                      for q, a in hub["faq"]]),
        R.ld_breadcrumbs(ctx, lang, trail),
    ]
    title = f"{hub['h1']} | {SITE['name']}"
    return assemble(ctx, lang, rel, title, hub["desc"], body,
                    jsonld=ld, nav_active="vpn-explained/")


def page_explained(ctx, lang, topic: dict):
    slug = topic["slug"]
    rel = f"vpn-explained/{slug}/index.html"
    enter(ctx, lang, rel)
    a = topic[lang]
    by_id = {p["id"]: p for p in ctx["providers"]}

    chunks = []
    for sec in a["sections"]:
        chunks.append(f"<h2>{e(sec['h2'])}</h2>")
        for para in sec["p"]:
            chunks.append(f"<p>{linkify(para, ctx, lang)}</p>")
        if sec.get("list"):
            items = "".join(f"<li>{linkify(x, ctx, lang)}</li>"
                            for x in sec["list"])
            chunks.append(f"<ul>{items}</ul>")
    prose = "".join(chunks)

    faq_items = [(q, f"<p>{linkify(ans, ctx, lang)}</p>")
                 for q, ans in a["faq"]]

    related = "".join(review_tile(ctx, lang, by_id[pid])
                      for pid in topic.get("reviews", []))
    related += "".join(
        topic_tile(ctx, lang, tp) for tp in load_topics()
        if tp["slug"] in topic.get("guides", [])
    )

    trail = [
        (C.S["nav_home"][lang], "index.html"),
        (C.S["explained_hub_link"][lang], "vpn-explained/"),
        (a["title"], None),
    ]

    body = f"""<main id="main">
<section class="section">
  <div class="wrap">
    <div class="wrap-tight" style="padding-inline:0">
      {R.breadcrumbs(ctx, lang, trail)}
      <span class="eyebrow">{icon(topic["icon"])} {e(C.S["explained_eyebrow"][lang])}</span>
      <h1>{e(a["title"])}</h1>
      <p class="lede">{e(a["lede"])}</p>
      <div class="prose" style="margin-top:1.75rem">{prose}</div>
    </div>
  </div>
</section>

<section class="section section--sm" id="faq">
  <div class="wrap wrap-tight">
    <header class="section-head">
      <h2>{e(C.S["explained_faq_title"][lang])}</h2>
    </header>
    <div style="margin-top:1.5rem">{R.faq_block(faq_items)}</div>
    <p class="section-footer">
      <a href="{ctx["path"]("faq.html", lang)}" class="btn btn--ghost btn--sm">
        {e(C.S["all_faq"][lang])} {icon("arrow-right")}
      </a>
    </p>
  </div>
</section>

<section class="section section--alt" id="related">
  <div class="wrap">
    <header class="section-head">
      <span class="eyebrow">{icon("link")} {e(C.S["explained_related_title"][lang])}</span>
      <h2>{e(C.S["explained_related_title"][lang])}</h2>
      <p class="lede">{e(C.S["explained_related_lede"][lang])}</p>
    </header>
    <div class="card-grid">{related}</div>
    <p class="section-footer">
      <a href="{ctx["path"]("vpn-explained/", lang)}" class="btn btn--ghost btn--sm">
        {e(C.S["explained_hub_link"][lang])} {icon("arrow-right")}
      </a>
    </p>
  </div>
</section>

{cta_band(ctx, lang,
    title=C.S["cta_home_title"][lang],
    body=C.S["cta_home_body"][lang],
    label=HOME[lang]["compare_cta"],
    href=ctx["path"]("compare.html", lang))}
</main>"""

    ld = [
        R.ld_org(ctx),
        R.ld_article(ctx, lang, title=a["title"], description=a["desc"],
                     rel=f"vpn-explained/{slug}/",
                     published=topic.get("published", ctx["build_date"]),
                     modified=topic.get("modified", ctx["build_date"])),
        R.ld_faqpage([(q, resolve_tokens(ans, ctx, lang, html=False))
                      for q, ans in a["faq"]]),
        R.ld_breadcrumbs(ctx, lang, trail),
    ]
    title = f"{a['title']} | {SITE['name']}"
    return assemble(ctx, lang, rel, title, a["desc"], body,
                    jsonld=ld, nav_active="vpn-explained/")


def page_how_we_test(ctx, lang):
    rel = "how-we-test.html"
    enter(ctx, lang, rel)
    hw = HOW_WE_TEST[lang]

    why = "".join(f"<p>{p}</p>" for p in hw["why_body"])

    indep = "".join(
        f'<div class="card"><div class="ring-row"><span style="flex:none">{icon("check" if kind == "good" else "x-circle")}</span>'
        f'<h3 style="font-size:1rem">{e(title)}</h3></div>'
        f'<p class="muted" style="font-size:.92rem;margin-top:.6rem">{e(body)}</p></div>'
        for kind, title, body in hw["indep_body"]
    )

    limits = "".join(f"<li>{e(x)}</li>" for x in hw["limits"])

    body = f"""<main id="main">
<section class="section">
  <div class="wrap">
    <div class="wrap-tight" style="padding-inline:0">
      <span class="eyebrow">{icon("scale")} {e(hw["eyebrow"])}</span>
      <h1>{e(hw["h1"])}</h1>
      <p class="lede">{e(hw["lede"])}</p>

      <div class="prose" style="margin-top:2rem">
        <h2>{e(hw["why_title"])}</h2>
        {why}
      </div>
    </div>
  </div>
</section>

<section class="section section--sm">
  <div class="wrap">
    <div class="section-head">
      <h2>{e(hw["weights_title"])}</h2>
      <p class="lede">{e(hw["weights_lede"])}</p>
    </div>
    {weights_table(ctx, lang)}
  </div>
</section>

<section class="section section--sm">
  <div class="wrap">
    <div class="section-head"><h2>{e(hw["defs_title"])}</h2></div>
    <div class="stack">
      {"".join(
        f'<div class="card"><h3>{e(SCORE_DEFS[k][lang][0])}'
        f'<span class="badge badge--accent" style="margin-left:.6rem">{int(ctx["weights"][k] * 100)}%</span></h3>'
        f'<p class="muted" style="font-size:.93rem;margin-top:.6rem">{e(SCORE_DEFS[k][lang][1])}</p></div>'
        for k in sorted(ctx["weights"], key=lambda k: -ctx["weights"][k])
      )}
    </div>
  </div>
</section>

<section class="section section--sm">
  <div class="wrap">
    <div class="section-head"><h2>{e(hw["indep_title"])}</h2></div>
    <div class="card-grid">{indep}</div>
  </div>
</section>

<section class="section section--sm">
  <div class="wrap wrap-tight">
    <div class="prose">
      <h2>{e(hw["limits_title"])}</h2>
      <ul>{limits}</ul>
      <h2>{e(hw["remove_title"])}</h2>
      <p>{e(hw["remove_body"])}</p>
      <h2>{e(hw["correct_title"])}</h2>
      <p>{e(hw["correct_body"])}</p>
    </div>
  </div>
</section>
</main>"""

    title = f"{hw['h1']} | {SITE['name']}"
    return assemble(ctx, lang, rel, title, hw["lede"][:180], body,
                    jsonld=[R.ld_org(ctx)], nav_active="how-we-test.html")


def page_faq(ctx, lang):
    rel = "faq.html"
    enter(ctx, lang, rel)
    items = [(q, f"<p>{a}</p>") for q, a in FAQ_GENERAL[lang]]

    body = f"""<main id="main">
<section class="section">
  <div class="wrap wrap-tight">
    <span class="eyebrow">{icon("info")} {e(C.S["faq_eyebrow"][lang])}</span>
    <h1>{e(C.S["faq_title"][lang])}</h1>
    <p class="lede">{e(C.S["faq_lede"][lang])}</p>
    <div style="margin-top:2rem">{R.faq_block(items)}</div>
  </div>
</section>
</main>"""
    return assemble(ctx, lang, rel, f"{C.S['faq_title'][lang]} | {SITE['name']}",
                    C.S["faq_lede"][lang][:180], body,
                    jsonld=[R.ld_org(ctx), R.ld_faqpage(FAQ_GENERAL[lang])],
                    nav_active="faq.html")


def page_about(ctx, lang):
    rel = "about.html"
    enter(ctx, lang, rel)
    a = ABOUT[lang]
    s = SITE

    what = "".join(f"<p>{p}</p>" for p in a["what_body"])
    ed = "".join(
        f'<div class="card"><div class="ring-row"><span style="flex:none">{icon("check-circle")}</span>'
        f'<h3 style="font-size:1rem">{e(title)}</h3></div>'
        f'<p class="muted" style="font-size:.92rem;margin-top:.6rem">{e(body)}</p></div>'
        for _, title, body in a["ed_body"]
    )
    disc = "".join(f"<p>{p}</p>" for p in a["disc_body"])

    body = f"""<main id="main">
<section class="section">
  <div class="wrap wrap-tight">
    <span class="eyebrow">{icon("users")} {e(a["eyebrow"])}</span>
    <h1>{e(a["h1"])}</h1>
    <p class="lede">{e(a["lede"])}</p>
  </div>
</section>

<section class="section section--sm">
  <div class="wrap">
    <div class="prose">
      <h2>{e(a["what_title"])}</h2>
      {what}
    </div>
  </div>
</section>

<section class="section section--sm">
  <div class="wrap">
    <div class="section-head"><h2>{e(a["ed_title"])}</h2></div>
    <div class="card-grid">{ed}</div>
  </div>
</section>

<section class="section section--sm" id="disclosure">
  <div class="wrap wrap-tight">
    <div class="prose">
      <h2>{e(a["disc_title"])}</h2>
      {disc}
    </div>
  </div>
</section>

<section class="section section--sm">
  <div class="wrap wrap-tight">
    <div class="prose">
      <h2>{e(a["contact_title"])}</h2>
      <p>{e(a["contact_body"])}</p>
    </div>
    <div class="logo-plate" style="margin-top:1.5rem">
      <img src="{ctx["asset"]("img/vpn-pick-lockup-lg.png")}" width="320" height="311"
           alt="{e(SITE["name"])}" decoding="async">
    </div>
    <div class="identity" style="margin-top:1.5rem">
      <dt>{e(C.S["identity_heading"][lang])}</dt>
      <dd>{e(s["legal_name"])}</dd>
      <dd>
        {e(C.S["identity_label_email"][lang])}:
        <a href="mailto:{e(s["email"])}">{e(s["email"])}</a> ·
        {e(C.S["identity_label_address"][lang])}: {e(s["address"])}
      </dd>
    </div>
  </div>
</section>
</main>"""

    title = f"{a['h1']} | {SITE['name']}"
    return assemble(ctx, lang, rel, title, a["lede"][:180], body,
                    jsonld=[R.ld_org(ctx)], nav_active="about.html")


def page_legal(ctx, lang, which: str):
    rel = f"legal/{which}.html"
    enter(ctx, lang, rel)
    d = LEGAL[which][lang]

    sections = ""
    for heading, paras in d["sections"]:
        sections += (
            f'<div class="prose" style="margin-top:2.5rem">'
            f"<h2>{e(heading)}</h2>{''.join(paras)}</div>"
        )

    nav_map = {"privacy": "footer_privacy", "cookies": "footer_cookies",
               "terms": "footer_terms"}
    title = f"{d['h1']} | {SITE['name']}"

    body = f"""<main id="main">
<section class="section">
  <div class="wrap wrap-tight">
    <span class="eyebrow">{icon("doc")} {e(d["eyebrow"])}</span>
    <h1>{e(d["h1"])}</h1>
    <p class="lede">{e(d["lede"])}</p>
    <p class="faint" style="margin-top:1rem">
      {e(d["updated"])}: {e(R.long_date(ctx["build_date"], lang))}
    </p>
    {sections}
  </div>
</section>
</main>"""
    return assemble(ctx, lang, rel, title, d["lede"][:180], body,
                    jsonld=[R.ld_org(ctx)], nav_active="")


# ---------------------------------------------------------------------------
# Per-provider FAQ (3 questions each, generated from verified data)
# ---------------------------------------------------------------------------


def provider_faq(p, lang):
    cur = R.CURRENCY[lang]
    plan = cheapest_plan(p)
    monthly = plan["monthlySEK"] if cur == "SEK" else plan["monthlyUSD"]
    totalp = plan["totalSEK"] if cur == "SEK" else plan["totalUSD"]
    term = plan["term"][lang]

    _audit_kw = dict(
        ram=C.S["yes"][lang] if p["ramOnly"] else C.S["no"][lang],
        alliance=(
            C.S["eye_none"][lang]
            if p["eyesAlliance"] in ("none", "none-eu")
            else C.S["eye_in_alliance"][lang]
        ),
        court=C.S["pf_court_yes"][lang] if p["courtTested"]
        else C.S["pf_court_no"][lang],
    )
    if p["audit"]["count"]:
        audit_answer = C.S["pf_a_audit"][lang].format(
            firm=p["audit"]["firm"],
            count=p["audit"]["count"],
            latest=p["audit"]["latest"],
            **_audit_kw,
        )
    else:
        audit_answer = C.S["pf_a_audit_none"][lang].format(
            name=p["name"],
            **_audit_kw,
        )

    qa = [
        (
            C.S["pf_q_price"][lang].format(name=p["name"]),
            C.S["pf_a_price"][lang].format(
                monthly=money_prec(monthly, lang, cur),
                total=money(totalp, lang, cur),
                term=term,
                days=p["moneyBackDays"],
            ),
        ),
        (
            C.S["pf_q_audit"][lang].format(name=p["name"]),
            audit_answer,
        ),
        (
            C.S["pf_q_score"][lang].format(name=p["name"]),
            C.S["pf_a_score"][lang].format(
                name=p["name"],
                score=f"{weighted_score(p, WEIGHTS_REF):.1f}",
                rank=p["rank"],
                badge=p["badge"][lang],
            ),
        ),
    ]
    return qa


# Score quoted in the generated per-provider FAQ. Always read from the data
# file so the number can never drift away from the published scoring model.
WEIGHTS_REF = load_json("providers.json")["_meta"]["scoringModel"]["weights"]


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------


def assemble(ctx, lang, rel, title, description, body, *, jsonld=None,
             nav_active="", script=None, sticky=None, aff_bar=True) -> str:
    depth = rel.count("/")

    extra_script = ""
    if script:
        extra_script = f'\n  <script src="{ctx["asset"]("js/" + script)}?v={R.asset_key("js/" + script)}" defer></script>'

    sticky_html = sticky_bar_for(ctx, lang, sticky) if sticky else ""

    page = R.head(ctx, lang, title=title, description=description,
                  path=rel, jsonld=jsonld)
    page += "\n<body>\n"
    page += f'<a class="skip-link" href="#main">{e(C.S["skip_to_content"][lang])}</a>\n'
    page += f'<svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" style="display:none">{ctx["sprite"]}</svg>\n'
    if aff_bar:
        page += R.aff_bar(ctx, lang) + "\n"
    page += R.header(ctx, lang, rel, nav_active) + "\n"
    page += body + "\n"
    page += sticky_html
    page += R.footer(ctx, lang) + "\n"
    page += R.consent(ctx, lang) + "\n"
    page += "</body>\n</html>\n"

    # Inject the extra deferred script right after app.js in <head>.
    if extra_script:
        marker = f'<script src="{ctx["asset"]("js/app.js")}?v={R.asset_key("js/app.js")}" defer></script>'
        page = page.replace(marker, marker + extra_script)

    return page


def sticky_bar_for(ctx, lang, slug_path):
    """Mobile bar pointing at this provider's own review page."""
    pid = slug_path.rsplit("/", 1)[-1].replace(".html", "")
    p = next((x for x in ctx["providers"] if x["slug"] == pid), None)
    return R.sticky_bar(ctx, lang, p) if p else ""


# ---------------------------------------------------------------------------
# Sitemap, robots, root redirect
# ---------------------------------------------------------------------------


def build_sitemap(pages: list) -> str:
    """pages: [(url_rel_path, locale_rel_path, lang, changefreq, priority)]"""
    origin = SITE["origin"].rstrip("/")
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for path_rel, rel, lang, freq, prio in pages:
        loc = f"{origin}/{path_rel}"
        other = "sv" if lang == "en" else "en"
        out.append("  <url>")
        out.append(f"    <loc>{e(loc)}</loc>")
        out.append(f'    <xhtml:link rel="alternate" hreflang="{lang}" href="{e(loc)}"/>')
        out.append(
            f'    <xhtml:link rel="alternate" hreflang="{other}" '
            f'href="{e(origin)}/{other}/{rel}"/>'
        )
        out.append(
            f'    <xhtml:link rel="alternate" hreflang="x-default" '
            f'href="{e(origin)}/en/{rel}"/>'
        )
        out.append(f"    <changefreq>{freq}</changefreq>")
        out.append(f"    <priority>{prio}</priority>")
        out.append("  </url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def build_root_index() -> str:
    """Root '/' entry point: detects browser language, offers both."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
""" + R.gtag_head(SITE) + """
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>VPN-Pick.com — VPN comparisons in English &amp; Swedish</title>
<meta name="description" content="Independent VPN comparisons. Choose your language: English or Svenska.">
<meta name="robots" content="noindex, follow">
<meta name="color-scheme" content="dark light">
<meta name="theme-color" content="#080b14" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#f7f9fc" media="(prefers-color-scheme: light)">
<link rel="canonical" href="https://vpn-pick.com/">
<link rel="alternate" hreflang="en" href="https://vpn-pick.com/en/">
<link rel="alternate" hreflang="sv" href="https://vpn-pick.com/sv/">
<link rel="alternate" hreflang="x-default" href="https://vpn-pick.com/en/">
""" + f'<link rel="icon" href="assets/img/vpn-pick-icon.png?v={R.favicon_key()}" type="image/png">' + f'<link rel="stylesheet" href="assets/css/site.css?v={R.asset_key("css/site.css")}">' + f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={SITE["adsense_client"]}" crossorigin="anonymous"></script>' + """
<link rel="apple-touch-icon" href="assets/img/vpn-pick-touch.png">
<script>/* theme before first paint, so a light-mode visitor never sees a dark flash */
(function () {
  var t = null;
  try { t = localStorage.getItem('vpnpick:theme'); } catch (e) {}
  if (t !== 'light' && t !== 'dark') {
    t = (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches)
      ? 'light' : 'dark';
  }
  document.documentElement.setAttribute('data-theme', t);
})();</script>
<script>
/* Pick a language from the browser, then leave. Falls back to English. */
(function () {
  var nav = (navigator.languages || [navigator.language || 'en'])
            .join(',').toLowerCase();
  var target = nav.indexOf('sv') === 0 || nav.indexOf(',sv') > -1 ? 'sv/' : 'en/';
  location.replace(target);
})();
</script>
<style>
  .picks { display: grid; gap: 16px; margin-top: 32px;
           grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); max-width: 560px; }
</style>
</head>
<body>
  <main id="main" class="wrap" style="padding-block:15vh 10vh;max-width:640px">
    <div class="logo-plate" style="margin-bottom:28px">
      <img src="assets/img/vpn-pick-lockup.png" width="110" height="152" alt="VPN-Pick.com">
    </div>
    <h1 style="font-size:clamp(1.9rem,6vw,2.8rem)">Choose your language</h1>
    <p class="lede" style="margin-top:1rem">Välj språk. We redirect you automatically.</p>
    <div class="picks">
      <a class="btn btn--primary btn--lg" href="en/">English</a>
      <a class="btn btn--ghost btn--lg" href="sv/" lang="sv">Svenska</a>
    </div>
    <p class="faint" style="margin-top:2.5rem">
      <a href="en/">Continue in English</a> · <a href="sv/" lang="sv">Fortsätt på svenska</a>
    </p>
  </main>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

LOCALES = ("en", "sv")


def main() -> int:
    ctx = make_context()

    # Only offer use-case options that at least one provider actually targets.
    used = set()
    for p in ctx["providers"]:
        used.update(p["bestFor"])
    ctx["use_case_order"] = [
        u for u in load_json("providers.json")["useCases"] if u["id"] in used
    ]

    written = []
    sitemap_rows = []
    topics = load_topics()
    explained = load_explained()

    def emit(lang: str, rel: str, html: str, freq="weekly", prio="0.7"):
        out = os.path.join(ROOT, lang, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(html)
        written.append(os.path.join(lang, rel))
        # Folder pages are published as their directory URL; a top-level
        # index.html keeps its file URL so the sitemap stays as it was.
        url_rel = rel[:-len("index.html")] if rel.endswith("/index.html") else rel
        sitemap_rows.append((f"{lang}/{url_rel}", url_rel, lang, freq, prio))

    for lang in LOCALES:
        emit(lang, "index.html", page_home(ctx, lang), "daily", "1.0")
        emit(lang, "compare.html", page_compare(ctx, lang), "weekly", "0.9")
        emit(lang, "reviews.html", page_reviews_index(ctx, lang), "weekly", "0.8")
        for p in ctx["providers"]:
            emit(lang, f"vpn/{p['slug']}.html", page_review(ctx, lang, p),
                 "weekly", "0.8")
        emit(lang, "how-we-test.html", page_how_we_test(ctx, lang), "monthly", "0.7")
        emit(lang, "faq.html", page_faq(ctx, lang), "monthly", "0.6")
        emit(lang, "about.html", page_about(ctx, lang), "monthly", "0.5")
        # money pages: /best-vpn-for/ + one clean folder URL per task
        emit(lang, "best-vpn-for/index.html",
             page_best_vpn_for_hub(ctx, lang), "monthly", "0.7")
        for topic in topics:
            emit(lang, f"best-vpn-for/{topic['slug']}/index.html",
                 page_best_vpn_for(ctx, lang, topic), "weekly", "0.7")
        # explainers: /vpn-explained/ + one clean folder URL per question
        emit(lang, "vpn-explained/index.html",
             page_explained_hub(ctx, lang), "monthly", "0.7")
        for topic in explained:
            emit(lang, f"vpn-explained/{topic['slug']}/index.html",
                 page_explained(ctx, lang, topic), "monthly", "0.6")
        for which in ("privacy", "cookies", "terms"):
            emit(lang, f"legal/{which}.html", page_legal(ctx, lang, which),
                 "yearly", "0.3")

    # root entry point
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(build_root_index())

    # sitemap
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(build_sitemap(sitemap_rows))

    # robots
    origin = SITE["origin"].rstrip("/")
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(
            "User-agent: *\n"
            "Allow: /\n"
            "Disallow: /*?\n"
            "\n"
            f"Sitemap: {origin}/sitemap.xml\n"
        )

    # ads.txt — AdSense authorization. Without it Google will not serve ads,
    # and site verification stalls. The pub ID is derived from the AdSense
    # client ID so the two can never disagree.
    pub_id = SITE["adsense_client"].replace("ca-", "")
    with open(os.path.join(ROOT, "ads.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"google.com, {pub_id}, DIRECT, f08c47fec0942fa0\n")

    # hosting headers (Netlify / Cloudflare Pages)
    with open(os.path.join(ROOT, "_headers"), "w", encoding="utf-8") as fh:
        fh.write(
            "/assets/*\n"
            "  Cache-Control: public, max-age=31536000, immutable\n"
            "\n"
            "/*.html\n"
            "  Cache-Control: public, max-age=0, must-revalidate\n"
            "  X-Content-Type-Options: nosniff\n"
            "  Referrer-Policy: strict-origin-when-cross-origin\n"
            "  X-Frame-Options: SAMEORIGIN\n"
            "  Permissions-Policy: geolocation=(), microphone=(), camera=(), interest-cohort=()\n"
            "\n"
            "/*\n"
            "  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload\n"
            "  Content-Security-Policy: default-src 'self'; img-src 'self' data:"
            " https://pagead2.googlesyndication.com https://googleads.g.doubleclick.net"
            " https://tpc.googlesyndication.com https://www.google-analytics.com; "
            "style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'"
            " https://pagead2.googlesyndication.com https://www.googletagmanager.com"
            " https://www.google-analytics.com; "
            "frame-src https://googleads.g.doubleclick.net https://tpc.googlesyndication.com; "
            "connect-src 'self' https://pagead2.googlesyndication.com"
            " https://googleads.g.doubleclick.net https://www.googletagmanager.com"
            " https://www.google-analytics.com https://*.google-analytics.com; "
            "frame-ancestors 'self'; base-uri 'self'; form-action 'self'\n"
        )

    # clean redirects
    with open(os.path.join(ROOT, "_redirects"), "w", encoding="utf-8") as fh:
        fh.write(
            "/index.html  /  301\n"
            "/en           /en/           301\n"
            "/sv           /sv/           301\n"
        )

    print(f"Built {len(written)} pages + root index, sitemap, robots, _headers, _redirects")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())