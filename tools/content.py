"""
content.py — every piece of prose on the site, in English and Swedish.

Rule for this file: nothing is a marketing claim. Every factual statement about
a provider lives in assets/data/providers.json instead, so it can be verified
and dated in one place. This file holds only editorial and explanatory text.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# UI strings
# ---------------------------------------------------------------------------

S = {
    "language":            {"en": "Language", "sv": "Språk"},
    "menu":                {"en": "Menu", "sv": "Meny"},
    "toggle_theme":        {"en": "Switch to light theme", "sv": "Byt till ljust tema"},
    "primary_nav":         {"en": "Primary navigation", "sv": "Huvudnavigering"},
    "breadcrumb":          {"en": "Breadcrumb", "sv": "Brödsmulor"},
    "external_link":       {"en": "External", "sv": "Extern"},
    "best_label":          {"en": "Best overall", "sv": "Bäst totalt"},

    # nav
    "nav_compare":         {"en": "Compare", "sv": "Jämför"},
    "nav_reviews":         {"en": "Reviews", "sv": "Recensioner"},
    "nav_how":             {"en": "How we test", "sv": "Så testar vi"},
    "nav_faq":             {"en": "FAQ", "sv": "Frågor"},
    "nav_about":           {"en": "About", "sv": "Om oss"},
    "all_reviews":         {"en": "All reviews", "sv": "Alla recensioner"},

    # provider card
    "per_month":           {"en": "/month", "sv": "/mån"},
    "for_term":            {"en": "for {term}", "sv": "för {term}"},
    "money_back_fmt":      {"en": "{days}-day money-back guarantee", "sv": "{days} dagars ångerrätt"},
    "ram_only":            {"en": "RAM-only", "sv": "RAM-servrar"},
    "open_source":         {"en": "Open source", "sv": "Källkodsöppna"},
    "unlimited_devices":   {"en": "Unlimited devices", "sv": "Obegränsade enheter"},
    "has_free_tier":       {"en": "Free tier", "sv": "Gratisnivå"},
    "anon_signup":         {"en": "No email needed", "sv": "Ingen e-post"},
    "court_tested":        {"en": "Court tested", "sv": "Domstolsprovat"},
    "pros":                {"en": "What we like", "sv": "Det vi gillar"},
    "cons":                {"en": "What we don't", "sv": "Det vi inte gillar"},
    "pick_for":            {"en": "Our pick:", "sv": "Vår val:"},
    "review_headline_fmt": {"en": "{name} review", "sv": "{name} recension"},

    # comparison table
    "col_provider":        {"en": "VPN", "sv": "VPN"},
    "col_score":           {"en": "Our score", "sv": "Vårt betyg"},
    "col_price":           {"en": "From /month", "sv": "Från /mån"},
    "col_total":           {"en": "Total price", "sv": "Totalpris"},
    "col_servers":         {"en": "Servers", "sv": "Servrar"},
    "col_countries":       {"en": "Countries", "sv": "Länder"},
    "col_devices":         {"en": "Devices", "sv": "Enheter"},
    "col_jurisdiction":    {"en": "Jurisdiction", "sv": "Jurisdiktion"},
    "col_audit":           {"en": "Audits", "sv": "Revisioner"},
    "col_free":            {"en": "Free tier", "sv": "Gratisnivå"},
    "col_guarantee":       {"en": "Guarantee", "sv": "Ångerrätt"},

    "filter_search":       {"en": "Search providers", "sv": "Sök leverantörer"},
    "filter_usecase":      {"en": "Filter by need", "sv": "Filtrera efter behov"},
    "filter_feature":      {"en": "Must have", "sv": "Måste ha"},
    "filter_any":          {"en": "Any", "sv": "Alla"},
    "feature_free":        {"en": "Free tier available", "sv": "Gratisnivå finns"},
    "feature_unlimited":   {"en": "Unlimited devices", "sv": "Obegränsade enheter"},
    "feature_open_source": {"en": "Open-source apps", "sv": "Källkodsöppna appar"},
    "feature_anonymous":   {"en": "No email required", "sv": "Ingen e-post krävs"},
    "reset_filters":       {"en": "Reset filters", "sv": "Återställ filter"},
    "sort_label":          {"en": "Sort by", "sv": "Sortera efter"},

    # table cell values
    "yes":                 {"en": "Yes", "sv": "Ja"},
    "no":                  {"en": "No", "sv": "Nej"},
    "limited":             {"en": "Yes", "sv": "Ja"},
    "unlimited":           {"en": "Unlimited", "sv": "Obegränsat"},
    "not_public":          {"en": "Not published", "sv": "Inte publicerat"},
    "eye_alliance":        {"en": "In the alliance", "sv": "I alliansen"},
    "eye_none":            {"en": "Outside", "sv": "Utanför"},
    "eye_5":               {"en": "5 Eyes", "sv": "5 Eyes"},
    "eye_9":               {"en": "9 Eyes", "sv": "9 Eyes"},
    "eye_14":              {"en": "14 Eyes", "sv": "14 Eyes"},
    "audit_none":          {"en": "None found", "sv": "Ingen hittad"},

    # footer
    "footer_about":        {"en": "About", "sv": "Om"},
    "footer_about_link":   {"en": "How we work", "sv": "Så arbetar vi"},
    "footer_blurb": {
        "en": "Independent VPN reviews in English and Swedish. We publish the "
              "exact method behind every score so you can disagree with us — and you should.",
        "sv": "Oberoende VPN-recensioner på engelska och svenska. Vi publicerar den "
              "exakta metoden bakom varje betyg så att du kan disagreea med oss — och det borde du.",
    },
    "footer_reviews":      {"en": "Providers", "sv": "Leverantörer"},
    "footer_guides":       {"en": "Guides", "sv": "Guider"},
    "footer_legal":        {"en": "Legal", "sv": "Juridik"},
    "footer_disclosure":   {"en": "Affiliate disclosure", "sv": "Annonsinformation"},
    "footer_privacy":      {"en": "Privacy policy", "sv": "Integritetspolicy"},
    "footer_cookies":      {"en": "Cookie policy", "sv": "Kookiepolicy"},
    "footer_terms":        {"en": "Terms of use", "sv": "Användarvillkor"},
    "footer_rights":       {"en": "All rights reserved.", "sv": "Alla rättigheter förbehållna."},
    "footer_noindependence": {
        "en": "We are not affiliated with the VPN providers we review. We are not independent of them — we are paid by some of them.",
        "sv": "Vi är inte knutna till de VPN-leverantörer vi recenserar. Vi är alltså inte oberoende av dem — vi betalas av vissa av dem.",
    },
    "identity_heading":    {"en": "Advertiser identification", "sv": "Annonsörsidentifikation"},
    "identity_body": {
        "en": "Swedish marketing law requires that you can always identify who is behind "
              "the advertising, and reach them if something is wrong. This site is a "
              "commercial comparison service. Details below.",
        "sv": "Svensk marknadsföringslag kräver att du alltid kan identifiera vem som står "
              "bakom reklamen och kunna nå dem om något är fel. Den här webbplatsen är en "
              "kommersiell jämförelsetjänst. Uppgifterna nedan.",
    },
    "identity_label_email": {"en": "Email", "sv": "E-post"},
    "identity_label_address": {"en": "Address", "sv": "Adress"},

    # consent
    "consent_title":      {"en": "Cookies on this site", "sv": "Kakor på den här webbplatsen"},
    "consent_body": {
        "en": "We use one essential cookie to remember that you made a choice. Analytics "
              "cookies are only set if you explicitly accept them. Analytics (Google Analytics) "
              "is only enabled on accept — until then it is consent-denied and sets no cookies. "
              "Pages also load Google AdSense, which may set its own advertising cookies — see "
              "the cookie policy. We do not sell data, and we do not fingerprint your device.",
        "sv": "Vi använder en nödvändig kaka för att komma ihåg att du gjort ett val. "
              "Analyskakor sätts bara om du uttryckligen godkänner dem. Analys (Google Analytics) "
              "aktiveras bara vid godkännande — fram till dess är den samtyckesnekad och sätter "
              "inga kakor. Sidorna laddar även Google AdSense, som kan sätta egna annonskakor — "
              "se kookiepolicyn. Vi säljer ingen data och gör ingen enhetsfingeravtryckning.",
    },
    "consent_accept":      {"en": "Accept analytics", "sv": "Godkänn analys"},
    "consent_necessary":   {"en": "Necessary only", "sv": "Endast nödvändiga"},
    "consent_saved":       {"en": "Preferences saved.", "sv": "Inställningar sparade."},

    # compare page extras
    "sort_label":           {"en": "Sort by", "sv": "Sortera efter"},
    "sort_score_desc":      {"en": "Score (high to low)", "sv": "Betyg (högst först)"},
    "sort_score_asc":       {"en": "Score (low to high)", "sv": "Betyg (lägst först)"},
    "sort_price_asc":       {"en": "Price (low to high)", "sv": "Pris (lägst först)"},
    "sort_price_desc":      {"en": "Price (high to low)", "sv": "Pris (högst först)"},
    "sort_servers_desc":    {"en": "Most servers", "sv": "Flest servrar"},
    "sort_devices_desc":    {"en": "Most devices", "sv": "Flest enheter"},
    "sort_free_desc":       {"en": "Free tier first", "sv": "Gratisnivå först"},
    "sort_guarantee_desc":  {"en": "Longest guarantee", "sv": "Längst ångerrätt"},
    "sort_rank_asc":        {"en": "Ranking order", "sv": "Rankningsordning"},
    "our_score":            {"en": "Our score", "sv": "Vårt betyg"},

    # cmp empty
    "cmp_empty":            {"en": "No provider matches those filters. Try widening them.", "sv": "Ingen leverantör matchar filtren. Prova att bredda dem."},
    "results":             {"en": "providers shown", "sv": "leverantörer visas"},
    "renew_price":         {"en": "Watch the renewal price", "sv": "Se förnyelsepriset"},

    # guarantee
    "guarantee_unit":       {"en": "days", "sv": "dagar"},

    # term
    "term":                 {"en": "Term", "sv": "Avtalslängd"},
    "best_value":           {"en": "Best value", "sv": "Bäst pris"},
    "alt_currency":         {"en": "Also in USD", "sv": "Även i USD"},
    "all_faq":              {"en": "Read all questions", "sv": "Läs alla frågor"},
    "of_ten":               {"en": "of 11", "sv": "av 11"},
    "our_score":            {"en": "Our score", "sv": "Vårt betyg"},
    "best_option":          {"en": "Strongest option", "sv": "Starkaste alternativet"},
    "score_basis":          {"en": "How it is scored", "sv": "Hur det betygsätts"},

    # compare page
    "col_criterion":        {"en": "Criterion", "sv": "Kriterium"},
    "col_weight":           {"en": "Weight", "sv": "Vikt"},
    "showing_all":          {"en": "Showing all {n} providers", "sv": "Visar alla {n} leverantörer"},
    "showing":              {"en": "Showing {a} of {b} providers", "sv": "Visar {a} av {b} leverantörer"},
    "compare_cta_arrow":    {"en": "Compare", "sv": "Jämför"},
    "copy_link":            {"en": "Copy link to this view", "sv": "Kopiera länk till den här vyn"},
    "copied":               {"en": "Link copied", "sv": "Länken kopierad"},
    "back_to_top":          {"en": "Back to top", "sv": "Till toppen"},

    # pricing / plan picker on review pages
    "plan_choose":          {"en": "Choose a plan", "sv": "Välj plan"},
    "plan_selected":        {"en": "Selected plan", "sv": "Vald plan"},
    "total_price":          {"en": "Total price", "sv": "Totalpris"},
    "renew_note":           {"en": "Renews at the standard price", "sv": "Förnyas till standardpris"},

    # how-we-test
    "score_model":          {"en": "Published scoring model", "sv": "Publicerad betygsmodell"},
    "score_model_body":     {"en": "Every score on this site is the weighted sum of five components. The weights are the same for all eleven providers and never change to suit one of them.",
                             "sv": "Varje betyg på den här webbplatsen är den viktade summan av fem komponenter. Vikterna är desamma för alla elva leverantörer och ändras aldrig för att passa någon av dem."},
    "score_model_foot":     {"en": "Affiliate commission is not one of the five components.",
                             "sv": "Affiliateprovision ingår inte bland de fem komponenterna."},

    # compare page
    "eyebrow_compare":      {"en": "Every number we publish", "sv": "Varje siffra vi publicerar"},
    "verified_on":          {"en": "Prices and facts verified on {date}.", "sv": "Priser och fakta verifierade {date}."},

    # reviews index
    "reviews_index_eyebrow": {"en": "Provider reviews", "sv": "Leverantörsrecensioner"},
    "reviews_index_title":   {"en": "All 11 VPN reviews", "sv": "Alla 11 VPN-recensioner"},
    "reviews_index_lede":    {"en": "Eleven providers, ranked by our published method. Each review states what we did and did not verify, what the score is actually based on, and who it suits.",
                              "sv": "Elva leverantörer, rankade med vår publicerade metod. Varje recension anger vad vi gjorde och inte gjorde, vad betyget faktiskt bygger på och vem det passar."},

    # review page
    "review_title_fmt":     {"en": "{name} review", "sv": "{name} recension"},
    "review_h1_fmt":        {"en": "{name} review", "sv": "{name} recension"},

    "cta_label":            {"en": "Check current price", "sv": "Kontrollera aktuellt pris"},
    "cta_home_title":       {"en": "See all eleven providers side by side",
                             "sv": "Se alla elva leverantörer sida vid sida"},
    "cta_home_body":        {"en": "Filter by what you need, compare every figure we publish, and open any row to read why a provider scored the way it did.",
                             "sv": "Filtrera på det du behöver, jämför alla siffror vi publicerar och öppna en rad för att läsa varför en leverantör fick sitt betyg."},

    "ld_itemlist_home":     {"en": "Best VPNs 2026, ranked by published method",
                             "sv": "Bästa VPN 2026, rankade med publicerad metod"},

    "audit_source":         {"en": "Audit evidence cited: {firm}. We summarise publicly available reports and do not have access to the underlying working papers.",
                             "sv": "Revisionsbevis som citeras: {firm}. Vi sammanfattar offentligt tillgängliga rapporter och har inte tillgång till underlaget."},
    "audit_source_none":    {"en": "No independent audit has been published that we could find. We summarise the provider's own policy documents instead, and say so wherever the claim matters.",
                             "sv": "Ingen oberoende revision har publicerats vad vi kunnat hitta. Vi sammanfattar i stället leverantörens egna policydokument, och säger det där påståendet spelar roll."},
    "not_published":        {"en": "Not published", "sv": "Inte publicerat"},
    "price_caveat":         {"en": "Prices change frequently and are set by the provider. The date above is when we last verified them; the provider's checkout is always authoritative, and you will never be charged the wrong amount because of an error here.",
                             "sv": "Priser ändras ofta och sätts av leverantören. Datumet ovan är när vi senast verifierade dem; leverantörens kassa är alltid auktoriteten, och du kommer aldrig att debiteras fel på grund av ett fel här."},
    "renew_explainer":      {"en": "The promotional price on {name} only applies to the initial term. Before you buy, check what the provider charges to renew, and set a reminder for the cancellation deadline in the last month of that term. A 30-day window is the standard escape hatch, but it does not exist in every plan.",
                             "sv": "Kampanjpriset för {name} gäller bara den första avtalslängden. Kontrollera vad leverantören tar för förnyelse innan du köper, och sätt en påminnelse om uppsägningsfristen under den sista månaden av avtalslängden. 30 dagars ångerrätt är den vanliga vägen ut, men den finns inte i alla planer."},
    "streaming_heading":    {"en": "Streaming and unblocking", "sv": "Streaming och upplåsning"},
    "better_at":            {"en": "{here} scores {here_score} on value against {other_score} for {other}.",
                             "sv": "{here} får {here_score} på värde mot {other_score} för {other}."},

    # facets
    "facet_jurisdiction":   {"en": "Jurisdiction", "sv": "Jurisdiktion"},
    "facet_alliance":       {"en": "Intelligence alliance", "sv": "Underrättelseallians"},
    "facet_owner":          {"en": "Ownership", "sv": "Ägande"},
    "facet_launched":       {"en": "Founded", "sv": "Grundat"},
    "facet_ram":            {"en": "RAM-only servers", "sv": "RAM-servrar"},
    "facet_opensource":     {"en": "Open-source apps", "sv": "Källkodsöppna appar"},
    "facet_audit":          {"en": "Independent audits", "sv": "Oberoende revisioner"},
    "facet_court":          {"en": "Tested in court", "sv": "Provat i domstol"},
    "facet_court_evidence": {"en": "Evidence of a real test", "sv": "Bevis på ett verkligt test"},
    "facet_anon_signup":    {"en": "Anonymous signup", "sv": "Anonym registrering"},
    "facet_crypto":         {"en": "Crypto payment", "sv": "Kryptobetalning"},
    "facet_transparency":   {"en": "Transparency report", "sv": "Transparensrapport"},
    "facet_servers":        {"en": "Servers", "sv": "Servrar"},
    "facet_countries":      {"en": "Countries", "sv": "Länder"},
    "facet_protocols":      {"en": "Protocols", "sv": "Protokoll"},
    "facet_devices":        {"en": "Simultaneous devices", "sv": "Samtidiga enheter"},
    "facet_guarantee":      {"en": "Money-back window", "sv": "Ångerrättsfönster"},
    "facet_free":           {"en": "Free allowance", "sv": "Gratisvolym"},
    "facet_trial":          {"en": "Free trial", "sv": "Gratisperiod"},
    "eye_in_alliance":      {"en": "Inside the alliance", "sv": "Inuti alliansen"},

    # faq
    "faq_eyebrow":          {"en": "Questions and answers", "sv": "Frågor och svar"},
    "faq_title":            {"en": "VPN questions, answered honestly", "sv": "VPN-frågor, ärligt besvarade"},
    "faq_lede":             {"en": "The questions people actually ask us, including the ones where the honest answer is that a VPN is not the right tool.",
                             "sv": "Frågorna folk faktiskt ställer oss, inklusive de där det ärliga svaret är att en VPN inte är rätt verktyg."},

    # provider FAQ
    "pf_q_price":           {"en": "How much does {name} cost?", "sv": "Hur mycket kostar {name}?"},
    "pf_a_price":           {"en": "The cheapest plan we list works out at {monthly} per month for {term}, which is {total} in total. That figure can change at any time — we last verified it on the date shown above — and it is the effective cost of the whole subscription rather than a headline monthly rate. You get {days} days to change your mind.",
                             "sv": "Det billigaste plan vi listar blir {monthly} per månad i {term}, vilket är {total} totalt. Siffran kan ändras när som helst — vi verifierade den senast datumet ovan — och det är hela prenumerationens effektiva kostnad, inte en rubriksats per månad. Du har {days} dagar att ändra dig."},
    "pf_q_audit":           {"en": "Can {name} really be trusted not to log my data?", "sv": "Kan {name} verkligen litas på att inte logga mina data?"},
    "pf_a_audit":           {"en": "The claim is supported by {count} independent audit engagements with {firm}, the most recent dated {latest}. RAM-only servers: {ram}. Intelligence alliance membership: {alliance}. Real-world legal test: {court}. We rate what is verifiable rather than what is promised, which is why this answer scores the way it does.",
                             "sv": "Påståendet stöds av {count} oberoende revisionsuppdrag med {firm}, det senaste daterat {latest}. RAM-servrar: {ram}. Medlemskap i underrättelseallians: {alliance}. Verkligt rättsligt test: {court}. Vi betygsätter det som går att verifiera snarare än det som lovas, och det är därför det här svaret får sitt betyg."},
    "pf_q_score":           {"en": "Why does {name} score what it scores?", "sv": "Varför får {name} det betyg det får?"},
    "pf_a_score":           {"en": "{name} scores {score} out of 10, which places it number {rank} of the eleven we review, under the badge '{badge}'. The score is a weighted sum of privacy, speed, value, streaming and ease of use, with the weights published in full on our methodology page. Affiliate commission had no influence on any component of it.",
                             "sv": "{name} får {score} av 10, vilket placerar det som nummer {rank} av de elva vi recenserar, under märket '{badge}'. Betyget är en viktad summa av integritet, hastighet, värde, streaming och användarvänlighet, med vikterna publicerade i sin helhet på vår metodsida. Affiliateprovision påverkade ingen enda komponent av det."},
    "pf_court_yes":         {"en": "yes — there is a documented case", "sv": "ja — det finns ett dokumenterat fall"},
    "pf_court_no":          {"en": "not published", "sv": "inte publicerat"},
    "pf_a_audit_none":      {"en": "No independent audit of {name} has been published that we could find, so there is no external check on the logging claim. RAM-only servers: {ram}. Intelligence alliance membership: {alliance}. Real-world legal test: {court}. The privacy score reflects that gap: a policy promise without verification scores below verified ones, and affiliate commission had no influence on any component of it.",
                             "sv": "Ingen oberoende revision av {name} har publicerats vad vi kunnat hitta, så det finns ingen extern kontroll av loggfrihetspåståendet. RAM-servrar: {ram}. Medlemskap i underrättelseallians: {alliance}. Verkligt rättsligt test: {court}. Integritetsbetyget speglar det glappet: ett policylöfte utan verifiering får lägre poäng än verifierade, och affiliateprovision påverkade ingen enda komponent av det."},

    # best-vpn-for money pages (shared section labels; {topic} = page topic)
    "bfv_eyebrow":          {"en": "Best VPN for", "sv": "Bäst VPN för"},
    "bfv_picks_title":      {"en": "Top 3 for {topic}", "sv": "Topp 3 för {topic}"},
    "bfv_picks_note":       {"en": "Ordered by how well each one fits this task, not by our overall ranking — every score here is the score on that provider's review.",
                             "sv": "Ordnade efter hur väl de passar uppgiften, inte efter vår totalplacering — varje betyg här är samma betyg som på leverantörens recension."},
    "bfv_why_title":        {"en": "How we chose", "sv": "Så valde vi"},
    "bfv_criteria_title":   {"en": "What this guide weighs", "sv": "Vad den här guiden viktlägger"},
    "bfv_criteria_caption": {"en": "The five published components, re-weighted for this task",
                             "sv": "De fem publicerade komponenterna, omviktlagda för uppgiften"},
    "bfv_table_title":      {"en": "All eleven, side by side", "sv": "Alla elva, sida vid sida"},
    "bfv_table_lede":       {"en": "The full table with the same published scores. Sort it here, or open the main comparison with filters.",
                             "sv": "Hela tabellen med samma publicerade betyg. Sortera den här, eller öppna huvudjämförelsen med filter."},
    "bfv_review_link":      {"en": "Full review", "sv": "Hela recensionen"},
    "bfv_faq_title":        {"en": "Common questions about {topic}", "sv": "Vanliga frågor om {topic}"},
    "bfv_related_title":    {"en": "More best-VPN guides", "sv": "Fler guider"},
    "bfv_related_lede":     {"en": "Twelve guides, one per task. Pick the job you actually have.",
                             "sv": "Tolv guider, en per uppgift. Välj det jobb du faktiskt har."},
    "bfv_cta_title":        {"en": "Ready to pick a VPN for {topic}?", "sv": "Redo att välja VPN för {topic}?"},
    "bfv_cta_body":         {"en": "All eleven providers, with the same published scores this guide is built on — no separate list, no inflated numbers.",
                             "sv": "Alla elva leverantörer, med samma publicerade betyg som den här guiden bygger på — ingen separat lista, inga uppblåsta siffror."},
    "bfv_hub_faq_title":    {"en": "How these guides work", "sv": "Så fungerar de här guiderna"},
    "bfv_hub_link":         {"en": "All best-VPN guides", "sv": "Alla guider"},
    "bfv_read":             {"en": "Read guide", "sv": "Läs guiden"},

    # home page section linking into the money pages
    "home_guides_title":    {"en": "Best VPN for the job you actually have",
                             "sv": "Bäst VPN för jobbet du faktiskt har"},
    "home_guides_lede":     {"en": "Twelve task-specific guides — streaming, Netflix, gaming, "
                                   "torrenting, privacy, travel, phones, desktops and routers — "
                                   "each with published weights and a top three.",
                             "sv": "Tolv guider per uppgift — streaming, Netflix, gaming, "
                                   "torrenting, integritet, resor, mobiler, datorer och routrar — "
                                   "var och en med publicerade vikter och en topp 3."},

    # informational section (/vpn-explained/)
    "explained_hub_link":   {"en": "VPN explained", "sv": "VPN förklarat"},
    "explained_eyebrow":    {"en": "VPN explained", "sv": "VPN förklarat"},
    "explained_home_title": {"en": "New to VPNs? Start here",
                             "sv": "Ny med VPN? Börja här"},
    "explained_home_lede":  {"en": "Plain answers to the questions people ask before they "
                                   "subscribe — no jargon, and no claim we cannot show you "
                                   "the source for.",
                             "sv": "Svar på frågorna folk ställer innan de prenumererar — "
                                   "utan sjargong och utan påståenden vi inte kan belägga."},
    "explained_hub_title":  {"en": "Every explainer, in one place",
                             "sv": "Alla förklaringar på ett ställe"},
    "explained_hub_lede":   {"en": "The questions readers ask before they buy, written from "
                                   "the same published scores as the comparison.",
                             "sv": "Frågorna läsare ställer innan de köper, skrivna med samma "
                                   "publicerade betyg som jämförelsen."},
    "explained_faq_title":  {"en": "Frequently asked questions", "sv": "Vanliga frågor"},
    "explained_related_title": {"en": "Where this connects", "sv": "Var det här kopplar vidare"},
    "explained_related_lede":  {"en": "The reviews and task guides this answer points to, each "
                                      "with the scores behind it.",
                                "sv": "De recensioner och uppgiftsguider det här svaret pekar "
                                      "på, med betygen bakom var och en."},
    "explained_read":       {"en": "Read", "sv": "Läs"},

    # breadcrumb root
    "nav_home":             {"en": "Home", "sv": "Hem"},

    # skip link
    "skip_to_content":      {"en": "Skip to content", "sv": "Hoppa till innehållet"},
}



BENEFITS = {
    "en": [
        ("scale", "Court and audit evidence, not promises",
         "We look for a named auditor with a date, and for documented cases where a provider "
         "was legally compelled to produce data. A promise in a privacy policy is the weakest "
         "form of evidence there is."),
        ("scale", "Full prices, never the fake one",
         "Every provider advertises a price that only exists if you commit for two years. We "
         "show the total you pay, the monthly equivalent, and what happens when it renews."),
        ("refresh", "Prices checked on a schedule",
         "Prices change constantly. Every price on this site carries the date it was last "
         "verified, and we re-check the whole list on a fixed cycle."),
        ("eye", "Eye alliances explained, not assumed",
         "Jurisdiction decides who can order a VPN company to hand over records. We say which "
         "country each provider sits in and whether it is inside 5, 9 or 14 Eyes."),
        ("code", "Open source is marked",
         "Providers whose clients you can read on GitHub are flagged separately from those "
         "asking you to trust them."),
        ("tag", "No provider pays for a position",
         "Commission rates never enter the scoring. If a provider paid us more we still score "
         "them the same way, and we say so on the methodology page."),
    ],
    "sv": [
        ("scale", "Domstols- och revisionsbevis, inte löften",
         "Vi söker en namngiven revisor med datum och dokumenterade fall där en leverantör "
         "rättsligt tvingats lämna ut data. Ett löfte i en integritetspolicy är den svagaste "
         "formen av evidens som finns."),
        ("tag", "Hela priset, aldrig det falska",
         "Varje leverantör annonserar ett pris som bara existerar om du binder dig i två år. "
         "Vi visar totalen du betalar, månadsekvivalenten och vad som händer vid förnyelse."),
        ("refresh", "Priser kontrollerade enligt schema",
         "Priser ändras ständigt. Varje pris på den här webbplatsen bär datum för senaste "
         "verifiering, och vi kontrollerar hela listan i en fast cykel."),
        ("eye", "Eyes-allianser förklarade, inte förutsatta",
         "Jurisdiktion avgör vem som kan beordra en VPN-leverantör att lämna ut register. Vi "
         "säger vilket land varje leverantör sitter i och om det ligger inom 5, 9 eller 14 Eyes."),
        ("code", "Källkod öppen är märkt",
         "Leverantörer vars klienter du kan läsa på GitHub märks separat från dem som ber dig "
         "lita på dem."),
        ("refresh", "Ingen leverantör betalar för sin plats",
         "Provisionssatser ingår aldrig i betygsättningen. Om en leverantör betalade oss mer "
         "så skulle vi fortfarande betygsätta dem likadana, och vi säger det på metodsidan."),
    ],
}


HOME = {
    "en": {
        "eyebrow": "Independent reviews · English & Swedish",
        "h1": "The 11 best VPNs, scored by a method we publish",
        "lede": (
            "We test what can be tested, cite what cannot, and show our full weighting so you "
            "can argue with us. Eleven providers, no paid positions, no invented benchmark numbers."
        ),
        "cta_primary": "See the full comparison",
        "cta_secondary": "Read how we rank",
        "trust": [
            "Prices verified {date}",
            "11 providers reviewed",
            "Commission never affects scores",
        ],
        "top_eyebrow": "Recommendations",
        "top_title": "Our top three",
        "top_lede": (
            "If you only read one section, read this one. Each pick is the strongest option for "
            "a different reason, so the right choice depends on which one matters to you."
        ),
        "compare_eyebrow": "Side by side",
        "compare_title": "All eleven, side by side",
        "compare_lede": (
            "The full table with every number we have. Filter by what you actually need."
        ),
        "compare_cta": "Open the filterable comparison",
        "why_title": "How we decide",
        "why_lede": (
            "Most VPN comparison sites are advertising with a table attached. Here is exactly "
            "what we do instead, in enough detail that you can reproduce it."
        ),
        "usecase_title": "Start from what you need",
        "usecase_lede": "Pick a situation and we will point you at the provider that wins it.",
        "method_title": "Our weighting, in the open",
        "method_lede": (
            "Every score on this site is a weighted sum of five components. The weights never "
            "change to suit a provider — that is the whole point of publishing them."
        ),
        "faq_title": "Straight answers",
        "method_cta": "Read the full method",
    },
    "sv": {
        "eyebrow": "Oberoende recensioner · Engelska & svenska",
        "h1": "De 11 bästa VPN:erna, betygsatta med en publicerad metod",
        "lede": (
            "Vi testar det som går att testa, citerar det som inte gör det och visar hela "
            "vikningen så att du kan argumentera mot oss. Elva leverantörer, inga betalda "
            "placeringar, inga påhittade mätvärden."
        ),
        "cta_primary": "Se hela jämförelsen",
        "cta_secondary": "Läs hur vi rankar",
        "trust": [
            "Priser verifierade {date}",
            "11 leverantörer recenserade",
            "Provision påverkar aldrig betyg",
        ],
        "top_eyebrow": "Rekommendationer",
        "top_title": "Våra tre bästa",
        "top_lede": (
            "Om du bara läser en sektion, läs den här. Varje val är det starkaste alternativet "
            "av olika skäl, så rätt val beror på vilken av dem som spelar roll för dig."
        ),
        "compare_eyebrow": "Sida vid sida",
        "compare_title": "Alla elva, sida vid sida",
        "compare_lede": (
            "Hela tabellen med varje siffra vi har. Filtrera på det du faktiskt behöver."
        ),
        "compare_cta": "Öppna den filtrerbara jämförelsen",
        "why_title": "Hur vi bestämmer",
        "why_lede": (
            "De flesta VPN-jämförelsesajter är reklam med en bifogad tabell. Här är exakt vad "
            "vi gör i stället, i tillräcklig detalj för att du ska kunna reproducera det."
        ),
        "usecase_title": "Börja med vad du behöver",
        "usecase_lede": "Välj en situation så pekar vi ut leverantören som vinner den.",
        "method_title": "Vår vikning, öppen",
        "method_lede": (
            "Varje betyg på den här webbplatsen är en viktad summa av fem komponenter. Vikterna "
            "ändras aldrig för att passa en leverantör — det är hela poängen med att publicera dem."
        ),
        "faq_title": "Raka svar",
        "method_cta": "Läs hela metoden",
    },
}


COMPARE = {
    "en": {
        "eyebrow": "Full comparison",
        "h1": "Compare all 11 VPNs",
        "lede": (
            "Every figure we publish, in one filterable table. Sort by what matters, search by "
            "name or country, and open any row to read the reasoning."
        ),
        "results": "providers shown",
            "empty": "No provider matches those filters. Try widening them.",
    "cmp_empty": "No provider matches those filters. Try widening them.",
        "notes_title": "How to read this table",
        "notes": [
            ("tag", "Prices are what you actually pay",
             "The per-month figure is the effective cost of the longest term we list. The total "
             "next to it is what leaves your account. Renewal prices are usually higher and are "
             "the provider's own published rate, not ours."),
            ("eye", "Jurisdiction is a legal fact, not a quality judgement",
             "A provider registered in a Five, Nine or Fourteen Eyes country sits inside a "
             "data-sharing alliance. That does not make it dishonest — it changes what a "
             "government can compel. Where a provider has been subpoenaed and produced nothing, "
             "we say so."),
            ("audit", "Audit counts are dated and named",
             "We count independent assurance engagements against the no-logs claim, not company "
             "blog posts. Apps-only audits are noted but not counted the same as infrastructure "
             "audits."),
            ("clock", "Prices are verified on a schedule",
             "Every figure was last checked on the date shown at the top of this page. If a price "
             "has changed since, the provider's own checkout is always the authority."),
        ],
        "disclosure_title": "Straight about what this is",
        "disclosure": (
            "This is a comparison site funded by affiliate commissions. When you click through "
            "to a provider and buy, we may receive money. It does not change your price and it "
            "does not change where a provider appears in this table. Providers cannot pay to be "
            "ranked higher, and we do not accept payment for reviews."
        ),
        "faq_title": "Comparison questions",
    },
    "sv": {
        "eyebrow": "Fullständig jämförelse",
        "h1": "Jämför alla 11 VPN",
        "lede": (
            "Varje siffra vi publicerar, i en filtrerbart tabell. Sortera på det som spelar "
            "roll, sök på namn eller land, och öppna en rad för att läsa resonemanget."
        ),
        "results": "leverantörer visas",
        "empty": "Ingen leverantör matchar filtren. Prova att bredda dem.",
        "notes_title": "Så läser du tabellen",
        "notes": [
            ("tag", "Priserna är vad du faktiskt betalar",
             "Månadssiffran är effektiv kostnad för den längsta avtalslängd vi listar. "
             "Totalen bredvid är vad som lämnar ditt konto. Förnyelsepriser är normalt högre "
             "och är leverantörens egna publicerade pris, inte vårt."),
            ("eye", "Jurisdiktion är en juridisk fakta, inte ett kvalitetsomdöme",
             "En leverantör registrerad i ett Five-, Nine- eller Fourteen Eyes-land ligger inuti "
             "en datadelningsallians. Det gör den inte oärlig — det förändrar vad en regering "
             "kan tvinga fram. Där en leverantör blivit kallad och inte lämnat ut något säger vi det."),
            ("audit", "Revisionsantal är daterade och namngivna",
             "Vi räknar oberoende försäkringsengagemang mot loggfrihetspåståendet, inte "
             "företagsblogginlägg. Revisioner som bara gäller appar noteras men räknas inte "
             "samma som infrastrukturrevisioner."),
            ("clock", "Priser verifieras enligt schema",
             "Alla siffror kontrollerades senast det datum som visas överst på den här sidan. "
             "Om ett pris ändrats sedan är leverantörens egen kassa alltid auktoriteten."),
        ],
        "disclosure_title": "Rakt ut om vad det här är",
        "disclosure": (
            "Det här är en jämförelsetjänst som finansieras av affiliateprovisioner. När du "
            "klickar vidare till en leverantör och köper kan vi få pengar. Det påverkar inte "
            "ditt pris och det påverkar inte var en leverantör hamnar i tabellen. Leverantörer "
            "kan inte betala för att rankas högre, och vi tar inte betalt för recensioner."
        ),
        "faq_title": "Jämförelsefrågor",
    },
}


REVIEW = {
    "en": {
        "verdict_label": "Our verdict",
        "scores_title": "Score breakdown",
        "scores_lede": (
            "The weighted total, and what each component contributed. Weights are published "
            "and identical across all eleven providers."
        ),
        "basis_label": "Why we scored it this way",
        "privacy_title": "Privacy and logging",
        "network_title": "Network, protocols and speed",
        "price_title": "Pricing",
        "who_title": "Who it suits",
        "who_body": "idealFor",
        "bench_title": "A note on our speed score",
        "bench_body": (
            "We have not run our own speed benchmarks, so we do not pretend we have. This speed "
            "score is an editorial estimate built from network architecture — protocol support, "
            "RAM-only versus disk infrastructure, server density and dedicated streaming "
            "capacity — together with findings from published independent reviews. It is a "
            "reliable indicator of which providers are fast in general. It is not a measurement "
            "of your line, your ISP or your home."
        ),
        "renew_title": "Read the renewal price",
        "alternatives_title": "How it compares",
        "alternatives_lede": (
            "Where this provider wins and where it does not, against the two nearest "
            "alternatives on our list."
        ),
        "vs_win": "Better than",
        "vs_lose": "Weaker than",
        "faq_title": "{name} questions",
        "cta_title": "Try {name}",
        "cta_body": (
            "Check the current price and the terms of the plan you want before you commit. "
            "Every plan here includes a money-back window, so the first decision is reversible."
        ),
        "update_note": "Prices and facts last verified",
    },
    "sv": {
        "verdict_label": "Vårt omdöme",
        "scores_title": "Poängfördelning",
        "scores_lede": (
            "Det viktade totalt och vad varje komponent bidrog med. Vikterna är publicerade "
            "och identiska för alla elva leverantörer."
        ),
        "basis_label": "Varför vi betygsatte så här",
        "privacy_title": "Integritet och loggning",
        "network_title": "Nätverk, protokoll och hastighet",
        "price_title": "Pris",
        "who_title": "Vem det passar",
        "who_body": "idealFor",
        "bench_title": "En anmärkning om vårt hastighetsbetyg",
        "bench_body": (
            "Vi har inte kört våra egna hastighetstester och låtsas inte att vi har gjort det. "
            "Det här hastighetsbetyget är en redaktionell uppskattning byggd på nätverkets "
            "arkitektur — protokollstöd, RAM-baserad mot diskbaserad infrastruktur, "
            "servertäthet och dedikerad streamingkapacitet — tillsammans med resultat från "
            "publicerade oberoende recensioner. Det är en tillförlitlig indikator på vilka "
            "leverantörer som är snabba generellt. Det är inte en mätning av din linje, din "
            "internetleverantör eller ditt hem."
        ),
        "renew_title": "Läs förnyelsepriset",
        "alternatives_title": "Hur det står sig",
        "alternatives_lede": (
            "Var den här leverantören vinner och inte vinner, mot de två närmaste alternativen "
            "i vår lista."
        ),
        "vs_win": "Bättre än",
        "vs_lose": "Svagare än",
        "faq_title": "Frågor om {name}",
        "cta_title": "Prova {name}",
        "cta_body": (
            "Kontrollera det aktuella priset och villkoren för den plan du vill ha innan du "
            "binder dig. Alla planer här har ett ångerrättsfönster, så det första beslutet är "
            "reversibelt."
        ),
        "update_note": "Priser och fakta senast verifierade",
    },
}


HOW_WE_TEST = {
    "en": {
        "eyebrow": "Methodology",
        "h1": "Exactly how we rank VPNs",
        "lede": (
            "Swedish law requires comparison services to tell consumers what criteria determine "
            "their ranking and how much each criterion counts. This page is that disclosure, "
            "written so you can check our work rather than take it on trust."
        ),
        "why_title": "Why we publish this",
        "why_body": [
            "From September 2022, Swedish marketing law requires comparison services and "
            "marketplaces to inform consumers which criteria determine the ranking of offers, "
            "and what those criteria weigh relative to each other. Most comparison sites "
            "ignore this. We would rather comply and be checkable.",
            "There is a second reason. Affiliate comparison sites are structurally conflicted: "
            "the more providers we recommend, the more we earn. Publishing the weighting makes "
            "that conflict visible and limits how far it can distort the result.",
            "If you find a real error, we want to know. Corrections are made transparently and "
            "the change is dated.",
        ],
        "weights_title": "The weighting",
        "weights_lede": (
            "These five weights are fixed. They apply identically to every provider, they do "
            "not change seasonally, and no provider is ever exempt from them."
        ),
        "defs_title": "What each score measures",
        "indep_title": "What affiliate status can and cannot do",
        "indep_body": [
            ("bad", "Commission rates never enter the scoring",
             "The percentage we might receive has no weight in any of the five components. A "
             "provider paying 100% of the first sale scores exactly the same as one paying 20%."),
            ("bad", "No provider can pay for a position",
             "Nobody at this site can accept a payment in exchange for a rank, a badge or a "
             "higher score. Commercial terms offered by providers are declined where they "
             "attach to editorial outcomes."),
            ("good", "Commission does affect what we can afford to do",
             "Funding pays for the site to exist. It lets us keep the review length, the "
             "verification dates and the free comparison genuinely free rather than paywalled."),
            ("good", "Free products count as payment",
             "If we ever receive a VPN subscription to test one, that is compensation and we "
             "will say so on the review."),
        ],
        "limits_title": "The limits of our method",
        "limits": [
            "We do not run our own throughput benchmarks. Our speed score is an architectural "
            "estimate combined with published third-party results, and every review says so.",
            "We cannot verify a provider's internal code unless the client is open source. "
            "Where it is not, we say that and explain what it means.",
            "Audit findings are summarised from publicly available reports. We do not have "
            "access to the underlying evidence, and we do not imply that we do.",
            "Server counts are the providers' own published figures and are not independently "
            "verified. We date them.",
            "Prices change daily. The date of last verification is shown on every price, and "
            "the provider's checkout is always the authority if the two disagree.",
        ],
        "remove_title": "How a provider is removed",
        "remove_body": (
            "We remove a provider if its no-logs claim is contradicted by documented evidence, "
            "if it is found to have misrepresented a material feature, if it becomes "
            "unreachable for a sustained period, or if we cannot verify basic facts such as "
            "jurisdiction. A provider paying less commission is not a reason for removal, and "
            "neither is a provider paying more."
        ),
        "correct_title": "Corrections",
        "correct_body": (
            "Corrections are made in place and dated. We do not silently delete a claim we got "
            "wrong — the change history is part of the record. Email corrections to the address "
            "in the footer."
        ),
        "weights_table_caption": "Published scoring weights, applied identically to all eleven providers",
    },
    "sv": {
        "eyebrow": "Metod",
        "h1": "Exakt hur vi rankar VPN",
        "lede": (
            "Svensk lag kräver att jämförelsetjänster informerar konsumenter om vilka kriterier "
            "som avgör rankningen och hur mycket de väger. Den här sidan är den upplysningen, "
            "skriven så att du kan kontrollera vårt arbete i stället för att lita på det."
        ),
        "why_title": "Varför vi publicerar detta",
        "why_body": [
            "Från september 2022 kräver svensk marknadsföringslag att jämförelsetjänster och "
            "marknadsplatser informerar om vilka kriterier som avgör hur erbjudanden rankas och "
            "hur deras inbördes tyngd väger. De flesta jämförelsesajter struntar i det. Vi väljer "
            " hellre att följa regeln och vara kontrollerbara.",
            "Det finns en andra anledning. Affiliate-jämförelsesajter är strukturellt i "
            "konflikt: ju fler leverantörer vi rekommenderar, desto mer tjänar vi. Att "
            "publicera vikningen gör konflikten synlig och begränsar hur mycket den kan "
            "förvränga resultatet.",
            "Om du hittar ett verkligt fel vill vi veta det. Korrigeringar görs öppet och "
            "ändringen dateras.",
        ],
        "weights_title": "Vikningen",
        "weights_lede": (
            "Dessa fem vikter är fasta. De gäller identiskt för varje leverantör, de ändras "
            "inte säsongsmässigt och ingen leverantör är undantagen från dem."
        ),
        "defs_title": "Vad varje betyg mäter",
        "indep_title": "Vad affiliatesstatus kan och inte kan göra",
        "indep_body": [
            ("bad", "Provisioner ingår aldrig i betygsättningen",
             "Procentsatsen vi kan få har ingen tyngd i någon av de fem komponenterna. En "
             "leverantör som betalar 100 % av första försäljningen får exakt samma betyg som "
             "en som betalar 20 %."),
            ("bad", "Ingen leverantör kan betala för sin plats",
             "Ingen på den här webbplatsen kan ta emot en betalning mot en placering, ett märke "
             "eller ett högre betyg. Kommersiella villkor som kopplas till redaktionella "
             "utfall avböjs."),
            ("good", "Provision påverkar vad vi har råd att göra",
             "Finansieringen betalar för att webbplatsen ska finnas. Den låter oss hålla "
             "recensionslängden, verifieringsdatumen och den kostnadsfria jämförelsen genuint "
             "gratis i stället för låst."),
            ("good", "Gratis produkter räknas som betalning",
             "Om vi någång får en VPN-prenumeration för att testa den är det ersättning, och "
             "det kommer att stå på recensionen."),
        ],
        "limits_title": "Våra metoders gränser",
        "limits": [
            "Vi kör inte våra egna genomströmningstester. Vårt hastighetsbetyg är en arkitektur-"
            "uppskattning kombinerad med publicerade tredjepartsresultat, och varje recension "
            "säger det.",
            "Vi kan inte verifiera en leverantörs interna kod om inte klienten är källkodsöppen. "
            "Där den inte är det säger vi det och förklarar vad det betyder.",
            "Revisionsfynd sammanfattas från offentligt tillgängliga rapporter. Vi har inte "
            "tillgång till underlaget och låtsas inte att vi har det.",
            "Serverantal är leverantörernas egna publicerade siffror och verifieras inte "
            "oberoende. Vi daterar dem.",
            "Priser ändras dagligen. Datum för senaste verifiering visas vid varje pris, och "
            "leverantörens kassa är alltid auktoriteten om de två skiljer sig åt.",
        ],
        "remove_title": "Hur en leverantör tas bort",
        "remove_body": (
            "Vi tar bort en leverantör om dess loggfrihetspåstående motsägs av dokumenterad "
            "evidens, om det visar sig ha vilselett om en väsentlig funktion, om den blir "
            "otillgänglig under längre period, eller om vi inte kan verifiera grundläggande "
            "fakta som jurisdiktion. Att en leverantör betalar mindre provision är ingen anledning "
            "till borttagning, och inte heller att den betalar mer."
        ),
        "correct_title": "Korrigeringar",
        "correct_body": (
            "Korrigeringar görs på plats och dateras. Vi raderar inte tyst ett påstående vi "
            "gjort fel — ändringshistoriken är en del av dokumentationen. Skicka korrigeringar "
            "till adressen i sidfoten."
        ),
        "weights_table_caption": "Publicerade vikter, tillämpade identiskt på alla elva leverantörer",
    },
}


SCORE_DEFS = {
    "privacy": {
        "en": ("Privacy and logging",
               "Jurisdiction and data-retention law; membership of the 5/9/14-Eyes alliances; "
               "independent audits of the no-logs claim with a named firm and date; whether "
               "servers are RAM-only, which makes retention structurally impossible; documented "
               "cases of legal compulsion; how much identifying information signup collects."),
        "sv": ("Integritet och loggning",
               "Jurisdiktion och lagstiftning om databehållning; medlemskap i 5/9/14-Eyes-"
               "allianserna; oberoende revisioner av loggfrihetspåståendet med namngiven "
               "revisor och datum; om servrarna är RAM-baserade, vilket gör behållning "
               "strukturellt omöjlig; dokumenterade fall av rättsligt tvång; hur mycket "
               "identifierande information registreringen samlar in."),
    },
    "speed": {
        "en": ("Speed and reliability",
               "An architectural estimate, not our own benchmark. Protocol support and whether "
               "WireGuard is available; RAM-only versus disk infrastructure; server density and "
               "proximity to major cities; dedicated streaming and gaming capacity; stability "
               "reported in published independent reviews."),
        "sv": ("Hastighet och tillförlitlighet",
               "En arkitekturuppskattning, inte vår egen mätning. Protokollstöd och om "
               "WireGuard finns; RAM-baserad mot diskbaserad infrastruktur; servertäthet och "
               "närhet till större städer; dedikerad streaming- och spelfunktion; stabilitet "
               "rapporterad i publicerade oberoende recensioner."),
    },
    "price": {
        "en": ("Value for money",
               "The effective monthly cost of the longest term offered, weighted against what "
               "the subscription actually delivers — device count, features and network size. "
               "Providers whose renewal price roughly doubles score lower, because the real "
               "cost of a VPN is the second year, not the first."),
        "sv": ("Värde för pengarna",
               "Den effektiva månadskostnaden för längsta avtalslängd, vägt mot vad prenumerationen "
               "faktiskt ger — antal enheter, funktioner och nätverkets storlek. Leverantörer vars "
               "förnyelsepris ungefär fördubblas får lägre poäng, eftersom en VPNs verkliga kostnad "
               "är andra året, inte det första."),
    },
    "streaming": {
        "en": ("Streaming and TV unblocking",
               "How consistently the provider restores geo-blocked catalogues across major "
               "streaming services, whether it maintains dedicated servers for them, and how "
               "often the answer changes. Providers that do not attempt this score low by "
               "design, which we state rather than penalise silently."),
        "sv": ("Upplåsning av streaming och tv",
               "Hur konsekvent leverantören återställer geoblockerade kataloger över stora "
               "streamingtjänster, om de underhåller dedikerade servrar för dem och hur ofta "
               "svaret ändras. Leverantörer som inte försöker score lågt av design, vilket vi "
               "uttalar i stället för att straffa i tysthet."),
    },
    "easeOfUse": {
        "en": ("Apps and ease of use",
               "How quickly a non-technical person can install, connect and trust the app; "
               "whether servers are labelled by purpose; platform coverage including smart TVs "
               "and routers; and whether support is reachable and useful."),
        "sv": ("Appar och användarvänlighet",
               "Hur snabbt en icke-teknisk person kan installera, ansluta och lita på appen; om "
               "servrarna är märkta efter ändamål; plattformstäckning inklusive smart-tv och "
               "routers; och om supporten är nåbar och användbar."),
    },
}


ABOUT = {
    "en": {
        "eyebrow": "About us",
        "h1": "Who runs this site, and why",
        "lede": (
            "We are an independent editorial comparison service publishing in English and "
            "Swedish. We are not affiliated with any VPN provider we review. We are paid by "
            "some of them. Both of those sentences are true at once and you should hold us to "
            "both."
        ),
        "what_title": "What this site is",
        "what_body": [
            "We test, research and compare commercial VPN services. We earn money when you buy "
            "one through our links. That is the entire business model — there is no subscription, "
            "no premium tier and nothing for sale.",
            "We publish in English and Swedish because the same consumer questions deserve the "
            "same answers in both languages, and because most of the largest comparison sites "
            "publish in English only.",
        ],
        "ed_title": "Our editorial rules",
        "ed_body": [
            ("check", "We do not accept payment for a review or a position",
             "No provider can buy a slot in our table, a badge, a score or a place at the top. "
             "Where a provider offers commercial terms attached to editorial outcomes, we decline."),
            ("check", "Every factual claim is dated and sourced",
             "Server counts, audit names and prices all carry the date we last verified them. "
             "Where a provider does not publish something, we write 'not published' instead of "
             "estimating."),
            ("check", "We disclose what we received",
             "If a provider gives us a free subscription to test, that is compensation and it is "
             "disclosed on the review."),
            ("check", "We correct publicly",
             "Errors are fixed in place and dated. We do not quietly delete a claim we got wrong."),
        ],
        "disc_title": "Affiliate disclosure",
        "disc_body": [
            "Many links on this site are affiliate links. When you click one and buy, the "
            "provider may pay us a commission. In some cases it costs you nothing extra; in a "
            "small number of cases a provider offers a discount code that is only available "
            "through affiliates, in which case using our link may give you a better price.",
            "Commissions vary by provider, plan and term, and they change. We do not control "
            "which providers we cover or in what order they appear. That decision is made on "
            "the criteria published on our methodology page, and the weights there are fixed.",
            "Under Swedish and EU rules, every affiliate link is labelled 'Ad' or 'Annons' next "
            "to the link itself, and every page containing affiliate links carries a disclosure "
            "bar at the top. If you find a commercial link that is not labelled, please tell us "
            "and we will fix it.",
        ],
        "contact_title": "Contact and corrections",
        "contact_body": (
            "We read everything. If a price is wrong, a review is unfair, or a provider has "
            "changed something material, we want to hear about it. Include the page URL and, "
            "where relevant, a screenshot."
        ),
        "responsible_title": "Editorial responsibility",
    },
    "sv": {
        "eyebrow": "Om oss",
        "h1": "Vilka driver den här webbplatsen, och varför",
        "lede": (
            "Vi är en oberoende redaktionell jämförelsetjänst som publicerar på engelska och "
            "svenska. Vi är inte knutna till någon VPN-leverantör vi recenserar. Vi betalas av "
            "vissa av dem. Båda meningarna är sanna samtidigt och du ska hålla oss till båda."
        ),
        "what_title": "Vad den här webbplatsen är",
        "what_body": [
            "Vi testar, undersöker och jämför kommersiella VPN-tjänster. Vi tjänar pengar när du "
            "köper en via våra länkar. Det är hela affärsmodellen — ingen prenumeration, ingen "
            "premiumnivå och ingenting till salu.",
            "Vi publicerar på engelska och svenska eftersom samma konsumentfrågor förtjänar "
            "samma svar på båda språken, och eftersom de flesta av de största jämförelsesajterna "
            "publicerar enbart på engelska.",
        ],
        "ed_title": "Våra redaktionella regler",
        "ed_body": [
            ("check", "Vi tar inte betalt för en recension eller en placering",
             "Ingen leverantör kan köpa en plats i vår tabell, ett märke, ett betyg eller en "
             "plats i toppen. Där en leverantör erbjuder kommersiella villkor kopplade till "
             "redaktionella utfall avböjer vi."),
            ("check", "Varje faktapåstående är daterat och källt",
             "Serverantal, revisionsnamn och priser bär alla datum för senaste verifiering. Där "
             "en leverantör inte publicerar något skriver vi 'inte publicerat' i stället för att "
             "uppskatta."),
            ("check", "Vi redovisar vad vi mottagit",
             "Om en leverantör ger oss en gratisprenumeration att testa är det ersättning och det "
             "redovisas på recensionen."),
            ("check", "Vi korrigerar offentligt",
             "Fel rättas på plats och dateras. Vi raderar inte tyst ett påstående vi gjort fel."),
        ],
        "disc_title": "Annonsinformation",
        "disc_body": [
            "Många länkar på den här webbplatsen är annonslänkar. När du klickar en sådan och "
            "köper kan leverantören betala oss en provision. I vissa fall kostar det dig inget "
            "extra; i ett litet antal fall erbjuder en leverantör en rabattkod som bara finns "
            "via affiliates, och då kan vår länk ge dig ett bättre pris.",
            "Provisionerna varierar per leverantör, plan och avtalslängd, och de ändras. Vi "
            "kontrollerar inte vilka leverantörer som täcks eller i vilken ordning de visas. "
            "Det beslutet fattas utifrån kriterierna på vår metodsida, och vikterna där är fasta.",
            "Enligt svenska och EU-regler märks varje annonslänk med 'Ad' eller 'Annons' intill "
            "själva länken, och varje sida som innehåller annonslänkar har en upplysningstabell "
            "överst. Om du hittar en kommersiell länk som inte är märkt, säg till oss så rättar "
            "vi det.",
        ],
        "contact_title": "Kontakt och korrigeringar",
        "contact_body": (
            "Vi läser allt. Om ett pris är fel, en recension är orättvis eller en leverantör har "
            "ändrat något väsentligt vill vi veta det. Ange sidans URL och, där det är relevant, "
            "en skärmbild."
        ),
        "responsible_title": "Redaktionellt ansvar",
    },
}

# ---------------------------------------------------------------------------
# General FAQ (shared)
# ---------------------------------------------------------------------------


FAQ_GENERAL = {
    "en": [
        ("Do VPN providers pay to be ranked higher?",
         "No. Commission rates have no weight in any of our five scoring components, and nobody "
         "here can accept payment in exchange for a rank, a badge or a score. The weights are "
         "published in full on our methodology page and never change to suit a provider."),
        ("Do you actually test the VPNs you review?",
         "Partly, and we are precise about which parts. We research the provider's own "
         "documentation, audit reports and terms, and we assess network architecture directly. "
         "We have not run our own throughput benchmarks, so we do not publish invented speed "
         "numbers — our speed score is a disclosed architectural estimate instead."),
        ("Why is one VPN rated 9 and another 7 if both say they keep no logs?",
         "Because a privacy policy is the weakest form of evidence. We grade what is verifiable: "
         "the named auditor and the date of their report, whether servers are RAM-only, which "
         "country the provider is registered in, and whether they have ever been legally "
         "compelled to produce data and failed."),
        ("What does \"RAM-only servers\" actually mean?",
         "The servers boot from a read-only image and never write to a disk. Everything in "
         "memory is wiped on every restart, including one caused by a physical seizure. It means "
         "logs cannot be retained even if the provider wanted to retain them, which is a stronger "
         "guarantee than a policy asking you to trust them."),
        ("Is a VPN illegal in Sweden?",
         "No. Using a VPN is entirely legal in Sweden, and using one to access content you have "
         "the right to access is not an offence. What is illegal is using one to infringe someone "
         "else's copyright, which is exactly as true without a VPN."),
        ("Will a VPN slow my connection down?",
         "Some, though far less than most people expect. With WireGuard on a modern protocol you "
         "will typically lose single-digit percentages of throughput on a fast Swedish broadband "
         "line. The overhead is much smaller on long routes than in the widely repeated claims "
         "that a VPN always cuts speed by half."),
        ("What is the difference between a no-logs policy and an audited no-logs policy?",
         "A no-logs policy is a promise in a document. An audited no-logs policy is a promise "
         "that a named independent firm inspected and confirmed, on a date we list. The second "
         "is worth more, though it only tells you the systems were configured correctly on the "
         "day of the inspection."),
        ("Do you sell my data?",
         "No. We do not run advertising, we are not in the business of selling or renting "
         "personal data, and we do not fingerprint your device. Our own privacy policy covers "
         "what the site itself collects, which is deliberately close to nothing."),
        ("How do you make money?",
         "Affiliate commissions, when you choose to buy through one of our links. The prices you "
         "pay are set by the provider. Some providers offer affiliate-only discount codes, in "
         "which case our link may give you a lower price rather than costing you more."),
        ("Do I need a VPN at all?",
         "Honestly, for most people on Swedish home broadband, probably not for privacy against "
         "your own internet provider — Swedish operators are under the same EU legal framework "
         "as everyone else in Europe. A VPN earns its place when you travel on untrusted "
         "networks, when you need to reach a service from another region, or when you want to "
         "stop your ISP seeing what you access."),
        ("Do free VPNs collect my data?",
         "Often, yes — free tiers subsidised by data collection are the norm, and even paid "
         "providers with free tiers may have weaker logging practices on those free accounts. "
         "Two of the eleven providers we list have a free tier we consider genuinely usable."),
        ("How often do you update the site?",
         "Prices are verified on a fixed cycle and each figure carries its own verification "
         "date. Provider facts — server counts, audit history, ownership — are re-checked "
         "whenever we learn something has changed. Nothing on this site is evergreen without a "
         "date on it."),
    ],
    "sv": [
        ("Betalar VPN-leverantörer för att rankas högre?",
         "Nej. Provisionssatser har ingen tyngd i någon av våra fem betygskomponenter, och ingen "
         "här kan ta emot betalning mot en placering, ett märke eller ett betyg. Vikterna "
         "publiceras i sin helhet på vår metodsida och ändras aldrig för att passa en leverantör."),
        ("Testar ni VPN:erna ni recenserar?",
         "Delvis, och vi är tydliga med vilka delar. Vi undersöker leverantörens egen dokumentation, "
         "revisionsrapporter och villkor, och vi bedömer nätverkets arkitektur direkt. Vi har inte "
         "kört våra egna genomströmningstester och publicerar därför inga påhittade "
         "hastighetssiffror — vårt hastighetsbetyg är en redaktionell arkitekturuppskattning i stället."),
        ("Varför får en VPN betyget 9 och en annan 7 om båda säger att de inte sparar loggar?",
         "För att en integritetspolicy är den svagaste formen av evidens. Vi betygsätter vad som "
         "går att verifiera: den namngivna revisorn och rapportens datum, om servrarna är "
         "RAM-baserade, vilket land leverantören är registrerad i och om de någonsin rättsligt "
         "tvingats lämna ut data och misslyckats."),
        ("Vad betyder egentligen \"RAM-servrar\"?",
         "Servrarna startar från en skrivskyddad bild och skriver aldrig till disk. Allt i "
         "minnet raderas vid varje omstart, även en som orsakas av en fysisk beslagtagning. Det "
         "innebär att loggar inte kan behållas även om leverantören ville behålla dem, vilket är "
         "ett starkare löfte än en policy som ber dig lita på dem."),
        ("Är VPN olagligt i Sverige?",
         "Nej. Att använda en VPN är helt lagligt i Sverige, och att använda en för att komma åt "
         "innehåll du har rätt att komma åt är inte brott. Det som är olagligt är att använda en "
         "för att kränka någon annans upphovsrätt, vilket är lika sant utan VPN."),
        ("Kommer en VPN att sakta ner min anslutning?",
         "Något, men mycket mindre än de flesta tror. Med WireGuard på ett modernt protokoll "
         "förlorar du typiskt enställiga procent i genomströmning på en snabb svensk bredbandslinje. "
         "Overheaden är mycket mindre på långa avstånd än i de ofta återciterade påståendena att en "
         "VPN alltid halverar hastigheten."),
        ("Vad är skillnaden mellan en loggfri policy och en granskad loggfri policy?",
         "En loggfri policy är ett löfte i ett dokument. En granskad loggfri policy är ett löfte "
         "som en namngiven oberoende firma inspekterade och bekräftade, på ett datum vi anger. Det "
         "andra är värdefullare, även om det bara säger att systemen var korrekt konfigurerade "
         "inspektionsdagen."),
        ("Säljer ni min data?",
         "Nej. Vi kör ingen reklam, vi säljer eller hyr inte ut personuppgifter och vi gör ingen "
         "enhetsfingeravtryckning. Vår egen integritetspolicy täcker vad webbplatsen själv "
         "samlar in, vilket medvetet är mycket lite."),
        ("Hur tjänar ni pengar?",
         "Affiliateprovisioner, när du väljer att köpa via en av våra länkar. Priserna du betalar "
         "sätts av leverantören. Vissa leverantörer erbjuder rabattkoder som bara finns för "
         "affiliates, och då kan vår länk ge dig ett lägre pris i stället för att kosta mer."),
        ("Behöver jag en VPN alls?",
         "Ärligt talat, för de flesta på svensk hembredband, förmodligen inte för integritet mot "
         "din egen internetleverantör — svenska operatörer omfattas av samma EU-rättsliga ram "
         "som alla andra i Europa. En VPN tjänar sitt fall när du reser på opålitliga nätverk, "
         "när du behöver nå en tjänst från en annan region, eller när du vill att din ISP inte "
         "ska se vad du besöker."),
        ("Samlar gratis-VPN:er in min data?",
         "Ofta, ja — gratisnivåer som finansieras av datainsamling är normen, och även betalda "
         "leverantörer med gratisnivå kan ha svagare loggpolicies på de kontona. Två av de elva "
         "leverantörer vi listar har en gratisnivå som vi anser genuint användbar."),
        ("Hur ofta uppdaterar ni webbplatsen?",
         "Priser verifieras i en fast cykel och varje siffra bär sitt eget verifieringsdatum. "
         "Leverantörsfakta — serverantal, revisionshistorik, ägande — kontrolleras om när vi får "
         "veta att något ändrats. Inget på den här webbplatsen är permanent utan datum."),
    ],
}


COMPARE_FAQ = {
    "en": [
        ("Which VPN is the cheapest?",
         "On the longest term we list, Private Internet Access at $59 for three years, "
         "followed by Windscribe at $54 for two. Monthly prices are a different "
         "picture entirely and are always far higher — that gap is the main thing to look at "
         "before you commit."),
        ("Which VPN has the best privacy?",
         "Proton VPN scores highest on our privacy component because open-source clients, Swiss "
         "jurisdiction and five consecutive Securitum audits are all independently verifiable. "
         "NordVPN scores highest overall because its RAM-only fleet enforces the no-logs claim in "
         "hardware rather than policy. Private Internet Access is the only one with two "
         "documented US federal subpoenas answered with 'we had nothing'."),
        ("Which VPN is best for streaming?",
         "ExpressVPN has the highest streaming score of the eleven, at 9.4. CyberGhost has the "
         "friendliest setup for beginners because every server is named after the service it is "
         "for. Mullvad and IVPN score low here and do not attempt it, which we treat as a "
         "legitimate choice rather than a fault."),
        ("Is it worth paying for the longer term?",
         "The discount is real — a 2-year or 3-year term can cost less per month than a single "
         "month does. The risk is renewal, because the promotional price does not persist. Check "
         "the renewal rate, and note the date you would need to cancel by."),
        ("What does a limited device count mean in practice?",
         "It is the number of devices that can be connected at the same time, not the number of "
         "devices you may have installed. A household with four people and two phones and a "
         "laptop each reaches ten easily. NordVPN's limit of 10 is comfortable; CyberGhost's 7 "
         "and IVPN's 2 are tight."),
    ],
    "sv": [
        ("Vilken VPN är billigast?",
         "På den längsta avtalslängd vi listar, Private Internet Access för cirka 590 kr i tre år, "
         "följt av Windscribe för cirka 550 kr i två år. Månadspriser är en helt annan bild och är "
         "alltid mycket högre — den luckan är det viktigaste att titta på innan du binder dig."),
        ("Vilken VPN har bäst integritet?",
         "Proton VPN får högst poäng på vår integritetskomponent eftersom källkodsöppna klienter, "
         "schweizisk jurisdiktion och fem Securitum-revisioner i rad alla går att verifiera "
         "oberoende. NordVPN får högst totalt eftersom dess RAM-flottor upprätthåller "
         "loggfrihetspåståendet i hårdvara snarare än i policy. Private Internet Access är det "
         "enda med två dokumenterade amerikanska federala kallelser som besvarades med 'vi hade "
         "ingenting'."),
        ("Vilken VPN är bäst för streaming?",
         "ExpressVPN har det högsta streamingbetyget av de elva, 9,4. CyberGhost har den "
         "vänligaste installationen för nybörjare eftersom varje server är namngiven efter den "
         "tjänst den är till för. Mullvad och IVPN får låga poäng här och försöker inte, vilket vi "
         "ser som ett legitimt val snarare än ett fel."),
        ("Lönar det sig att betala för längre avtalslängd?",
         "Rabatten är verklig — ett 2- eller 3-årsavtal kan kosta mindre per månad än vad en "
         "enskild månad gör. Risken är förnyelsen, eftersom kampanjpriset inte består. Kontrollera "
         "förnyelsepriset och notera vilket datum du måste avsluta senast."),
        ("Vad betyder en begränsad enhetsgräns i praktiken?",
         "Det är antalet enheter som kan vara anslutna samtidigt, inte antalet enheter du får "
         "installera. Ett hushåll med fyra personer och två telefoner och en dator vardera når "
         "tio lätt. NordVPNs gräns på 10 är bekväm; CyberGhosts 7 och IVPN:s 2 är tighta."),
    ],
}

# ---------------------------------------------------------------------------
# Legal pages
# ---------------------------------------------------------------------------


LEGAL = {
    "privacy": {
        "en": {
            "eyebrow": "Legal",
            "h1": "Privacy policy",
            "lede": "What this site collects, what it does not, and what changes when you click an affiliate link.",
            "updated": "Last updated",
            "sections": [
                ("Who is responsible", [
                    "<p>This site is operated by a Swedish independent editorial comparison service. "
                    "The advertiser and publisher responsible for the content on these pages is identified "
                    "in the footer of every page, including legal name, organisation number, postal "
                    "address and email address.</p>",
                ]),
                ("What we collect ourselves", [
                    "<p>We collect almost nothing ourselves. Specifically, we do not sell or rent personal "
                    "data, and we do not perform device fingerprinting or cross-site tracking. "
                    "Advertising on these pages is served by Google AdSense, which processes data under "
                    "Google's own policy — see the cookie policy for what that means and how to control it.</p>",
                    "<p>The site sets no analytics or advertising cookies unless you explicitly accept "
                    "them in the consent banner. If you decline, one strictly necessary cookie is set to "
                    "remember that choice so you are not asked again on your next visit.</p>",
                    "<p>Our hosting provider processes IP addresses in order to serve pages and to "
                    "protect against abuse. Their processing is governed by our agreement with them and "
                    "by applicable data protection law.</p>",
                ]),
                ("Server logs", [
                    "<p>Like any web server, our host records technical connection data such as IP "
                    "address, timestamp, requested URL, browser identification and referrer, in order to "
                    "deliver the site, diagnose faults and defend against attacks. These logs are not "
                    "combined with any other data and are not used to build a profile of you.</p>",
                ]),
                ("Affiliate links", [
                    "<p>This is the part that matters most on a site like this. When you click an "
                    "affiliate link, you leave this site and go to a third party. From that moment the "
                    "third party's own privacy policy applies, and we have no control over or access to "
                    "what they collect.</p>",
                    "<p>Many VPN providers place a cookie or similar technology when you arrive through "
                    "an affiliate link, so that if you later subscribe we are credited with the referral. "
                    "That tracking is set by the provider, not by us. Depending on your choices and their "
                    "policy, a provider may also see that you arrived from us and which link you used.</p>",
                    "<p>We do not receive your payment details, your email address or anything you enter "
                    "on a provider's site. Providers may email you about their own products. You can "
                    "unsubscribe from those emails through the provider, not through us.</p>",
                ]),
                ("Your rights under GDPR", [
                    "<p>If you are in the European Economic Area, you have the right to access, correct, "
                    "erase, restrict or object to processing of your personal data, to data portability, "
                    "and to lodge a complaint with a supervisory authority — the Swedish Authority for "
                    "Privacy Protection (IMY) in our case.</p>",
                    "<p>Because we collect so little, in practice there is usually nothing to request. "
                    "Where a request concerns data held by a VPN provider you subscribed to, they are the "
                    "controller and must handle it — we cannot act on their behalf.</p>",
                ]),
                ("Children", [
                    "<p>This site is not directed at children and we do not knowingly collect personal "
                    "data from anyone under 16.</p>",
                ]),
                ("Changes to this policy", [
                    "<p>If this policy changes materially we will update the date at the top of this page "
                    "and describe what changed.</p>",
                ]),
            ],
        },
        "sv": {
            "eyebrow": "Juridik",
            "h1": "Integritetspolicy",
            "lede": "Vad den här webbplatsen samlar in, vad den inte gör, och vad som ändras när du klickar en annonslänk.",
            "updated": "Senast uppdaterad",
            "sections": [
                ("Vem är ansvarig", [
                    "<p>Den här webbplatsen drivs av en svensk oberoende redaktionell jämförelsetjänst. "
                    "Den annonsör och utgivare som ansvarar för innehållet på de här sidorna anges i "
                    "sidfoten på varje sida, med juridiskt namn, organisationsnummer, postadress och "
                    "e-postadress.</p>",
                ]),
                ("Vad vi samlar in själva", [
                    "<p>Vi samlar in nästan ingenting själva. Specifikt säljer eller hyr vi inte ut "
                    "personuppgifter, och vi utför ingen enhetsfingeravtryckning eller spårning mellan "
                    "webbplatser. Annonseringen på de här sidorna levereras av Google AdSense, som behandlar "
                    "data under Googles egen policy — se kookiepolicyn för vad det innebär och hur du styr det.</p>",
                    "<p>Webbplatsen sätter inga analys- eller annonskakor om du inte uttryckligen godkänner "
                    "dem i samtyckesrutan. Om du avböjer sätts en strikt nödvändig kaka för att komma ihåg "
                    "ditt val, så att vi inte frågar igen vid nästa besök.</p>",
                    "<p>Vår hostingleverantör behandlar IP-adresser för att leverera sidor och för att "
                    "skydda mot övergrepp. Deras behandling regleras av vårt avtal med dem och av "
                    "tillämplig dataskyddslagstiftning.</p>",
                ]),
                ("Serverloggar", [
                    "<p>Som alla webbservrar registrerar vår värd teknisk anslutningsdata såsom "
                    "IP-adress, tidpunkt, begärd URL, webbläsaridentifiering och referrer, för att "
                    "leverera webbplatsen, felsöka och försvara mot attacker. Dessa loggar kombineras "
                    "inte med annan data och används inte för att bygga en profil av dig.</p>",
                ]),
                ("Annonslänkar", [
                    "<p>Det här är den viktigaste delen på en webbplats som denna. När du klickar en "
                    "annonslänk lämnar du den här webbplatsen och går till en tredje part. Från det "
                    "ögonblicket gäller tredje partens egen integritetspolicy, och vi har varken kontroll "
                    "över eller tillgång till vad de samlar in.</p>",
                    "<p>Många VPN-leverantörer sätter en kaka eller liknande teknik när du kommer via en "
                    "annonslänk, så att vi kan tillgodoräkna oss hänvisningen om du senare prenumererar. "
                    "Den spårningen sätts av leverantören, inte av oss. Beroende på dina val och deras "
                    "policy kan en leverantör också se att du kom från oss och vilken länk du använde.</p>",
                    "<p>Vi får inte dina betalningsuppgifter, din e-postadress eller något du anger på "
                    "en leverantörs webbplats. Leverantörer kan mejla dig om sina egna produkter. Du "
                    "avslutar sådana mejl hos leverantören, inte hos oss.</p>",
                ]),
                ("Dina rättigheter enligt GDPR", [
                    "<p>Om du befinner dig inom Europeiska ekonomiska området har du rätt till tillgång, "
                    "rättelse, radering, begränsning eller att invända mot behandling av dina "
                    "personuppgifter, till dataportabilitet och att lämna in en klagomål till en "
                    "tillsynsmyndighet — i vårt fall Integritetsskyddsmyndigheten (IMY).</p>",
                    "<p>Eftersom vi samlar in så lite finns det i praktiken sällan något att begära ut. "
                    "När en begäran rör data som hålls av en VPN-leverantör du prenumererat på är de "
                    "personuppgiftsansvariga och måste hantera den — vi kan inte agera för deras räkning.</p>",
                ]),
                ("Barn", [
                    "<p>Den här webbplatsen är inte riktad till barn och vi samlar inte medvetet in "
                    "personuppgifter från någon under 16 år.</p>",
                ]),
                ("Ändringar av policyn", [
                    "<p>Om policyn ändras väsentligen uppdaterar vi datumet överst på sidan och "
                    "beskriver vad som ändrats.</p>",
                ]),
            ],
        },
    },

    "cookies": {
        "en": {
            "eyebrow": "Legal",
            "h1": "Cookie policy",
            "lede": "Our own list is short: one preference cookie, optional analytics, and local storage. Advertising is served by Google AdSense under Google's own policy, described in its own section below.",
            "updated": "Last updated",
            "sections": [
                ("What we actually set", [
                    "<p>By default this site sets one cookie, and only if you interact with the consent "
                    "banner: a first-party preference cookie that records your choice so the banner does "
                    "not reappear. It contains no identifier, is not readable by any other site, and "
                    "expires after twelve months.</p>",
                    "<p>Analytics is Google Analytics, gated by the consent banner: until you accept it runs consent-denied and sets no cookies; after accept it may set its usual measurement cookies (_ga and similar). Advertising cookies come from Google AdSense, described below — not from us.</p>",
                ]),
                ("What we never set", [
                    "<ul><li>No advertising cookies set by us — Google's are described below.</li>"
                    "<li>No third-party tracking pixels, beacons or social pixels of our own.</li>"
                    "<li>No cross-site or cross-domain tracking cookies of our own.</li>"
                    "<li>No device or browser fingerprinting.</li>"
                    "<li>No data sold, rented or shared by us with advertising networks.</li></ul>",
                ]),
                ("Advertising (Google AdSense)", [
                    "<p>Pages on this site load Google AdSense, which serves the display advertising that funds the free comparison. Google acts as an independent controller for the data it processes for that purpose — we do not control, access or receive it.</p>",
                    "<p>Google may use cookies and similar technologies to serve and measure ads, including personalised advertising where you have consented. Without consent, Google serves non-personalised ads. Read how Google uses data from partner sites, manage ad personalisation in Google Ad Settings, and read its advertising principles: <a href=\"https://policies.google.com/technologies/partner-sites\">how Google uses partner-site data</a> · <a href=\"https://adssettings.google.com\">Google Ad Settings</a> · <a href=\"https://policies.google.com/technologies/ads\">Google's advertising principles</a>.</p>",
                    "<p>Blocking Google's advertising cookies does not break this site: the comparison, prices and reviews work the same with or without them.</p>",
                ]),
                ("Local storage", [
                    "<p>We use your browser's local storage for one purpose: remembering whether you chose "
                    "a light or dark theme, and which order you last sorted the comparison table in. "
                    "This never leaves your device and is not transmitted to us.</p>",
                ]),
                ("Cookies set by providers, not by us", [
                    "<p>When you click an affiliate link and arrive at a VPN provider's site, that "
                    "provider may set its own cookies, including an affiliate tracking cookie that "
                    "credits the referral if you subscribe. Those cookies are governed by the "
                    "provider's privacy policy and its consent regime, not by this one. We have no "
                    "access to them and no control over them.</p>",
                ]),
                ("How to control cookies", [
                    "<p>You can block or delete cookies in your browser settings at any time. Blocking "
                    "strictly necessary cookies may mean your theme choice and consent answer are not "
                    "remembered between visits. Most browsers also offer a built-in tracking "
                    "protection mode.</p>",
                ]),
            ],
        },
        "sv": {
            "eyebrow": "Juridik",
            "h1": "Kookiepolicy",
            "lede": "Vår egen lista är kort: en preferenskaka, valfri analys och lokal lagring. Annonsering levereras av Google AdSense under Googles egen policy, beskriven i ett eget avsnitt nedan.",
            "updated": "Senast uppdaterad",
            "sections": [
                ("Vad vi faktiskt sätter", [
                    "<p>Som standard sätter den här webbplatsen en enda kaka, och bara om du interagerar "
                    "med samtyckesrutan: en förstagångskaka som registrerar ditt val så att rutan inte "
                    "visas igen. Den innehåller ingen identifierare, går inte att läsa av någon annan "
                    "webbplats och upphör efter tolv månader.</p>",
                    "<p>Analys är Google Analytics, styrd av samtyckesrutan: tills du godkänner körs den samtyckesnekad och sätter inga kakor; efter godkännande kan den sätta sina vanliga mätkakor (_ga och liknande). Annonskakor kommer från Google AdSense, beskrivet nedan — inte från oss.</p>",
                ]),
                ("Vad vi aldrig sätter", [
                    "<ul><li>Inga annonskakor satta av oss — Googles beskrivs nedan.</li>"
                    "<li>Inga egna spårningspixlar, beacons eller sociala pixlar från tredje part.</li>"
                    "<li>Inga egna kakor för spårning mellan webbplatser eller domäner.</li>"
                    "<li>Ingen enhets- eller webbläsarfingeravtryckning.</li>"
                    "<li>Inga data som säljs, hyrs ut eller delas av oss med annonsnätverk.</li></ul>",
                ]),
                ("Annonsering (Google AdSense)", [
                    "<p>Sidorna på den här webbplatsen laddar Google AdSense, som levererar den displayannonsering som finansierar den fria jämförelsen. Google agerar som självständig personuppgiftsansvarig för de data de behandlar för det ändamålet — vi kontrollerar, kommer åt eller tar emot dem inte.</p>",
                    "<p>Google kan använda kakor och liknande teknik för att leverera och mäta annonser, inklusive personaliserad annonsering där du har samtyckt. Utan samtycke levererar Google icke-personaliserade annonser. Läs hur Google använder data från partnersajter, hantera personalisering i Googles annonsinställningar och läs deras annonsprinciper: <a href=\"https://policies.google.com/technologies/partner-sites\">så använder Google partnersajters data</a> · <a href=\"https://adssettings.google.com\">Googles annonsinställningar</a> · <a href=\"https://policies.google.com/technologies/ads\">Googles annonsprinciper</a>.</p>",
                    "<p>Att blockera Googles annonskakor förstör inte den här webbplatsen: jämförelsen, priserna och recensionerna fungerar likadant med eller utan dem.</p>",
                ]),
                ("Lokal lagring", [
                    "<p>Vi använder webbläsarens lokala lagring för ett enda ändamål: att komma ihåg om du "
                    "valde ljust eller mörkt tema, och i vilken ordning du sist sorterade "
                    "jämförelsetabellen. Det lämnar aldrig din enhet och skickas inte till oss.</p>",
                ]),
                ("Kakor som sätts av leverantörer, inte av oss", [
                    "<p>När du klickar en annonslänk och kommer till en VPN-leverantörs webbplats kan "
                    "leverantören sina egna kakor, inklusive en spårningskaka för annonslänkar som "
                    "tillgodoräkna hänvisningen om du prenumererar. De kakorna regleras av "
                    "leverantörens integritetspolicy och dess samtyckeshantering, inte av den här. Vi "
                    "har varken tillgång till eller kontroll över dem.</p>",
                ]),
                ("Hur du kontrollerar kakor", [
                    "<p>Du kan blockera eller radera kakor i webbläsarens inställningar när som helst. "
                    "Om du blockerar strikt nödvändiga kakor kan det innebära att ditt temaval och ditt "
                    "samtalssvar inte sparas mellan besök. De flesta webbläsare erbjuder även ett "
                    "inbyggt spårningsskydd.</p>",
                ]),
            ],
        },
    },

    "terms": {
        "en": {
            "eyebrow": "Legal",
            "h1": "Terms of use",
            "lede": "The rules for using this site, and the limits of what it can promise you.",
            "updated": "Last updated",
            "sections": [
                ("Acceptance", [
                    "<p>By using this site you accept these terms. If you do not accept them, please do "
                    "not use the site.</p>",
                ]),
                ("What this site is", [
                    "<p>This site is an independent commercial comparison and editorial service. It "
                    "provides information about third-party services. We are not the provider of any VPN "
                    "service, we are not affiliated with the providers we describe unless we explicitly "
                    "state otherwise, and we are not a party to any contract you enter into with a "
                    "provider.</p>",
                    "<p>Information on this site is provided for general guidance. It is not legal, "
                    "financial or professional advice, and it is not a recommendation tailored to your "
                    "circumstances.</p>",
                ]),
                ("Commercial relationships", [
                    "<p>This site earns affiliate commissions when you purchase from a provider through "
                    "one of our links. Some providers are only reachable through affiliates, which means "
                    "using our link may give you a lower price. Our commercial relationships are disclosed "
                    "on every page containing affiliate links and in our about page. They do not affect "
                    "our editorial conclusions, and the scoring method behind every ranking on this site "
                    "is published in full.</p>",
                ]),
                ("Prices and accuracy", [
                    "<p>Prices, plans, features, server counts and terms change frequently and are "
                    "controlled entirely by each provider. We verify them on a schedule and display the "
                    "date of last verification, but we cannot guarantee that any figure is current. The "
                    "provider's own website and checkout are always the authoritative source. If a price "
                    "shown here is wrong, you will not be charged the wrong amount.</p>",
                    "<p>Scores on this site are editorial judgements built from publicly available "
                    "information. They are not laboratory measurements and are not a guarantee of any "
                    "outcome.</p>",
                ]),
                ("Acceptable use", [
                    "<p>You may read, print and share this content for personal, non-commercial use. You "
                    "may not republish substantial portions of it commercially, scrape it at a rate that "
                    "degrades the service, or use it in a way that implies our endorsement of a product "
                    "we have not endorsed.</p>",
                ]),
                ("Intellectual property", [
                    "<p>The text, layout, design and original graphics on this site belong to us. Provider "
                    "names and trademarks belong to their respective owners and are used here "
                    "nominatively to identify the services being compared. We do not claim any ownership "
                    "of provider logos or brand assets.</p>",
                ]),
                ("Limitation of liability", [
                    "<p>To the extent permitted by law, we are not liable for any loss arising from "
                    "your use of this site or of any third-party service we describe. This includes "
                    "reliance on any figure, score or statement published here. Nothing in these terms "
                    "limits liability for injury caused by gross negligence, or liability that cannot "
                    "be limited under applicable law, including consumer protection law.</p>",
                ]),
                ("Governing law and consumer rights", [
                    "<p>These terms are governed by Swedish law. If you are a consumer, you retain the "
                    "protection of mandatory consumer protection provisions in your country of residence, "
                    "and nothing here removes rights you have under Swedish or EU law. Disputes that "
                    "cannot be resolved by negotiation are handled by the Swedish Consumer Disputes "
                    "Board (Konsumenttvisterkostnadsnämnden) where you are resident in Sweden.</p>",
                ]),
                ("Changes", [
                    "<p>We may update these terms. The date at the top of this page reflects the current "
                    "version, and material changes will be described on the page.</p>",
                ]),
            ],
        },
        "sv": {
            "eyebrow": "Juristik",
            "h1": "Användarvillkor",
            "lede": "Reglerna för att använda den här webbplatsen, och gränserna för vad den kan lova dig.",
            "updated": "Senast uppdaterad",
            "sections": [
                ("Godkännande", [
                    "<p>Genom att använda den här webbplatsen godkänner du dessa villkor. Om du inte "
                    "godkänner dem, använd inte webbplatsen.</p>",
                ]),
                ("Vad den här webbplatsen är", [
                    "<p>Den här webbplatsen är en oberoende kommersiell jämförelse- och "
                    "redaktionstjänst. Den ger information om tredjepartstjänster. Vi är inte "
                    "leverantör av någon VPN-tjänst, vi är inte knutna till de leverantörer vi beskriver "
                    "om vi inte uttryckligen anger det, och vi är inte part i något avtal du ingår med "
                    "en leverantör.</p>",
                    "<p>Informationen på den här webbplatsen ges som allmän vägledning. Den är inte "
                    "juridisk, ekonomisk eller professionell rådgivning och är inte en rekommendation "
                    "anpassad till dina förutsättningar.</p>",
                ]),
                ("Kommersiella relationer", [
                    "<p>Den här webbplatsen tjänar affiliateprovisioner när du köper från en leverantör "
                    "via någon av våra länkar. Vissa leverantörer är endast nåbara via affiliates, vilket "
                    "innebär att vår länk kan ge dig ett lägre pris. Våra kommersiella relationer "
                    "redovisas på varje sida som innehåller annonslänkar och på v sida om oss. De "
                    "påverkar inte våra redaktionella slutsatser, och metoden bakom varje rankning på "
                    "den här webbplatsen publiceras i sin helhet.</p>",
                ]),
                ("Priser och riktighet", [
                    "<p>Priser, planer, funktioner, serverantal och villkor ändras ofta och styrs "
                    "helt av respektive leverantör. Vi verifierar dem enligt schema och visar datum för "
                    "senaste verifiering, men vi kan inte garantera att någon siffra är aktuell. "
                    "Leverantörens egen webbplats och kassa är alltid den auktoritativa källan. Om ett "
                    "pris som visas här är fel blir du inte debiterat fel.</p>",
                    "<p>Betygen på den här webbplatsen är redaktionella bedömningar byggda på "
                    "offentligt tillgänglig information. De är inte laboratoriemätningar och är ingen "
                    "garanti för något utfall.</p>",
                ]),
                ("Tillåten användning", [
                    "<p>Du får läsa, skriva ut och dela innehållet för personligt, icke-kommersiellt "
                    "bruk. Du får inte återpublicera betydande delar av det kommersiellt, inte hämta "
                    "det i en takt som försämrar tjänsten och inte använda det på ett sätt som antyder "
                    "vårt stöd för en produkt vi inte stöder.</p>",
                ]),
                ("Immateriella rättigheter", [
                    "<p>Texten, layouten, designen och den originella grafiken på den här webbplatsen "
                    "tillhör oss. Leverantörers namn och varumärken tillhör respektive ägare och används "
                    "här nominativt för att identifiera de tjänster som jämförs. Vi gör inga påståenden "
                    "om ägande av leverantörers logotyper eller varumärkesskapital.</p>",
                ]),
                ("Begränsning av ansvar", [
                    "<p>Så lång lagen tillåter ansvarar vi inte för någon förlust som uppkommer genom "
                    "din användning av den här webbplatsen eller av någon tredjepartstjänst vi "
                    "beskriver. Detta omfattar även förtroende på någon siffra, betyg eller påstående som "
                    "publiceras här. Inget i dessa villkor begränsar ansvar för skada orsakad av grov "
                    "vårdslöshet, eller ansvar som inte får begränsas enligt tillämplig lag, inklusive "
                    "konsumentskyddslagstiftning.</p>",
                ]),
                ("Tillämplig lag och konsumenträttigheter", [
                    "<p>Dessa villkor regleras av svensk rätt. Om du är konsument behåller du skyddet av "
                    "tvingande konsumentskyddsbestämmelser i ditt bosättningsland, och ingenting här "
                    "tar bort rättigheter du har enligt svensk eller EU-rätt. Tvister som inte kan "
                    "lösas genom förhandling hanteras av Konsumenttvisterkostnadsnämnden om du är "
                    "bosatt i Sverige.</p>",
                ]),
                ("Ändringar", [
                    "<p>Vi kan uppdatera dessa villkor. Datumet överst på sidan visar den aktuella "
                    "versionen, och väsentliga ändringar beskrivs på sidan.</p>",
                ]),
            ],
        },
    },
}


# ---------------------------------------------------------------------------
# Best VPN for … money pages: en|sv/best-vpn-for/<slug>/
#
# Per topic: label (inline topic word), h1, desc (meta description), lede,
# intro/why/guide (paragraph lists), guide_title, picks (curated top 3, keyed
# by provider id — ids must exist in providers.json), faq [(question, answer)].
# Criteria weights live in assets/data/topics.json; scores are never written
# here — they come from providers.json at build time.
# ---------------------------------------------------------------------------

BEST_VPN_FOR = {
    "en": {
        "hub": {
            "eyebrow": "Guides by task",
            "h1": "Best VPN for the job you actually have",
            "desc": ("Twelve VPN guides, one per task: streaming, Netflix, gaming, torrenting, "
                     "privacy, travel, phones, desktops and routers — each with a published "
                     "weighting and a top three we would buy."),
            "lede": ("Nobody needs the best VPN in the abstract. They need the best VPN for one job, "
                     "and the job changes the answer: the weights move, the scores do not."),
            "intro": [
                ("Each guide re-weights the same five components we always use — privacy, speed, "
                 "value, streaming and ease of use. A streaming guide leans on streaming and speed, "
                 "a privacy guide leans on privacy. The component scores themselves never move to "
                 "suit a page."),
                ("The top three on each guide are editorial picks chosen for that task, and they are "
                 "not always the top three of our overall ranking. Where a pick looks surprising the "
                 "reason is written under the card, so you can disagree with it on the evidence."),
            ],
            "faq": [
                ("Are these guides paid for?",
                 "The links are affiliate links, so we earn a commission if you subscribe through one. "
                 "Commission does not change a score, a pick or a weight — the tables and the method "
                 "run the same whether you click or not, and provider data is verified on a fixed cycle."),
                ("Why twelve guides instead of one list?",
                 "Because one list has to average over tasks that pull in opposite directions. Torrenting "
                 "cares about privacy and device limits, a television guide cares about consistency and "
                 "speed. Separate weights produce more useful answers than a single ranking can."),
                ("Do you benchmark speed yourselves?",
                 "No, and we publish no ping or throughput figures we cannot reproduce. Every speed number "
                 "on this site is a component of a published scoring model, not a measurement from our own "
                 "connection — which is why the method page matters more than any headline."),
            ],
        },

        "streaming": {
            "label": "streaming",
            "h1": "Best VPN for streaming",
            "desc": ("The best VPNs for streaming in 2026: ExpressVPN, NordVPN and Surfshark, chosen "
                     "on streaming ability, speed and value with weights we publish."),
            "lede": ("Streaming is where a VPN either disappears into the background or ruins the "
                     "evening. We re-weight the five components we always use toward the two that "
                     "decide it, then pick the three that hold up."),
            "intro": [
                ("A stream fails in two ways: it buffers, or the service refuses the connection "
                 "because it does not like where you appear to be from. Both are common, and both get "
                 "sold as the best VPN by sites that have never watched anything through one."),
                ("So this guide does not rank on streaming alone. Speed decides whether a high-bitrate "
                 "stream stays smooth, value decides whether it is worth renewing, and privacy still "
                 "counts because the same tunnel carries your banking and your inbox."),
            ],
            "why": [
                ("Streaming carries 40% of this decision and speed 30%; value takes 15%, privacy 10% and "
                 "ease of use 5%. The component scores come straight from our published model — nothing "
                 "is re-scored for a guide, only the weights change, and those weights are shown below."),
            ],
            "guide_title": "What a streaming VPN has to get right",
            "guide": [
                ("Consistency beats peaks. Any VPN can hold a connection for ten minutes on a good "
                 "evening; the question is whether the same server still works on Friday night, on the "
                 "TV app, while someone else in the house is on a video call."),
                ("Device limits matter more than people expect. A television, a console and a phone are "
                 "three simultaneous streams, and a plan for five devices is not the same as one for "
                 "unlimited — the comparison table below marks out which is which."),
            ],
            "picks": {
                "expressvpn": ("Highest streaming score here at 9.4 and our highest speed score at 9.6 — "
                               "the one to buy if the picture must not stall."),
                "nordvpn": ("9.2 for streaming inside the strongest overall score in the table, so nothing "
                            "else gives way when you turn the tunnel on."),
                "surfshark": ("9.0 for streaming with unlimited devices, which matters when the same "
                              "evening runs on a TV, a phone and a console at once."),
            },
            "faq": [
                ("Which VPN is best for streaming?",
                 "On this site, ExpressVPN: it has the highest streaming component at 9.4 and the highest "
                 "speed component at 9.6. NordVPN sits at 9.2 and costs less over a long term, while "
                 "Surfshark adds unlimited devices if the stream is on more than one screen."),
                ("Do I need a VPN to stream?",
                 "Not always. If your service is licensed where you are watching, you do not need one. It "
                 "matters when you travel, when a title is licensed elsewhere, or when your network treats "
                 "video badly — and it must never be the reason a live stream stutters."),
                ("Will a VPN make my stream buffer?",
                 "Encryption has a cost, but the gap between a fast provider and a slow one is larger than "
                 "the cost of the tunnel. That is exactly what the speed component measures, and it ranges "
                 "from 9.6 at the top of this table to 7.6 at the bottom."),
            ],
        },

        "netflix": {
            "label": "Netflix",
            "h1": "Best VPN for Netflix",
            "desc": ("Three VPNs our Netflix weighting puts on top in 2026 — ExpressVPN, NordVPN "
                     "and CyberGhost — chosen on our streaming, speed and ease-of-use scores."),
            "lede": ("Netflix is the test everyone runs first and the one most often faked. Here is "
                     "what actually decides whether a library on another continent opens."),
            "intro": [
                ("Catalogues are licensed per country, so a VPN is not so much unlocking Netflix as "
                 "presenting a different address and hoping the service accepts it. Some servers do, "
                 "some do not, and what worked last month is no guarantee about next month."),
                ("That is why one screenshot proves nothing. We lean on the streaming component, which "
                 "is built from repeated checks rather than a single lucky evening, and on the speed "
                 "component that keeps a 4K stream from quietly collapsing into something worse."),
            ],
            "why": [
                ("Streaming carries 45% here — the heaviest of any guide — with speed at 25%, value at 15% "
                 "and ease of use at 10%, because switching regions with a television remote is a "
                 "different job from clicking a mouse. Privacy takes the last 5%."),
            ],
            "guide_title": "How we judge a Netflix VPN",
            "guide": [
                ("A provider either presents an address the service accepts or it does not, and the "
                 "failure shows up as an error code rather than a slow picture. Consistency across "
                 "check dates is what the streaming component rewards, not one good evening."),
                ("The second half is bandwidth. Netflix adapts down silently, so a weak connection looks "
                 "like a worse picture instead of a failure. Speed is the guard against that, and it is "
                 "why a provider with a slightly lower streaming score can still be the better buy."),
            ],
            "picks": {
                "expressvpn": ("Streaming 9.4 and speed 9.6: the most reliable combination we publish, "
                               "at the highest price in this table."),
                "nordvpn": ("Streaming 9.2 with the best overall score of the eleven, and 111 countries to "
                            "pick an address from."),
                "cyberghost": ("Streaming 9.0, ease of use 9.4 and a 45-day money-back window — the longest "
                               "we list — if the catalogue disappoints."),
            },
            "faq": [
                ("Which VPN works with Netflix?",
                 "The three on this page, as far as our checks go: ExpressVPN, NordVPN and CyberGhost all "
                 "score 9.0 or better on streaming. Availability varies by country and by server, so treat "
                 "any guarantee you read elsewhere as marketing."),
                ("Why did my VPN stop working with Netflix?",
                 "Because the service recognises the address range your VPN server uses and blocks it. "
                 "Switching server location inside the app usually restores it; if it does not, the provider "
                 "has not caught up and another region is the pragmatic answer."),
                ("Is using a VPN with Netflix against the rules?",
                 "Streaming another region's catalogue through a VPN can conflict with the terms of service "
                 "of the service concerned. Read the terms that apply to you and decide for yourself — we "
                 "will not pretend there is a single answer for every country."),
            ],
        },

        "gaming": {
            "label": "gaming",
            "h1": "Best VPN for gaming",
            "desc": ("The best VPNs for gaming in 2026 — ExpressVPN, NordVPN and Surfshark — chosen on "
                     "speed, privacy and value, with no invented ping numbers."),
            "lede": ("Gamers ask for latency and we refuse to invent it. We cannot measure your route "
                     "to a game server, so this guide weights what we can publish honestly."),
            "intro": [
                ("The honest limit first: we do not measure ping, and we do not publish throughput "
                 "figures we cannot reproduce. A VPN that claims to lower your latency is making a "
                 "claim about your network that nobody can make from ours."),
                ("What we can weigh is the speed component — how little a tunnel costs in the model we "
                 "publish — plus privacy, because a game account with a payment method attached is "
                 "worth stealing, and value, because a subscription you keep beats one you churn."),
            ],
            "why": [
                ("Speed carries 45% for this guide, the highest share of any. Streaming gets 20%, privacy "
                 "15%, and ease of use and value 10% each. Those weights are shown below and are the only "
                 "thing that differs from our overall ranking."),
            ],
            "guide_title": "What to look for in a gaming VPN",
            "guide": [
                ("Stability matters more than a good number on one evening. A tunnel that holds through a "
                 "long session, on a server you can find again tomorrow, is worth more than a route that "
                 "was fast once and has since been moved."),
                ("Device limits decide the household. A router, a PC and a console can be three of the "
                 "simultaneous connections a plan allows, and unlimited plans remove the arithmetic "
                 "entirely — the table below shows each provider's limit."),
            ],
            "picks": {
                "expressvpn": ("Speed 9.6, the highest we publish, and the gaming use case is one of the "
                               "four this provider is marked as best for."),
                "nordvpn": ("Speed 9.4 inside the best overall score here, with 10 simultaneous devices "
                            "for the rest of the household."),
                "surfshark": ("Speed 8.8, unlimited devices and the lowest two-year total of these three at "
                              "59 USD — the sensible pick for a shared gaming PC."),
            },
            "faq": [
                ("Does a VPN reduce lag?",
                 "Not automatically. A VPN changes the route your traffic takes, which can help or hurt; "
                 "we do not publish ping numbers because we cannot reproduce yours. What we do publish is "
                 "how much throughput the tunnel costs in our speed component, and that is the honest part."),
                ("Will a VPN get me banned from a game?",
                 "Using a VPN is not against the rules of most games, but some restrict or block connections "
                 "that look like datacentre traffic, and a few punish accounts for it. Check the rules of "
                 "the game you play before you connect."),
                ("Which protocol should I use for gaming?",
                 "Every provider here offers a modern protocol — WireGuard, or a proprietary equivalent — "
                 "and that is the sensible default for latency and battery. OpenVPN remains the fallback "
                 "when a network blocks the newer one, and both are listed on every review page."),
            ],
            "spotlight": {
                "eyebrow": "For ping, not privacy",
                "title": "A different tool for one gaming problem: ping",
                "body": ("GearUP Booster is not a VPN and is not part of our ranking: it does not hide "
                         "your IP address or encrypt your traffic the way the providers above do. It does "
                         "one thing — route game traffic over shorter paths to cut ping, packet loss and "
                         "jitter on Windows, mobile and consoles — with a free trial so you can test it "
                         "on your own connection before paying."),
                "note": "Not a VPN, and not ranked here. A booster cannot fix slow broadband or a server on another continent.",
                "cta": "Try GearUP free",
                "affiliate_id": "gearup-booster",
            },
        },

        "torrenting": {
            "label": "torrenting",
            "h1": "Best VPN for torrenting",
            "desc": ("The best VPNs for torrenting in 2026 — Private Internet Access, Proton VPN and "
                     "Mullvad — chosen on privacy, price and the device limits that matter for P2P."),
            "lede": ("Torrenting is the one task where privacy is not a feature but the whole point, "
                     "and where a device limit or a missing port can end the download."),
            "intro": [
                ("A torrent client announces your address to every peer in the swarm. With a VPN the "
                 "swarm sees the VPN's address instead, which is the entire mechanism — and the reason "
                 "a provider's logging policy matters more here than anywhere else on this site."),
                ("The practical constraints are just as blunt: the connection must permit the traffic, "
                 "the plan must cover the devices you run it on, and a download that pauses every time "
                 "the tunnel reconnects is worse than no VPN at all."),
            ],
            "why": [
                ("Privacy carries 40% for this guide, with speed and value at 20% each, ease of use at "
                 "10% and streaming at 10% — streaming stays in the model only so this guide remains "
                 "comparable with the others."),
            ],
            "guide_title": "What a torrenting VPN has to get right",
            "guide": [
                ("Read the logging policy the way a lawyer would: what is retained, for how long, and "
                 "what happens on receipt of a legal request. Independent audits and court-tested claims "
                 "are worth more than a slogan, and both are facts we record per provider."),
                ("Then look at device limits and incoming connections. A desktop client plus a second "
                 "machine can exceed a small plan quickly, and one of our picks is marked for port "
                 "forwarding precisely because P2P behaves better when incoming connections work."),
            ],
            "picks": {
                "private-internet-access": ("Unlimited devices, open-source apps, port forwarding, and a "
                                            "no-logs claim tested twice in US federal court."),
                "protonvpn": ("The highest privacy score in the table at 9.7, Swiss jurisdiction and "
                              "open-source apps you can read rather than trust."),
                "mullvad": ("Swedish, independent, no account email and one flat monthly price — built for "
                            "leaving as little trace as the category allows."),
            },
            "faq": [
                ("Do I need a VPN to torrent?",
                 "Not for the protocol itself, which works without one. You need one if you do not want "
                 "your address visible to every peer, which is the normal reason people use it — and you "
                 "should only ever download material you have the right to download."),
                ("Which VPN is best for torrenting?",
                 "Private Internet Access for this task: unlimited devices, open-source apps and port "
                 "forwarding, with a court-tested privacy claim. Proton VPN leads on privacy score and "
                 "Mullvad on leaving no account behind."),
                ("Does a VPN slow down seeding?",
                 "Encryption and routing cost some throughput, yes. Our speed component covers that cost, "
                 "and it is the reason this guide weights speed at 20% rather than ignoring it — a tunnel "
                 "that is private but unusable has failed at the job too."),
            ],
        },

        "privacy": {
            "label": "privacy",
            "h1": "Best VPN for privacy",
            "desc": ("The best VPNs for privacy in 2026 — Proton VPN, NordVPN and Mullvad — chosen on "
                     "our privacy component, which carries 55% of this guide."),
            "lede": ("Privacy is the component this site already weights most heavily, so this guide "
                     "weights it harder still — and then asks what can actually be verified."),
            "intro": [
                ("Every provider claims not to log. The difference between them is what happens when "
                 "that claim is tested: independent audits, RAM-only infrastructure that cannot retain "
                 "data after a restart, named ownership, and court cases where the answer was nothing."),
                ("We record those facts per provider rather than summarising them into a feeling. Where "
                 "a claim has never been examined we say so — not published is a real answer and it is "
                 "printed as one."),
            ],
            "why": [
                ("Privacy carries 55% here — the heaviest single weight of any guide — with speed and "
                 "ease of use at 15% and 10%, value at 10% and streaming at 10%. The privacy component "
                 "itself is built from jurisdiction, audits, infrastructure and court evidence."),
            ],
            "guide_title": "How to read a privacy claim",
            "guide": [
                ("Start with jurisdiction and ownership: where the company is, which intelligence "
                 "alliances that country belongs to, and who is behind it. None of that is secret — we "
                 "list it on every review — and it changes what a legal request can compel."),
                ("Then look for the boring evidence: how many audits, which firm, when the last one was, "
                 "and whether the infrastructure would even hold the data after a restart. A provider "
                 "with seven audits and named owners is a different proposition from a logo and a promise."),
            ],
            "picks": {
                "protonvpn": ("Privacy 9.7, the highest we publish: Swiss jurisdiction, open-source apps "
                              "and a transparency report with numbers in it."),
                "nordvpn": ("Privacy 9.6 with six audits and RAM-only servers — the claim is enforced in "
                            "hardware rather than in a policy document."),
                "mullvad": ("Privacy 9.4, Swedish jurisdiction and a court-tested record: a 2023 police "
                            "raid that left with nothing."),
            },
            "faq": [
                ("Which VPN is the most private?",
                 "Proton VPN on our privacy component, at 9.7 of 10. NordVPN follows at 9.6 with RAM-only "
                 "infrastructure and six audits, and Mullvad at 9.4 with Swedish jurisdiction and no "
                 "account email at all. All three are open about what they are."),
                ("Are VPNs legal?",
                 "In most countries yes, including Sweden, the EU and the US. A minority of countries "
                 "restrict or license them, and the rules change. Check the law that applies where you "
                 "are before you rely on one — we will not give you a single global answer."),
                ("Does a VPN make me anonymous?",
                 "No. It hides your address from the sites you visit and from your network operator, not "
                 "from yourself: your accounts, your browser and your payment provider still know who you "
                 "are. Treat a VPN as one layer, not as a costume."),
            ],
        },

        "travel": {
            "label": "travel",
            "h1": "Best VPN for travel",
            "desc": ("The best VPNs for travelling in 2026 — NordVPN, ExpressVPN and Surfshark — chosen "
                     "on country coverage, speed and privacy for unfamiliar networks."),
            "lede": ("Airport wifi, a hotel portal that signs you out hourly, a network you cannot "
                     "inspect: travel is where a tunnel stops being optional."),
            "intro": [
                ("The threat on the road is ordinary: an open access point, a captive portal, a network "
                 "operator you have never heard of. Encrypting the connection removes most of that risk "
                 "for the price of a tap before you join."),
                ("The second half is coverage. The more countries a provider operates in, the more "
                 "likely you are to find a nearby address that a local service accepts — and nearby "
                 "matters, because distance is what makes a video call fall apart."),
            ],
            "why": [
                ("Speed carries 30% for this guide and privacy 25%, with streaming at 20%, ease of use "
                 "at 15% and value at 10%. Ease of use is weighted up deliberately: a travel VPN is "
                 "switched on in a hurry, on a phone, in a language you may not read well."),
            ],
            "guide_title": "Choosing a VPN for travel",
            "guide": [
                ("Coverage first. NordVPN publishes 111 countries, ExpressVPN 105 and Surfshark 100 — "
                 "all three are near the top of our table for exactly this reason, and every review page "
                 "prints its own count."),
                ("Then check the practicalities: how many devices the plan covers, whether the app works "
                 "without a laptop, and how long you have to change your mind after you land. Every "
                 "provider here offers at least a 30-day window."),
            ],
            "picks": {
                "nordvpn": ("111 countries, speed 9.4 and the best overall score in the table — the "
                            "widest map with the least compromise."),
                "expressvpn": ("105 countries and speed 9.6, our highest speed score, plus a "
                               "server list built for finding a working address quickly."),
                "surfshark": ("100 countries, unlimited devices and a two-year term at 59 USD — one plan "
                              "covers the whole family's trip."),
            },
            "faq": [
                ("Should I use a VPN on hotel wifi?",
                 "Yes, on any network you do not control — hotel, airport, café, a friend's router. The "
                 "tunnel keeps the connection encrypted from your device to the provider, which is the "
                 "part of the path the network operator can otherwise see."),
                ("Will a VPN work in every country?",
                 "No. A minority of countries restrict VPN use, some block providers, and the rules "
                 "change without notice. Check the current law before you travel and have a fallback "
                 "plan that does not depend on one."),
                ("Which VPN has the most countries?",
                 "NordVPN with 111, then ExpressVPN with 105 and Surfshark with 100. Country count is a "
                 "proxy, not a prize: what you actually need is a nearby address that your target "
                 "service accepts."),
            ],
        },

        "beginners": {
            "label": "beginners",
            "h1": "Best VPN for beginners",
            "desc": ("The easiest VPNs to start with in 2026 — CyberGhost, TunnelBear and ExpressVPN — "
                     "chosen on ease of use, price and how long you can change your mind."),
            "lede": ("Your first VPN should be hard to get wrong: clear apps, a price you understand "
                     "and enough time to find out whether you actually use it."),
            "intro": [
                ("Most people who quit a VPN do so in the first week, usually because the app asked "
                 "them a question they could not answer. Ease of use is not a nicety here — it is the "
                 "difference between a subscription and an unused one."),
                ("Second comes the exit: how long you have to change your mind, what the real total is "
                 "for the term, and whether a free tier lets you try the idea before paying anything. "
                 "All three are printed on this site before you click."),
            ],
            "why": [
                ("Ease of use carries 45% for this guide — the highest share of any — with value at 20%, "
                 "privacy and speed at 15% each and streaming at 5%. Nothing about the providers changes; "
                 "only what a beginner needs from them is weighted up."),
            ],
            "guide_title": "What a first VPN needs",
            "guide": [
                ("One screen, one button, sensible defaults. The best first VPN does not ask you to "
                 "choose a protocol, and it connects you to something reasonable without a tutorial. "
                 "Everything else can be learned later, on the same account."),
                ("Then check the money: the total for the term rather than a monthly headline, the "
                 "money-back window, and whether the plan covers the devices you already own. We print "
                 "all three next to every price on this site."),
            ],
            "picks": {
                "cyberghost": ("Ease of use 9.4, the clearest interface in this table and a 45-day "
                               "money-back window — the longest we list."),
                "tunnelbear": ("Ease of use 9.5 with a free tier and nine published audits, so you can "
                               "try the idea before you trust it with money."),
                "expressvpn": ("Ease of use 9.5 at the highest price here: one tap, sensible defaults, "
                               "and the speed to make the difference visible."),
            },
            "faq": [
                ("What is the easiest VPN to use?",
                 "TunnelBear and ExpressVPN tie at 9.5 for ease of use, with CyberGhost at 9.4 just behind "
                 "and the longest money-back window. All three are built to work without a manual, which "
                 "is what easy should mean."),
                ("Should a beginner start with a free VPN?",
                 "A free tier is a reasonable way to learn what a VPN does — three of our providers offer "
                 "one. Free tiers are usually slower, smaller and funded somehow, so read what the free "
                 "plan is funded by before you put anything sensitive through it."),
                ("How much should a first VPN cost?",
                 "Less than you would notice monthly and not more than you would be annoyed to lose. The "
                 "real number is the total for the term, which is why every price on this site shows the "
                 "total next to the monthly figure rather than instead of it."),
            ],
        },

        "iphone": {
            "label": "iPhone",
            "h1": "Best VPN for iPhone",
            "desc": ("The best VPNs for iPhone in 2026 — TunnelBear, ExpressVPN and Proton VPN — chosen "
                     "on ease of use, privacy and price for a phone-first setup."),
            "lede": ("On a phone the app is the product. This guide weights the interface hardest, "
                     "because a VPN you cannot operate one-handed is a VPN you will switch off."),
            "intro": [
                ("A phone VPN spends its life toggled: on at the airport, off at home, on again in a "
                 "café. Any provider can look good in a screenshot; what matters is whether the switch "
                 "is where your thumb expects it and whether it remembers what you wanted."),
                ("The other half is what the tunnel protects. On mobile the traffic includes banking "
                 "apps and messaging you would not open on hotel wifi, so privacy still carries real "
                 "weight — as does the price of a plan you may only use occasionally."),
            ],
            "why": [
                ("Ease of use carries 40% for this guide, privacy 25%, value 20%, speed 10% and "
                 "streaming 5%. Two of the three picks also publish a free tier, which matters when "
                 "you are testing whether you want this at all."),
            ],
            "guide_title": "Choosing a VPN for your iPhone",
            "guide": [
                ("Look for an app you can operate without reading: one connect button, a clear state, "
                 "and no requirement to understand protocols before the first connection. Everything "
                 "advanced should be optional, not a gate."),
                ("Then check what the plan costs over the term you actually buy, how many devices it "
                 "covers, and whether there is a free tier to try first. Those three facts sit next to "
                 "every price in the table below."),
            ],
            "picks": {
                "tunnelbear": ("Ease of use 9.5 with a free tier and nine published audits — the "
                               "gentlest way to start on a phone."),
                "expressvpn": ("Ease of use 9.5 and speed 9.6: the highest speed score here, for a phone "
                               "that also has to keep a call alive."),
                "protonvpn": ("Privacy 9.7 with a free tier and open-source apps, if you would rather "
                              "read the code than take the promise."),
            },
            "faq": [
                ("Do I need a VPN on my iPhone?",
                 "On your own mobile connection, usually not. On hotel, airport or café wifi, yes — that "
                 "is the case a tunnel is built for. It also hides your address from the sites you visit, "
                 "which some people want on principle."),
                ("Does a VPN drain iPhone battery?",
                 "An always-on tunnel costs some power, as any background connection does. We do not "
                 "publish battery figures because we cannot reproduce them across devices; what we do "
                 "publish is the speed cost of the tunnel itself."),
                ("Can I use one VPN on all my devices?",
                 "Depends on the plan: device limits run from 2 to unlimited in this table, and every "
                 "limit is printed in the comparison below. Three providers here do not count at all."),
            ],
        },

        "android": {
            "label": "Android",
            "h1": "Best VPN for Android",
            "desc": ("The best VPNs for Android in 2026 — Surfshark, Proton VPN and NordVPN — chosen on "
                     "ease of use, privacy and value for the widest phone platform."),
            "lede": ("Android gives you more choice than any other platform, including apps you can "
                     "read line by line. This guide weights privacy and openness accordingly."),
            "intro": [
                ("The Android ecosystem runs from a single toggle to a full network toolbox, and the "
                 "difference matters more here than on iOS because the same app often ships with more "
                 "options — and more ways to leave the tunnel half-configured."),
                ("Privacy carries real weight too. Android traffic is a mix of apps you chose and apps "
                 "you did not, so a no-logs policy you can audit is worth more than a longer feature list."),
            ],
            "why": [
                ("Ease of use carries 35% for this guide, privacy 30%, value 20%, speed 10% and "
                 "streaming 5%. Open-source apps are called out in the picks where our data records "
                 "them, because on Android that is the difference between trust and verification."),
            ],
            "guide_title": "Choosing a VPN for Android",
            "guide": [
                ("Decide how much you want to see. Some Android apps are one switch; others expose "
                 "protocol choices, split tunnelling and per-app rules. Neither is wrong, but the first "
                 "week sets the habit and a complicated app gets abandoned."),
                ("Then check the licence terms: the monthly figure is almost always tied to a multi-year "
                 "term, so read the total beside it. Every price on this site shows the total for the "
                 "term you actually buy."),
            ],
            "picks": {
                "surfshark": ("Unlimited devices and value 9.6 — the second-highest price score "
                              "of the eleven, on the platform with the most devices."),
                "protonvpn": ("Privacy 9.7, open-source apps and a free tier: verification rather than "
                              "a promise, at no cost to start."),
                "nordvpn": ("The best overall score in this table, with six audits and RAM-only servers "
                            "behind the app."),
            },
            "faq": [
                ("Do Android phones need a VPN?",
                 "On mobile data, rarely. On shared wifi, yes. Android also lets you route a single app "
                 "through the tunnel, which is useful if you only want one thing hidden — but the basics "
                 "are the same as on any other platform."),
                ("Which Android VPN is free?",
                 "Proton VPN, Windscribe and TunnelBear all publish a free tier. Free tiers are slower "
                 "and smaller by design, so read what the free plan is funded by before putting anything "
                 "sensitive through it."),
                ("Is an open-source Android VPN safer?",
                 "It is verifiable rather than safer by default: anyone can read what the app does, which "
                 "is exactly why we record open-source apps as a fact on every review instead of taking "
                 "it as a score."),
            ],
        },

        "windows": {
            "label": "Windows",
            "h1": "Best VPN for Windows",
            "desc": ("The best VPNs for Windows in 2026 — ExpressVPN, NordVPN and Private Internet "
                     "Access — chosen on ease of use, speed and privacy for a desktop setup."),
            "lede": ("On a desktop the VPN has to coexist with everything else you run — games, "
                     "calls, transfers — without becoming the thing you fight with."),
            "intro": [
                ("Windows is where most people first meet a VPN and where the most can go wrong: a "
                 "kill switch that blocks your work, a split tunnel you did not mean to set, an app "
                 "that starts with Windows and quietly reconnects all day."),
                ("It is also where speed matters most, because a desktop connection is usually the fast "
                 "one in the house and the tunnel is most visible there. That is why this guide weights "
                 "speed at a quarter of the decision."),
            ],
            "why": [
                ("Ease of use carries 35%, speed 25%, privacy 25%, value 10% and streaming 5%. One of "
                 "the three picks is chosen specifically because it exposes more control for people who "
                 "want it — and is marked as such rather than hidden behind a beginner-friendly default."),
            ],
            "guide_title": "What to check in a Windows VPN app",
            "guide": [
                ("Start with the defaults. A good Windows app connects sensibly, blocks leaks if the "
                 "tunnel drops, and never asks you to become a network engineer to get online. Advanced "
                 "controls should be there when you want them, invisible when you do not."),
                ("Then look at what surrounds the app: whether it can start with Windows, whether it "
                 "survives sleep, and how many devices the licence covers. Those are the three things "
                 "people discover in week two rather than on the sales page."),
            ],
            "picks": {
                "expressvpn": ("Ease of use 9.5 and speed 9.6 — the highest speed score here, in "
                               "a desktop app that stays out of the way, at the top of its price range."),
                "nordvpn": ("The best overall score here, with 10 simultaneous devices and RAM-only "
                            "infrastructure behind the client."),
                "private-internet-access": ("Open-source Windows apps, unlimited devices and a set of "
                                            "controls for people who want to see them."),
            },
            "faq": [
                ("Do I need a VPN on Windows at home?",
                 "On your own connection, usually not. On a shared or work network, on hotel wifi, or if "
                 "you do not want your address visible to the sites you visit, yes. It is a tool with a "
                 "specific job, not a general upgrade."),
                ("Does a VPN slow down Windows?",
                 "Encryption and routing cost some throughput — that is physics, and we do not pretend "
                 "otherwise. The speed component in the table is our published measure of that cost, "
                 "ranging from 9.6 down to 7.6 across this list."),
                ("Should the VPN start with Windows?",
                 "If you want protection before you notice you need it, yes. If you prefer to decide per "
                 "session, leave it manual. Either way check that the kill switch behaves the way you "
                 "expect before you rely on it."),
            ],
        },

        "mac": {
            "label": "Mac",
            "h1": "Best VPN for Mac",
            "desc": ("The best VPNs for Mac in 2026 — ExpressVPN, NordVPN and Proton VPN — chosen on "
                     "ease of use, privacy and speed for macOS."),
            "lede": ("Mac users tend to want the app to stay out of the way and the claims to be "
                     "checkable. This guide weights both."),
            "intro": [
                ("A Mac VPN lives in the menu bar and is judged by how little it interrupts: a clear "
                 "state, a quick connect, and no daemon that surprises you after an update."),
                ("Privacy is weighted at a quarter here because the platform's audience tends to care "
                 "about it — audits, jurisdiction and open-source clients are all recorded per provider "
                 "on this site, and all three picks score at or above 9.2 on that component."),
            ],
            "why": [
                ("Ease of use carries 40% for this guide, privacy 25%, speed 20%, value 10% and "
                 "streaming 5%. The weights are shown below and are the only thing that separates this "
                 "page from our overall ranking."),
            ],
            "guide_title": "Choosing a VPN for macOS",
            "guide": [
                ("Check how the app behaves across updates and sleep — a VPN that silently stops "
                 "protecting after a system update is worse than none, because you will not notice. "
                 "Every review here records whether the provider publishes audits and how recent they are."),
                ("Then the ordinary questions: how many devices, what the term actually costs, and how "
                 "long you have to change your mind. The answers are in the table below, next to the "
                 "score that put each provider on this page."),
            ],
            "picks": {
                "expressvpn": ("Ease of use 9.5 and speed 9.6: the least intrusive fast app in this "
                               "table, at its usual premium price."),
                "nordvpn": ("The best overall score here, six audits and RAM-only servers — the claim is "
                           "enforced in hardware rather than policy."),
                "protonvpn": ("Privacy 9.7 with Swiss jurisdiction and open-source clients, for a Mac "
                              "owner who would rather read than trust."),
            },
            "faq": [
                ("Does macOS need a VPN?",
                 "Not on your own connection. On any network you do not control, and if you do not want "
                 "your address visible to the sites you visit, yes. The tunnel does one job well and "
                 "does not fix anything else."),
                ("Do Mac VPNs use more battery?",
                 "An always-on tunnel costs some power on any laptop. We do not publish battery figures, "
                 "because they depend on hardware and usage we cannot reproduce — the speed component is "
                 "the number we can stand behind."),
                ("Can I use my Windows VPN licence on a Mac?",
                 "Usually yes: all eleven providers here cover multiple platforms on one subscription, and "
                 "the device limit — not the operating system — is what you should check. Every limit is "
                 "in the comparison table below."),
            ],
        },

        "routers": {
            "label": "routers",
            "h1": "Best VPN for routers",
            "desc": ("The best VPNs to run on a router in 2026 — NordVPN, ExpressVPN and Surfshark — "
                     "chosen on speed, setup effort and the device slots they save."),
            "lede": ("A VPN on the router protects every device in the house at once, including the "
                     "ones that cannot run an app. The trade is speed and setup, and this guide weights "
                     "both."),
            "intro": [
                ("The appeal is simple: one configuration covers the television, the console, the "
                 "printer and the guest wifi, and nobody in the house has to remember to switch "
                 "anything on. The router consumes one of the plan's device slots, which is exactly "
                 "why unlimited plans change the arithmetic."),
                ("The cost is throughput — every packet is encrypted on the way out — and the effort of "
                 "configuring it once properly. Ten of the eleven providers here offer OpenVPN, nine also offer "
                 "WireGuard, and ExpressVPN ships Lightway in its place; what differs is how much "
                 "speed survives."),
            ],
            "why": [
                ("Speed carries 35% for this guide, ease of use 30%, privacy 20%, value 10% and "
                 "streaming 5%. Ease of use is weighted up because works after you set it up once is "
                 "the entire requirement, and it is easier to promise than to deliver."),
            ],
            "guide_title": "Setting up a VPN on your router",
            "guide": [
                ("Confirm the firmware first. OpenVPN or WireGuard support — or firmware that adds it — "
                 "is the requirement; ten of the eleven providers here offer OpenVPN, nine add WireGuard, and "
                 "the question is which one your router handles better."),
                ("Then plan the devices. A router counts as one connection, so the household's phones "
                 "and laptops can run on the same subscription as the router itself — or on a separate "
                 "one if you want the tunnel only on the living-room screen."),
            ],
            "picks": {
                "nordvpn": ("Speed 9.4 with 111 countries and 10 device slots — the strongest all-round "
                            "choice when the whole house sits behind it."),
                "expressvpn": ("Speed 9.6, the highest we publish, which is what a router needs most "
                               "once every packet is being encrypted."),
                "surfshark": ("Unlimited devices and value 9.6 — one subscription covers the router and "
                              "everything else without counting."),
            },
            "faq": [
                ("Which VPN works best on a router?",
                 "Any that offers OpenVPN — ten of the eleven providers here do — or WireGuard, which nine of them "
                 "also ship. What separates them is how much speed survives the extra encryption, which "
                 "is why this guide weights speed at 35%: NordVPN, ExpressVPN and Surfshark lead on "
                 "that combination."),
                ("Does a router VPN slow down my internet?",
                 "Yes, some — every packet is encrypted, often on hardware without dedicated crypto "
                 "silicon. The size of the hit depends on the router as much as the provider, which is "
                 "why we publish a speed component rather than a promise."),
                ("Do I still need a VPN app on my phone?",
                 "Not for the home network, if the router tunnel is on. Keep an app for mobile data and "
                 "for any network away from home — the router only protects traffic that passes through "
                 "it, and your phone leaves the house with you."),
            ],
        },
    },

    "sv": {
        "hub": {
            "eyebrow": "Guider per uppgift",
            "h1": "Bäst VPN för jobbet du faktiskt har",
            "desc": ("Tolv VPN-guider, en per uppgift: streaming, Netflix, gaming, torrenting, "
                     "integritet, resor, mobiler, datorer och routrar — var och en med "
                     "publicerad vikning och en topp 3 vi skulle köpa själva."),
            "lede": ("Ingen behöver den bästa VPN:n i abstrakt mening. Du behöver den bästa "
                     "VPN:n för ett visst jobb, och jobbet ändrar svaret: vikterna flyttas, "
                     "betygen gör det inte."),
            "intro": [
                ("Varje guide viktar om samma fem komponenter vi alltid använder — integritet, "
                 "hastighet, pris, streaming och användarvänlighet. En streamingguide lutar sig "
                 "mot streaming och hastighet, en guide om integritet lutar sig mot "
                 "integriteten. Komponentbetygen i sig flyttas aldrig för att passa en sida."),
                ("Topp 3 i varje guide är redaktionella val gjorda för just den uppgiften, och de "
                 "är inte alltid de tre översta i vår totalrankning. Där ett val verkar "
                 "överraskande står skälet under kortet, så att du kan invända mot det utifrån "
                 "fakta."),
            ],
            "faq": [
                ("Betalas de här guiderna för?",
                 "Länkarna är annonslänkar, så vi får en provision om du prenumererar via en av "
                 "dem. Provisionen ändrar inget betyg, inget val och ingen vikt — tabellerna och "
                 "metoden fungerar på samma sätt oavsett om du klickar eller inte, och "
                 "leverantörsdata verifieras i en fast cykel."),
                ("Varför tolv guider och inte en enda lista?",
                 "För att en enda lista måste medelta över uppgifter som drar åt motsatta håll. "
                 "Torrenting bryr sig om integritet och enhetsgränser, en guide om tv bryr sig "
                 "om konsekvens och hastighet. Separata vikter ger användbarare svar än en enda "
                 "rankning kan."),
                ("Mäter ni hastigheten själva?",
                 "Nej, och vi publicerar inga ping- eller genomströmningssiffror vi inte kan "
                 "återskapa. Varje hastighetssiffra på den här webbplatsen är en komponent i en "
                 "publicerad betygsmodell, inte en mätning från vår egen anslutning — och "
                 "därför betyder metodsidan mer än någon rubrik."),
            ],
        },

        "streaming": {
            "label": "streaming",
            "h1": "Bäst VPN för streaming",
            "desc": ("Bästa VPN för streaming 2026: ExpressVPN, NordVPN och Surfshark, valda på "
                     "streamingförmåga, hastighet och pris med vikter vi publicerar."),
            "lede": ("Streaming är där en VPN antingen försvinner i bakgrunden eller förstör "
                     "kvällen. Vi viktar om de fem komponenter vi alltid använder mot de två som "
                     "avgör, och väljer sedan de tre som håller."),
            "intro": [
                ("En ström misslyckas på två sätt: den buffrar, eller så vägrar tjänsten "
                 "anslutningen för att den inte gillar var du verkar komma ifrån. Båda är "
                 "vanliga, och båda säljs som bästa VPN av sajter som aldrig sett något genom "
                 "en."),
                ("Därför rankar den här guiden inte enbart på streaming. Hastighet avgör om en "
                 "ström med hög bithastighet håller sig smidig, priset avgör om det är värt att "
                 "förnya, och integritet räknas fortfarande eftersom samma tunnel bär både "
                 "din bank och din inkorg."),
            ],
            "why": [
                ("Streaming bär 40 % av beslutet och hastighet 30 %; pris 15 %, integritet 10 % "
                 "och användarvänlighet 5 %. Komponentbetygen kommer direkt från vår "
                 "publicerade modell — inget omvärderas för en guide, bara vikterna ändras, och "
                 "de vikterna visas nedan."),
            ],
            "guide_title": "Vad en streaming-VPN måste få rätt",
            "guide": [
                ("Konsekvens slår toppar. Vilken VPN som helst kan hålla anslutningen i tio "
                 "minuter en god kväll; frågan är om samma server fortfarande fungerar "
                 "fredagskvällen, i tv-appen, medan någon annan i hushållet sitter i ett "
                 "videosamtal."),
                ("Enhetsgränser betyder mer än man tror. En tv, en konsol och en telefon är tre "
                 "samtidiga strömmar, och en plan för fem enheter är inte samma sak som en för "
                 "obegränsat — jämförelsetabellen nedan markerar vilket som är vilket."),
            ],
            "picks": {
                "expressvpn": ("Högsta streamingbetyg här, 9,4, och högsta hastighetsbetyget, "
                               "9,6 — den att köpa om bilden inte får stanna upp."),
                "nordvpn": ("9,2 i streaming inuti det starkaste totalbetyget i tabellen, så "
                            "inget annat viker när du slår på tunneln."),
                "surfshark": ("9,0 i streaming med obegränsat antal enheter, vilket spelar roll "
                              "när samma kväll går på en tv, en telefon och en konsol samtidigt."),
            },
            "faq": [
                ("Vilken VPN är bäst för streaming?",
                 "På den här webbplatsen ExpressVPN: den har högsta streamingkomponenten, 9,4, "
                 "och högsta hastighetskomponenten, 9,6. NordVPN ligger på 9,2 och kostar "
                 "mindre över en lång avtalslängd, medan Surfshark lägger till obegränsade "
                 "enheter om strömmen går på mer än en skärm."),
                ("Behöver jag en VPN för att strömma?",
                 "Inte alltid. Om din tjänst är licensierad där du tittar behöver du ingen. Det "
                 "spelar roll när du reser, när en titel är licensierad någon annanstans, eller "
                 "när ditt nätverk behandlar video dåligt — och det får aldrig vara skälet till "
                 "att en livesändning hakar."),
                ("Kommer en VPN att få min ström att buffra?",
                 "Kryptering har en kostnad, men skillnaden mellan en snabb och en långsam "
                 "leverantör är större än tunnelns kostnad. Det är precis vad "
                 "hastighetskomponenten mäter, och den sträcker sig från 9,6 överst i tabellen "
                 "till 7,6 längst ned."),
            ],
        },

        "netflix": {
            "label": "Netflix",
            "h1": "Bäst VPN för Netflix",
            "desc": ("Tre VPN som vår Netflix-viktning placerar högst i 2026 — ExpressVPN, NordVPN "
                     "och CyberGhost — valda på våra betyg för streaming, hastighet och "
                     "användarvänlighet."),
            "lede": ("Netflix är testet alla kör först och det som oftast fuskas med. Här är vad "
                     "som faktiskt avgör om en katalog på en annan kontinent öppnas."),
            "intro": [
                ("Kataloger licensieras per land, så en VPN låser inte upp Netflix så mycket "
                 "som den presenterar en annan adress och hoppas att tjänsten accepterar den. "
                 "Vissa servrar gör det, andra inte, och det som fungerade förra månaden är "
                 "ingen garanti för nästa."),
                ("Därför bevisar en skärmbild ingenting. Vi lutar oss mot streamingkomponenten, "
                 "som byggs på upprepade kontroller i stället för en enda lyckad kväll, och mot "
                 "hastighetskomponenten som håller en 4K-ström från att tyst kollapsa till "
                 "något sämre."),
            ],
            "why": [
                ("Streaming bär 45 % här — den tyngsta av någon guide — med hastighet 25 %, "
                 "pris 15 % och användarvänlighet 10 %, eftersom att byta region med en "
                 "fjärrkontroll är ett annat jobb än att klicka med en mus. Integritet tar de "
                 "sista 5 %."),
            ],
            "guide_title": "Så bedömer vi en Netflix-VPN",
            "guide": [
                ("En leverantör presenterar antingen en adress som tjänsten accepterar eller så "
                 "gör den det inte, och felet dyker upp som en felkod i stället för en sämre "
                 "bild. Konsekvens kontrollerna emellan är vad streamingkomponenten belönar, "
                 "inte en god kväll."),
                ("Den andra halvan är bandbredd. Netflix anpassar nedåt i tystnad, så en svag "
                 "anslutning ser ut som en sämre bild i stället för ett fel. Hastigheten är "
                 "skyddet mot det, och därför kan en leverantör med något lägre "
                 "streamingbetyg fortfarande vara det bättre köpet."),
            ],
            "picks": {
                "expressvpn": ("Streaming 9,4 och hastighet 9,6: den tillförlitligaste "
                               "kombinationen vi publicerar, till det högsta priset i tabellen."),
                "nordvpn": ("Streaming 9,2 med det bästa totalbetyget av de elva, och 111 länder "
                            "att välja en adress från."),
                "cyberghost": ("Streaming 9,0, användarvänlighet 9,4 och 45 dagars ångerrätt — "
                               "den längsta vi listar — om katalogen besvikar."),
            },
            "faq": [
                ("Vilken VPN fungerar med Netflix?",
                 "De tre på den här sidan, så långt våra kontroller räcker: ExpressVPN, NordVPN "
                 "och CyberGhost har alla 9,0 eller bättre i streaming. Tillgängligheten "
                 "varierar per land och per server, så betrakta garantierna du läser någon "
                 "annanstans som marknadsföring."),
                ("Varför slutade min VPN fungera med Netflix?",
                 "Eftersom tjänsten känner igen adressintervallet som din VPN-server använder "
                 "och blockerar det. Att byta serverplats i appen återställer det oftast; om "
                 "det inte gör det har leverantören inte hunnit ikapp och en annan region är "
                 "det pragmatiska svaret."),
                ("Är det mot reglerna att använda VPN med Netflix?",
                 "Att strömma en annan regions katalog via en VPN kan strida mot tjänstens "
                 "användarvillkor. Läs de villkor som gäller för dig och bestäm själv — vi "
                 "låtsas inte att det finns ett enda svar för alla länder."),
            ],
        },

        "gaming": {
            "label": "gaming",
            "h1": "Bäst VPN för gaming",
            "desc": ("Bästa VPN för gaming 2026 — ExpressVPN, NordVPN och Surfshark — valda på "
                     "hastighet, integritet och pris, utan påhittade ping-siffror."),
            "lede": ("Spelare vill ha låg latens, och vi vägrar hitta på hur låg den är. Vi kan "
                     "inte mäta din väg till en spelserver, så den här guiden viktar det vi "
                     "kan publicera ärligt."),
            "intro": [
                ("Den ärliga gränsen först: vi mäter inte ping, och vi publicerar inte "
                 "genomströmningssiffror vi inte kan återskapa. En VPN som påstår att sänka din "
                 "latens gör ett påstående om ditt nätverk som ingen kan göra från vårt."),
                ("Det vi kan vikta är hastighetskomponenten — hur lite en tunnel kostar i "
                 "modellen vi publicerar — plus integritet, eftersom ett spelkonto med en "
                 "betalmetod kopplad är värt att stjäla, och pris, eftersom en prenumeration du "
                 "behåller slår en du byter bort."),
            ],
            "why": [
                ("Hastighet bär 45 % i den här guiden, den högsta andelen av någon. Streaming "
                 "får 20 %, integritet 15 %, och användarvänlighet och pris 10 % var. De "
                 "vikterna visas nedan och är det enda som skiljer från vår totalrankning."),
            ],
            "guide_title": "Vad du ska titta på i en gaming-VPN",
            "guide": [
                ("Stabilitet betyder mer än bra siffror en god kväll. En tunnel som håller "
                 "genom en lång session, på en server du kan hitta igen i morgon, är värd mer "
                 "än en väg som var snabb en gång och sedan har flyttats."),
                ("Enhetsgränser avgör hushållet. En router, en PC och en konsol kan vara tre av "
                 "de samtidiga anslutningar en plan tillåter, och obegränsade planer tar bort "
                 "hela räkneexemplet — tabellen nedan visar varje leverantörs gräns."),
            ],
            "picks": {
                "expressvpn": ("Hastighet 9,6, det högsta vi publicerar, och gaming är ett av "
                               "de fyra användningsområden den här leverantören är märkt bäst "
                               "för."),
                "nordvpn": ("Hastighet 9,4 inuti det bästa totalbetyget här, med 10 samtidiga "
                            "enheter för resten av hushållet."),
                "surfshark": ("Hastighet 8,8, obegränsade enheter och det lägsta tvåårspriset "
                              "av dessa tre, 589 kr — det förnuftiga valet för en delad "
                              "spel-PC."),
            },
            "faq": [
                ("Minskar en VPN ping?",
                 "Inte automatiskt. En VPN ändrar vägen din trafik tar, vilket kan hjälpa eller "
                 "skada; vi publicerar inte ping-siffror eftersom vi inte kan återskapa dina. "
                 "Det vi publicerar är hur mycket genomströmning tunneln kostar i vår "
                 "hastighetskomponent, och det är den ärliga delen."),
                ("Kommer en VPN att göra att jag blir utestängd från ett spel?",
                 "Att använda en VPN bryter inte mot reglerna i de flesta spel, men vissa "
                 "begränsar eller blockerar anslutningar som ser ut som datacentertrafik, och "
                 "några straffar konton för det. Kontrollera reglerna i spelet du spelar innan "
                 "du ansluter."),
                ("Vilket protokoll ska jag använda för gaming?",
                 "Varje leverantör här erbjuder ett modernt protokoll — WireGuard, eller en "
                 "motsvarande egenutvecklad variant — och det är det förnuftiga standardvalet "
                 "för latens och batteri. OpenVPN är kvar som reserv när ett nätverk blockerar "
                 "det nyare, och båda listas på varje recensionssida."),
            ],
            "spotlight": {
                "eyebrow": "För ping, inte integritet",
                "title": "Ett annat verktyg för ett spelproblem: ping",
                "body": ("GearUP Booster är ingen VPN och ingår inte i vår rankning: den döljer inte "
                         "din IP-adress eller krypterar din trafik som leverantörerna ovan gör. Den gör "
                         "en sak — dirigerar speltrafik över kortare vägar för att sänka ping, "
                         "paketförlust och jitter på Windows, mobil och konsoler — med en gratis "
                         "provperiod så att du kan testa den på din egen uppkoppling innan du betalar."),
                "note": "Ingen VPN, och inte rankad här. En booster kan inte fixa långsamt bredband eller en server på en annan kontinent.",
                "cta": "Prova GearUP gratis",
                "affiliate_id": "gearup-booster",
            },
        },

        "torrenting": {
            "label": "torrenting",
            "h1": "Bäst VPN för torrenting",
            "desc": ("Bästa VPN för torrenting 2026 — Private Internet Access, Proton VPN och "
                     "Mullvad — valda på integritet, pris och de enhetsgränser som spelar roll "
                     "för P2P."),
            "lede": ("Torrenting är den enda uppgiften där integritet inte är en funktion utan "
                     "hela poängen, och där en enhetsgräns eller en saknad port kan avsluta "
                     "nedladdningen."),
            "intro": [
                ("En torrentklient annonserar din adress till varje peer i svärmen. Med en VPN "
                 "ser svärmen VPN:ns adress i stället, och det är hela mekaniken — och skälet "
                 "till att en leverantörs loggpolicy betyder mer här än någon annanstans på "
                 "den här webbplatsen."),
                ("De praktiska begränsningarna är lika raka: anslutningen måste tillåta "
                 "trafiken, planen måste täcka de enheter du kör den på, och en nedladdning som "
                 "pausar varje gång tunneln återansluter är värre än ingen VPN alls."),
            ],
            "why": [
                ("Integritet bär 40 % i den här guiden, med hastighet och pris på 20 % var, "
                 "användarvänlighet 10 % och streaming 10 % — streaming står kvar i modellen "
                 "bara för att den här guiden ska vara jämförbar med de andra."),
            ],
            "guide_title": "Vad en torrent-VPN måste få rätt",
            "guide": [
                ("Läs loggpolicyn som en jurist skulle: vad som behålls, under hur lång tid, och "
                 "vad som händer vid mottagande av en rättslig begäran. Oberoende revisioner och "
                 "rättsligt prövade påståenden är värd mer än en slogan, och båda är fakta vi "
                 "registrerar per leverantör."),
                ("Titta sedan på enhetsgränser och inkommande anslutningar. En skrivbordsklient "
                 "plus en andra maskin kan överstiga en liten plan snabbt, och ett av våra val "
                 "är märkt för portvidarebefordran just för att P2P beter sig bättre när "
                 "inkommande anslutningar fungerar."),
            ],
            "picks": {
                "private-internet-access": ("Obegränsade enheter, källkodsöppna appar, "
                                            "portvidarebefordran och ett loggfritt påstående "
                                            "prövat två gånger i amerikansk federal domstol."),
                "protonvpn": ("Det högsta integritetsbetyget i tabellen, 9,7, schweizisk "
                              "jurisdiktion och källkodsöppna appar du kan läsa i stället för "
                              "att lita på."),
                "mullvad": ("Svenskt, oberoende, inget e-postkonto och ett fast månadspris — "
                            "byggt för att lämna så lite spår som kategorin tillåter."),
            },
            "faq": [
                ("Behöver jag en VPN för att torrenta?",
                 "Inte för protokollet i sig, det fungerar utan. Du behöver en om du inte vill "
                 "att din adress syns för varje peer, och det är den vanliga anledningen att "
                 "folk använder den — och du ska bara någonsin ladda ner material du har rätt "
                 "att ladda ner."),
                ("Vilken VPN är bäst för torrenting?",
                 "Private Internet Access för den här uppgiften: obegränsade enheter, "
                 "källkodsöppna appar och portvidarebefordran, med ett rättsligt prövat "
                 "integritetspåstående. Proton VPN leder på integritetsbetyget och Mullvad på "
                 "att inte lämna något konto efter sig."),
                ("Saktar en VPN ner seedandet?",
                 "Kryptering och routing kostar genomströmning, ja. Vårt hastighetsbetyg täcker "
                 "den kostnaden, och det är skälet till att den här guiden viktar hastighet på "
                 "20 % i stället för att ignorera den — en tunnel som är privat men oanvändbar "
                 "har misslyckats med jobbet också."),
            ],
        },

        "privacy": {
            "label": "integritet",
            "h1": "Bäst VPN för integritet",
            "desc": ("Bästa VPN för integritet 2026 — Proton VPN, NordVPN och Mullvad — valda på "
                     "vår integritetskomponent, som bär 55 % av den här guiden."),
            "lede": ("Integritet är den komponent den här webbplatsen redan viktar tyngst, så "
                     "den här guiden viktar den ännu hårdare — och frågar sedan vad som "
                     "faktiskt går att verifiera."),
            "intro": [
                ("Varje leverantör påstår att den inte loggar. Skillnaden mellan dem är vad som "
                 "händer när påståendet prövas: oberoende revisioner, RAM-baserad "
                 "infrastruktur som inte kan behålla data efter en omstart, namngivet ägande, "
                 "och rättsfall där svaret var ingenting."),
                ("Vi registrerar de fakta per leverantör i stället för att sammanfatta dem till "
                 "en känsla. Där ett påstående aldrig har granskats säger vi det — inte "
                 "publicerat är ett verkligt svar och det skrivs ut som ett."),
            ],
            "why": [
                ("Integritet bär 55 % här — den tyngsta enskilda vikten av någon guide — med "
                 "hastighet 15 %, användarvänlighet 10 %, pris 10 % och streaming 10 %. Själva "
                 "integritetskomponenten byggs på jurisdiktion, revisioner, infrastruktur och "
                 "rättslig evidens."),
            ],
            "guide_title": "Så läser du ett integritetspåstående",
            "guide": [
                ("Börja med jurisdiktion och ägande: var företaget är, vilka "
                 "underrättelseallianser landet tillhör, och vem som står bakom. Inget av det "
                 "är hemligt — vi listar det på varje recension — och det förändrar vad en "
                 "rättslig begäran kan tvinga fram."),
                ("Titta sedan på den tråkiga evidensen: hur många revisioner, vilket firma, när "
                 "den senaste var, och om infrastrukturen ens skulle ha kvar data efter en "
                 "omstart. En leverantör med sju revisioner och namngivna ägare är ett annat "
                 "erbjudande än en logotyp och ett löfte."),
            ],
            "picks": {
                "protonvpn": ("Integritet 9,7, det högsta vi publicerar: schweizisk jurisdiktion, "
                              "källkodsöppna appar och en transparensrapport med siffror i."),
                "nordvpn": ("Integritet 9,6 med sex revisioner och RAM-baserade servrar — "
                            "påståendet upprätthålls i hårdvara i stället för i ett "
                            "policydokument."),
                "mullvad": ("Integritet 9,4, svensk jurisdiktion och en rättsligt prövad "
                            "historia: en polisrazzia 2023 som gick därifrån med ingenting."),
            },
            "faq": [
                ("Vilken VPN är mest privat?",
                 "Proton VPN på vår integritetskomponent, med 9,7 av 10. NordVPN följer med "
                 "9,6, RAM-baserad infrastruktur och sex revisioner, och Mullvad med 9,4, "
                 "svensk jurisdiktion och inget e-postkonto alls. Alla tre är öppna med vad de "
                 "är."),
                ("Är VPN lagligt?",
                 "I de flesta länder ja, inklusive Sverige, EU och USA. En minoritet av länder "
                 "begränsar eller licensierar dem, och reglerna ändras. Kontrollera den lag som "
                 "gäller där du är innan du litar på en — vi ger dig inte ett enda globalt "
                 "svar."),
                ("Gör en VPN mig anonym?",
                 "Nej. Den döljer din adress från de sidor du besöker och från din "
                 "nätverksoperatör, inte från dig själv: dina konton, din webbläsare och din "
                 "betalleverantör vet fortfarande vem du är. Betrakta en VPN som ett lager, "
                 "inte som en mask."),
            ],
        },

        "travel": {
            "label": "resor",
            "h1": "Bäst VPN för resor",
            "desc": ("Bästa VPN för resor 2026 — NordVPN, ExpressVPN och Surfshark — valda på "
                     "länderstäckning, hastighet och integritet för okända nätverk."),
            "lede": ("Flygplatswifi, en hotellportal som loggar ut dig varje timme, ett nätverk "
                     "du inte kan inspektera: resor är där tunneln slutar vara valfri."),
            "intro": [
                ("Hotet på resan är vardagligt: en öppen accesspunkt, en inloggningsportal, en "
                 "nätverksoperatör du aldrig hört talas om. Att kryptera anslutningen tar bort "
                 "det mesta av risken för priset av ett tryck innan du ansluter."),
                ("Den andra halvan är täckning. Ju fler länder en leverantör verkar i, desto "
                 "större chans att du hittar en nära adress som en lokal tjänst accepterar — och "
                 "nära spelar roll, eftersom avståndet är det som får ett videosamtal att falla "
                 "isär."),
            ],
            "why": [
                ("Hastighet bär 30 % i den här guiden och integritet 25 %, med streaming 20 %, "
                 "användarvänlighet 15 % och pris 10 %. Användarvänlighet vikts upp med flit: "
                 "en VPN för resor slås på i hastverk, på en telefon, på ett språk du kanske "
                 "inte läser väl."),
            ],
            "guide_title": "Välja VPN för resor",
            "guide": [
                ("Täckning först. NordVPN publicerar 111 länder, ExpressVPN 105 och Surfshark "
                 "100 — alla tre ligger nära toppen i vår tabell av exakt den skälen, och varje "
                 "recensionssida skriver ut sitt eget antal."),
                ("Kontrollera sedan det praktiska: hur många enheter planen täcker, om appen "
                 "fungerar utan bärbar dator, och hur lång tid du har på dig att ändra dig "
                 "efter att du landat. Varje leverantör här erbjuder minst 30 dagars "
                 "ångerrätt."),
            ],
            "picks": {
                "nordvpn": ("111 länder, hastighet 9,4 och det bästa totalbetyget i tabellen — "
                            "den bredaste kartan med minst kompromiss."),
                "expressvpn": ("105 länder och hastighet 9,6, vårt högsta hastighetsbetyg, "
                               "plus en serverlista byggd för att snabbt hitta en "
                               "fungerande adress."),
                "surfshark": ("100 länder, obegränsade enheter och en tvåårsperiod på 589 kr — "
                              "en plan täcker hela familjens resa."),
            },
            "faq": [
                ("Ska jag använda VPN på hotellets wifi?",
                 "Ja, på vilket nätverk som helst som du inte kontrollerar — hotell, flygplats, "
                 "café, en väns router. Tunneln håller anslutningen krypterad från din enhet "
                 "till leverantören, och det är den del av vägen som nätverksoperatören i annat "
                 "fall kan se."),
                ("Kommer en VPN att fungera i alla länder?",
                 "Nej. En minoritet av länder begränsar VPN-användning, vissa blockerar "
                 "leverantörer, och reglerna ändras utan förvarning. Kontrollera den aktuella "
                 "lagen innan du reser och ha en reservplan som inte beror på en."),
                ("Vilken VPN har flest länder?",
                 "NordVPN med 111, sedan ExpressVPN med 105 och Surfshark med 100. "
                 "Länderantal är en indikator, inte ett pris: vad du faktiskt behöver är en "
                 "nära adress som din måltjänst accepterar."),
            ],
        },

        "beginners": {
            "label": "nybörjare",
            "h1": "Bäst VPN för nybörjare",
            "desc": ("Bästa VPN att börja med 2026 — CyberGhost, TunnelBear och ExpressVPN — "
                     "valda på användarvänlighet, pris och hur länge du har på dig att ändra "
                     "dig."),
            "lede": ("Din första VPN ska vara svår att få fel: tydliga appar, ett pris du "
                     "förstår och tillräckligt med tid för att reda ut om du faktiskt använder "
                     "den."),
            "intro": [
                ("De flesta som slutar med en VPN gör det första veckan, oftast för att appen "
                 "ställde en fråga de inte kunde svara på. Användarvänlighet är inte en bonus "
                 "här — det är skillnaden mellan en prenumeration och en oanvänd."),
                ("Sedan kommer utgången: hur lång tid du har på dig att ändra dig, vad totalen "
                 "faktiskt blir för avtalslängden, och om en gratisnivå låter dig prova idén "
                 "innan du betalar något. Alla tre står på den här webbplatsen innan du "
                 "klickar."),
            ],
            "why": [
                ("Användarvänlighet bär 45 % i den här guiden — den högsta andelen av någon — "
                 "med pris 20 %, integritet 15 %, hastighet 15 % och streaming 5 %. Ingenting "
                 "om leverantörerna ändras; bara det en nybörjare behöver av dem vikts upp."),
            ],
            "guide_title": "Vad den första VPN:n behöver",
            "guide": [
                ("En skärm, en knapp, förnuftiga standardval. Den bästa första VPN:n ber dig "
                 "inte välja protokoll, och den ansluter dig till något rimligt utan genomgång. "
                 "Allt annat kan läras senare, på samma konto."),
                ("Kontrollera sedan pengarna: totalen för avtalslängden i stället för en "
                 "rubriksats per månad, ångerrättsfönstret, och om planen täcker de enheter du "
                 "redan äger. Vi skriver alla tre bredvid varje pris på den här webbplatsen."),
            ],
            "picks": {
                "cyberghost": ("Användarvänlighet 9,4, den tydligaste gränssnittet i tabellen "
                               "och 45 dagars ångerrätt — den längsta vi listar."),
                "tunnelbear": ("Användarvänlighet 9,5 med en gratisnivå och nio publicerade "
                               "revisioner, så att du kan prova idén innan du litar på den med "
                               "pengar."),
                "expressvpn": ("Användarvänlighet 9,5 till det högsta priset här: ett tryck, "
                               "förnuftiga standardval och hastigheten att göra skillnaden "
                               "synlig."),
            },
            "faq": [
                ("Vilken VPN är lättast att använda?",
                 "TunnelBear och ExpressVPN delar förstaplatsen med 9,5 i användarvänlighet, "
                 "med CyberGhost på 9,4 precis bakom och den längsta ångerrätten. Alla tre är "
                 "byggda för att fungera utan manual, och det är vad lätt ska betyda."),
                ("Bör en nybörjare börja med en gratis-VPN?",
                 "En gratisnivå är ett rimligt sätt att lära sig vad en VPN gör — tre av våra "
                 "leverantörer erbjuder en gratisnivå. Gratisnivåer är oftast långsammare, "
                 "mindre och finansierade på något sätt, så läs vad den fria planen finansieras "
                 "av innan du skickar något känsligt genom den."),
                ("Hur mycket ska en första VPN kosta?",
                 "Mindre än du märker per månad och inte mer än du blir irriterad över att "
                 "förlora. Den verkliga siffran är totalen för avtalslängden, och därför visar "
                 "varje pris på den här webbplatsen totalen bredvid månadssiffran, inte i "
                 "stället för den."),
            ],
        },

        "iphone": {
            "label": "iPhone",
            "h1": "Bäst VPN för iPhone",
            "desc": ("Bästa VPN för iPhone 2026 — TunnelBear, ExpressVPN och Proton VPN — valda "
                     "på användarvänlighet, integritet och pris för en telefon i första hand."),
            "lede": ("På en telefon är appen produkten. Den här guiden viktar gränssnittet "
                     "tyngst, eftersom en VPN du inte kan hantera med en hand är en VPN du "
                     "kommer att stänga av."),
            "intro": [
                ("En VPN på telefon lever sitt liv i att växlas: på vid flygplatsen, av hemma, "
                 "på igen i ett café. Vilken leverantör som helst kan se bra ut i en skärmbild; "
                 "det som spelar roll är om växeln ligger där tummen förväntar sig den och om "
                 "den kommer ihåg vad du ville."),
                ("Den andra halvan är vad tunneln skyddar. På mobil innefattar trafiken "
                 "bankappar och meddelanden du inte skulle öppna på hotellets wifi, så "
                 "integritet bär fortfarande verklig tyngd — och det gör priset på en plan du "
                 "kanske bara använder ibland."),
            ],
            "why": [
                ("Användarvänlighet bär 40 % i den här guiden, integritet 25 %, pris 20 %, "
                 "hastighet 10 % och streaming 5 %. Två av de tre valen publicerar också en "
                 "gratisnivå, vilket spelar roll när du testar om du vill ha det alls."),
            ],
            "guide_title": "Välja VPN till din iPhone",
            "guide": [
                ("Sök efter en app du kan använda utan att läsa: en anslutningsknapp, ett "
                 "tydligt läge och inget krav på att förstå protokoll före första "
                 "anslutningen. Allt avancerat ska vara valfritt, inte en mur."),
                ("Kontrollera sedan vad planen kostar över den avtalslängd du faktiskt köper, "
                 "hur många enheter den täcker, och om det finns en gratisnivå att prova först. "
                 "De tre fakta finns bredvid varje pris i tabellen nedan."),
            ],
            "picks": {
                "tunnelbear": ("Användarvänlighet 9,5 med en gratisnivå och nio publicerade "
                               "revisioner — det skonsammaste sättet att börja på en telefon."),
                "expressvpn": ("Användarvänlighet 9,5 och hastighet 9,6: det högsta "
                               "hastighetsbetyget här, för en telefon som också måste hålla ett "
                               "samtal vid liv."),
                "protonvpn": ("Integritet 9,7 med en gratisnivå och källkodsöppna appar, om du "
                              "hellre läser koden än tar löftet."),
            },
            "faq": [
                ("Behöver jag en VPN på min iPhone?",
                 "På din egen mobilanslutning, oftast inte. På hotellets, flygplatsens eller "
                 "caféts wifi, ja — det är fallet tunneln är byggd för. Den döljer också din "
                 "adress från de sidor du besöker, vilket vissa vill ha av princip."),
                ("Tömer en VPN iPhone-batteriet?",
                 "En tunnel som alltid är på kostar ström, precis som varje bakgrundsanslutning. Vi "
                 "publicerar inte batterisiffror eftersom vi inte kan återskapa dem över "
                 "enheter; det vi publicerar är hastighetskostnaden för tunneln själv."),
                ("Kan jag använda en VPN på alla mina enheter?",
                 "Beror på planen: enhetsgränser går från 2 till obegränsat i tabellen, och "
                 "varje gräns står i jämförelsen nedan. Tre leverantörer här räknar inte alls."),
            ],
        },

        "android": {
            "label": "Android",
            "h1": "Bäst VPN för Android",
            "desc": ("Bästa VPN för Android 2026 — Surfshark, Proton VPN och NordVPN — valda på "
                     "användarvänlighet, integritet och pris för den bredaste "
                     "telefonplattformen."),
            "lede": ("Android ger dig mer valmöjligheter än någon annan plattform, inklusive "
                     "appar du kan läsa rad för rad. Den här guiden viktar integritet och "
                     "öppenhet därefter."),
            "intro": [
                ("Android-ekosystemet sträcker sig från en enda växel till en komplett "
                 "verktygslåda för nätverk, och skillnaden betyder mer här än på iOS eftersom "
                 "samma app ofta levereras med fler alternativ — och fler sätt att lämna "
                 "tunneln halvkonfigurerad."),
                ("Integritet bär också verklig tyngd. Android-trafik är en blandning av appar "
                 "du valde och appar du inte valde, så en loggfri policy som går att granska är "
                 "värd mer än en längre funktionslista."),
            ],
            "why": [
                ("Användarvänlighet bär 35 % i den här guiden, integritet 30 %, pris 20 %, "
                 "hastighet 10 % och streaming 5 %. Källkodsöppna appar lyfts fram i valen där "
                 "våra data registrerar dem, eftersom det på Android är skillnaden mellan "
                 "tillit och verifiering."),
            ],
            "guide_title": "Välja VPN för Android",
            "guide": [
                ("Bestäm hur mycket du vill att appen ska visa. Vissa Android-appar är en "
                 "enda växel; andra "
                 "visar protokollval, split tunneling och regler per app. Inget av dem är fel, "
                 "men den första veckan sätter vanan och en komplicerad app lämnas snart."),
                ("Kontrollera sedan licensvillkoren: månadssiffran är nästan alltid kopplad till "
                 "en flerårig avtalslängd, så läs totalen bredvid. Varje pris på den här "
                 "webbplatsen visar totalen för den avtalslängd du faktiskt köper."),
            ],
            "picks": {
                "surfshark": ("Obegränsade enheter och pris 9,6 — det näst högsta prisbetyget "
                              "av de elva, på plattformen med flest enheter."),
                "protonvpn": ("Integritet 9,7, källkodsöppna appar och en gratisnivå: "
                              "verifiering i stället för ett löfte, utan kostnad att börja."),
                "nordvpn": ("Det bästa totalbetyget i tabellen, med sex revisioner och "
                            "RAM-baserade servrar bakom appen."),
            },
            "faq": [
                ("Behöver Android-telefoner en VPN?",
                 "På mobildata, sällan. På delat wifi, ja. Android låter dig också leda en enda "
                 "app genom tunneln, vilket är användbart om du bara vill dölja en sak — men "
                 "grunderna är samma som på vilken annan plattform som helst."),
                ("Vilken Android-VPN är gratis?",
                 "Proton VPN, Windscribe och TunnelBear publicerar alla en gratisnivå. "
                 "Gratisnivåer är långsammare och mindre av design, så läs vad den fria planen "
                 "finansieras av innan du skickar något känsligt genom den."),
                ("Är en källkodsöppn Android-VPN säkrare?",
                 "Den går att verifiera i stället för att vara säkrare som standard: vem som "
                 "helst kan läsa vad appen gör, och det är precis därför vi registrerar "
                 "källkodsöppna appar som en faktakategori på varje recension i stället för att "
                 "ta det som ett betyg."),
            ],
        },

        "windows": {
            "label": "Windows",
            "h1": "Bäst VPN för Windows",
            "desc": ("Bästa VPN för Windows 2026 — ExpressVPN, NordVPN och Private Internet "
                     "Access — valda på användarvänlighet, hastighet och integritet för "
                     "skrivbordet."),
            "lede": ("På en dator måste VPN:n samexistera med allt annat du kör — spel, samtal, "
                     "filöverföringar — utan att bli det du bråkar med."),
            "intro": [
                ("Windows är där de flesta först möter en VPN och där mest kan gå fel: ett "
                 "kill switch som blockerar ditt arbete, en split tunnel du inte avsåg att "
                 "ställa in, en app som startar med Windows och tyst återansluter hela dagen."),
                ("Det är också där hastighet betyder mest, eftersom en datorsanslutning oftast "
                 "är den snabba i hushållet och tunneln är mest synlig där. Därför viktar den "
                 "här guiden hastighet på en fjärdedel av beslutet."),
            ],
            "why": [
                ("Användarvänlighet bär 35 %, hastighet 25 %, integritet 25 %, pris 10 % och "
                 "streaming 5 %. Ett av de tre valen är gjort just för att det ger mer kontroll "
                 "till dem som vill ha det — och är märkt som sådant i stället för dolt bakom "
                 "ett nybörjarvänligt standardval."),
            ],
            "guide_title": "Vad du ska kontrollera i en Windows-VPN-app",
            "guide": [
                ("Börja med standardvalen. En bra Windows-app ansluter förnuftigt, blockerar "
                 "läckor om tunneln faller och kräver aldrig att du blir nätverksingenjör "
                 "för att komma online. Avancerade kontroller ska finnas när du vill ha dem, "
                 "osynliga när du inte gör det."),
                ("Titta sedan på det som omger appen: om den kan starta med Windows, om den "
                 "överlever sömnläge, och hur många enheter licensen täcker. Det är de tre "
                 "sakerna människor upptäcker vecka två i stället för på försäljningssidan."),
            ],
            "picks": {
                "expressvpn": ("Användarvänlighet 9,5 och hastighet 9,6 — det högsta "
                               "hastighetsbetyget här, i en datorapp som inte stör, i toppen av sitt "
                               "prisintervall."),
                "nordvpn": ("Det bästa totalbetyget här, med 10 samtidiga enheter och "
                            "RAM-baserad infrastruktur bakom klienten."),
                "private-internet-access": ("Källkodsöppna Windows-appar, obegränsade enheter "
                                            "och en uppsättning kontroller för dem som vill "
                                            "ha dem."),
            },
            "faq": [
                ("Behöver jag en VPN på Windows hemma?",
                 "På din egen anslutning, oftast inte. På ett delat eller arbetsnätverk, på "
                 "hotellets wifi, eller om du inte vill att din adress ska synas för de sidor "
                 "du besöker, ja. Det är ett verktyg med ett bestämt jobb, inte en allmän "
                 "uppgradering."),
                ("Saktar en VPN ner Windows?",
                 "Kryptering och routing kostar genomströmning — det är fysik, och vi låtsas "
                 "inte att det är något annat. Hastighetskomponenten i tabellen är vår "
                 "publicerade mätning av den kostnaden, från 9,6 ned till 7,6 i den här "
                 "listan."),
                ("Ska VPN:n starta med Windows?",
                 "Om du vill ha skydd innan du märker att du behöver det, ja. Om du hellre "
                 "bestämmer per session, lämna den manuell. Kontrollera i alla fall att kill "
                 "switch beter sig som du förväntar dig innan du litar på den."),
            ],
        },

        "mac": {
            "label": "Mac",
            "h1": "Bäst VPN för Mac",
            "desc": ("Bästa VPN för Mac 2026 — ExpressVPN, NordVPN och Proton VPN — valda på "
                     "användarvänlighet, integritet och hastighet för macOS."),
            "lede": ("Mac-användare vill oftast att appen ska hålla sig ur vägen och att "
                     "påståendena ska gå att kontrollera. Den här guiden viktar båda."),
            "intro": [
                ("En VPN på Mac lever i menyraden och bedöms utifrån hur lite den avbryter: ett "
                 "tydligt läge, en snabb anslutning och ingen demon som överraskar dig efter en "
                 "uppdatering."),
                ("Integritet vikts upp till en fjärdedel här eftersom plattformens publik "
                 "tendrar att bry sig om det — revisioner, jurisdiktion och källkodsöppna "
                 "klienter registreras per leverantör på den här webbplatsen, och alla tre val "
                 "får 9,2 eller högre på den komponenten."),
            ],
            "why": [
                ("Användarvänlighet bär 40 % i den här guiden, integritet 25 %, hastighet 20 %, "
                 "pris 10 % och streaming 5 %. Vikterna visas nedan och är det enda som skiljer "
                 "den här sidan från vår totalrankning."),
            ],
            "guide_title": "Välja VPN för macOS",
            "guide": [
                ("Kontrollera hur appen beter sig över uppdateringar och sömnläge — en VPN som "
                 "tyst slutar skydda efter en systemuppdatering är värre än ingen, eftersom du "
                 "inte märker det. Varje recension här registrerar om leverantören publicerar "
                 "revisioner och hur gamla de är."),
                ("Sedan de vanliga frågorna: hur många enheter, vad avtalslängden faktiskt "
                 "kostar och hur lång tid du har att ändra dig. Svaren finns i tabellen nedan, "
                 "bredvid det betyg som fick varje leverantör att hamna på den här sidan."),
            ],
            "picks": {
                "expressvpn": ("Användarvänlighet 9,5 och hastighet 9,6: den minst störande "
                               "snabba appen i tabellen, till sitt vanliga premiumpris."),
                "nordvpn": ("Det bästa totalbetyget här, sex revisioner och RAM-baserade servrar "
                            "— påståendet upprätthålls i hårdvara snarare än i policy."),
                "protonvpn": ("Integritet 9,7 med schweizisk jurisdiktion och källkodsöppna "
                              "klienter, för en Mac-ägare som hellre läser än litar."),
            },
            "faq": [
                ("Behöver macOS en VPN?",
                 "Inte på din egen anslutning. På vilket nätverk som helst du inte kontrollerar, "
                 "och om du inte vill att din adress ska synas för de sidor du besöker, ja. "
                 "Tunneln gör ett jobb bra och rättar inte något annat."),
                ("Använder Mac-VPN:er mer batteri?",
                 "En tunnel som alltid är på kostar ström på vilken bärbar dator som helst. Vi "
                 "publicerar inte batterisiffror, eftersom de beror på hårdvara och användning "
                 "vi inte kan återskapa — hastighetskomponenten är siffran vi kan stå för."),
                ("Kan jag använda min Windows-VPN-licens på en Mac?",
                 "Oftast ja: alla elva leverantörer här täcker flera plattformar på en "
                 "prenumeration, och det är enhetsgränsen — inte operativsystemet — som du ska "
                 "kontrollera. Varje gräns finns i jämförelsetabellen nedan."),
            ],
        },

        "routers": {
            "label": "routrar",
            "h1": "Bäst VPN för routrar",
            "desc": ("Bästa VPN att köra på en router 2026 — NordVPN, ExpressVPN och Surfshark "
                     "— valda på hastighet, installationsmöda och de enhetsplatser de sparar."),
            "lede": ("En VPN på routern skyddar alla enheter i hushållet på en gång, även de som "
                     "inte kan köra en app. Kompromissen är hastighet och installation, och den "
                     "här guiden viktar båda."),
            "intro": [
                ("Fördelen är enkel: en konfiguration täcker tv:n, konsolen, skrivaren och "
                 "gäst-wifin, och ingen i hushållet behöver komma ihåg att slå på något. "
                 "Routern tar en av planens enhetsplatser, och det är precis därför "
                 "obegränsade planer ändrar räkneexemplet."),
                ("Kostnaden är genomströmning — varje paket krypteras på väg ut — och mödan att "
                 "konfigurera det en gång ordentligt. Varje leverantör här erbjuder OpenVPN, "
                 "nio erbjuder också WireGuard, och ExpressVPN levererar Lightway i stället; "
                 "det som skiljer är hur mycket hastighet som överlever."),
            ],
            "why": [
                ("Hastighet bär 35 % i den här guiden, användarvänlighet 30 %, integritet 20 %, "
                 "pris 10 % och streaming 5 %. Användarvänlighet vikts upp eftersom kravet bara "
                 "är att det fungerar efter att du konfigurerat det en gång — och det är "
                 "lättare att lova än att leverera."),
            ],
            "guide_title": "Installera VPN på din router",
            "guide": [
                ("Bekräfta först vilken firmware. Stöd för OpenVPN eller WireGuard — eller "
                 "firmware som lägger till det — är kravet; varje leverantör här erbjuder "
                 "OpenVPN, nio lägger till WireGuard, och frågan är vilken din router hanterar "
                 "bättre."),
                ("Planera sedan enheterna. En router räknas som en anslutning, så hushållets "
                 "telefoner och bärbara datorer kan köra på samma prenumeration som routern "
                 "själv — eller på en separat prenumeration om du bara vill ha tunneln i "
                 "vardagsrumsskärmen."),
            ],
            "picks": {
                "nordvpn": ("Hastighet 9,4 med 111 länder och 10 enhetsplatser — det starkaste "
                            "helhetsvalet när hela huset sitter bakom den."),
                "expressvpn": ("Hastighet 9,6, det högsta vi publicerar, och det är vad en router "
                               "behöver mest när varje paket ska krypteras."),
                "surfshark": ("Obegränsade enheter och pris 9,6 — en prenumeration täcker "
                              "routern och allt annat utan att räkna."),
            },
            "faq": [
                ("Vilken VPN fungerar bäst på en router?",
                 "Vilken som helst som erbjuder OpenVPN — tio av de elva leverantörerna här gör det — "
                 "eller WireGuard, som nio av dem också har. Det som skiljer dem åt är hur mycket "
                 "hastighet som överlever den extra krypteringen, och därför viktar den här "
                 "guiden hastighet på 35 %: NordVPN, ExpressVPN och Surfshark leder på den "
                 "kombinationen."),
                ("Saktar en router-VPN ner mitt internet?",
                 "Ja, något — varje paket krypteras, oftast på hårdvara utan dedikerad "
                 "krypteringschip. Storleken på nedgången beror på routern lika mycket som på "
                 "leverantören, och därför publicerar vi en hastighetskomponent i stället för "
                 "ett löfte."),
                ("Behöver jag fortfarande en VPN-app i min telefon?",
                 "Inte för hemnätverket, om routerns tunnel är på. Ha en app för mobildata och "
                 "för vilket nätverk som helst borta hemifrån — routern skyddar bara trafik som "
                 "går genom den, och din telefon lämnar huset med dig."),
            ],
        },
    },
}


# Hub copy for the informational section (/vpn-explained/). The article bodies
# themselves live in assets/data/explained.json, one entry per slug with both
# languages inside it, so hreflang pairing cannot drift.
EXPLAINED_HUB = {
    "en": {
        "h1": "VPN Explained: What It Does and What It Doesn't",
        "desc": "Plain answers to the questions people ask before buying a VPN: what it "
                "does, what it hides, whether it slows you down, and what it never "
                "protects you from.",
        "lede": "Ten explainers, written the same way the comparison is — what is "
                "verifiable, what is marketing, and where the limits are.",
        "intro": [
            "Most VPN writing exists to sell a subscription, so the same three sentences "
            "get repeated until they sound like physics. A VPN encrypts the connection "
            "between your device and the server you chose, and it makes the rest of the "
            "internet see that server's address instead of your own. Everything past that "
            "sentence is context: what your internet provider can still observe, what the "
            "VPN provider itself logs, and which threats were never on the table.",
            "These pages answer one question each, in the order a reader actually asks "
            "them. Where a claim can be checked, we say what to check it against — the "
            "published scores ({{compare|the published comparison}}), the providers' own "
            "audit reports, or the plain architecture of the protocol. Where we are "
            "guessing, we write that we are guessing, and the full method sits at "
            "{{method|how we test}}.",
        ],
        "faq": [
            ("Are these VPN guides independent?",
             "The guides use the same eleven providers and the same five published components "
             "as the comparison, and the weights are printed on {{method|the method page}}. The site "
             "earns a commission if you subscribe through its links; no provider can pay to "
             "appear in an explainer, and the affiliate links are labelled everywhere they "
             "appear."),
            ("Do you test the claims in these articles?",
             "Where testing is possible we say what was measured. The speed component is an "
             "architectural estimate rather than our own throughput benchmark, and the "
             "articles say so wherever speed comes up — see {{method|how we test}} for "
             "the full method and its limits."),
        ],
    },
    "sv": {
        "h1": "VPN förklarat: vad den gör och vad den inte gör",
        "desc": "Svar på frågorna folk ställer innan de köper en VPN: vad tjänsten gör, "
                "vad den döljer, om den saktar ner surfen och vad den aldrig skyddar dig "
                "mot.",
        "lede": "Tio förklaringar, skrivna på samma sätt som jämförelsen — vad som går "
                "att verifiera, vad som är marknadsföring och var gränserna går.",
        "intro": [
            "Det mesta som skrivs om VPN finns till för att sälja ett abonnemang, och därför "
            "upprepas samma tre meningar tills de låter som fysik. En VPN krypterar "
            "anslutningen mellan din enhet och den server du valt, och får resten av "
            "internet att se serverns adress i stället för din egen. Allt efter den meningen "
            "är sammanhang: vad din internetleverantör ändå kan observera, vad VPN-leverantören "
            "själv loggar och vilka hot som aldrig stod på bordet.",
            "Här svaras en fråga per sida, i den ordning en läsare faktiskt ställer dem. När "
            "ett påstående går att kontrollera säger vi vad du ska kontrollera det mot — "
            "de publicerade betygen ({{compare|jämförelsen}}), leverantörernas egna "
            "revisionsrapporter eller protokollets upplägg. När vi gissar skriver vi att "
            "vi gissar, och hela metoden finns på {{method|hur vi testar}}.",
        ],
        "faq": [
            ("Är de här VPN-guiderna oberoende?",
             "Guiderna använder samma elva leverantörer och samma fem publicerade komponenter "
             "som jämförelsen, och vikterna finns på {{method|metodsidan}}. Webbplatsen tar provision om "
             "du prenumererar via dess länkar; ingen leverantör kan betala för att komma med "
             "i en förklaring, och affiliate-länkarna är märkta överallt där de förekommer."),
            ("Testar ni påståendena i de här artiklarna?",
             "Där test går att göra skriver vi vad som mättes. Hastighetskomponenten är en "
             "arkitekturuppskattning och inte vår egen genomströmmningsmätning, och det står "
             "i artiklarna var hastighet nämns — se {{method|så testar vi}} för hela metoden "
             "och dess gränser."),
        ],
    },
}


def t(key: str, lang: str) -> str:
    return S[key][lang]
