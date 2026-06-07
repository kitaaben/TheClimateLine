#!/usr/bin/env python3
"""Batch-apply SEO/GEO optimizations to all articles: OG tags, schema, meta, author."""
import json, re
from datetime import datetime
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
ARTICLES_DIR = PROJECT / "articles"
JSON_PATH = PROJECT / "articles.json"
BASE_URL = "https://theclimateline.pages.dev"
SITE_NAME = "The Climate Line"

data = json.loads(JSON_PATH.read_text(encoding="utf-8"))

META_DESCRIPTIONS = {
    "rising-temperatures-global-warming": "Global temperatures have risen 1.2°C — here's what the data shows and why every fraction of a degree matters. Learn the science behind rising temperatures and what we can do.",
    "rising-sea-levels-coastal-crisis": "Sea levels are rising faster than ever — 3.6mm per year. Discover how coastal cities from Miami to Mumbai are being reshaped by the encroaching ocean.",
    "heatwaves-climate-crisis": "Heatwaves kill more people than hurricanes and floods combined. Learn why extreme heat is the deadliest natural disaster and how to protect your community.",
    "will-we-be-part-of-the-climate-solution": "The defining question of our era: will we be part of the climate solution? Explore how individual action and civic engagement can shape a sustainable future.",
    "act-now-prevent-climate-catastrophe": "The next decade is the critical window for climate action. Learn what immediate steps we must take to prevent catastrophic warming and secure our future.",
    "climate-catastrophe-time-to-act-now": "The window for climate action is closing fast. Discover why the difference between 1.5°C and 2°C means life or death for ecosystems and communities worldwide.",
    "earths-climate-crisis-beyond-1c": "We've passed 1°C of warming — here's what the data shows. Learn about the measurable damage already underway and why every fraction of a degree matters.",
    "make-or-break-decade-climate-food": "Climate change threatens global food systems. Discover how regenerative agriculture and technology can feed a warming world before it's too late.",
    "carbon-lockout-window": "Every new power plant built today locks in decades of emissions. Learn why the carbon lockout window is closing and how clean energy can win the race.",
    "4c-catastrophe-our-final-warning": "A 4°C warmer world means cascading tipping points and mass extinction. Discover why avoiding this future requires immediate, transformative climate action.",
    "climate-crisis-time-to-act": "The science is clear and the solutions exist. Learn why the gap between knowledge and action is the biggest barrier to solving the climate crisis.",
    "climate-catastrophe-in-antarctica": "Antarctica is melting faster than predicted. Discover how the Thwaites 'Doomsday Glacier' threatens global sea levels and what scientists are watching.",
    "arctic-meltdown-our-final-warning": "The Arctic is warming 4x faster than the global average. Learn about sea ice death spirals, permafrost carbon bombs, and what this means for the planet.",
    "methane-emissions-threaten-our-planet": "Methane is 80x more potent than CO2 over 20 years. Discover why cutting methane emissions is the fastest lever we have to slow global warming today.",
    "methane-leaks-the-untold-crisis": "Satellite data reveals methane leaks are 70% higher than reported. Learn about super-emitters and the cheapest climate fix we're failing to deploy.",
    "climate-science-basics": "Understand the greenhouse effect, feedback loops, and climate tipping points in plain language. Your complete guide to the science of climate change.",
    "renewable-energy-solutions": "Solar, wind, and battery storage are cheaper than fossil fuels. Discover how renewable energy is powering a sustainable future — the technology, economics, and jobs.",
    "climate-news-2026": "Stay informed on the biggest climate developments of 2026. From policy milestones to technology breakthroughs — what's happening and what comes next.",
}

FAQ_CONTENT = {
    "rising-temperatures-global-warming": [
        ("How much has the Earth warmed?", "The Earth's average surface temperature has risen by approximately 1.2°C since the late 19th century, with the rate of warming accelerating sharply since the 1970s."),
        ("What causes global temperatures to rise?", "The primary cause is the accumulation of greenhouse gases from burning fossil fuels. CO2 concentrations have risen from 280 ppm to over 420 ppm — a level not seen in 4 million years."),
        ("Why does the Arctic warm faster?", "The Arctic warms nearly four times faster than the global average due to ice-albedo feedback: as ice melts, darker ocean water absorbs more sunlight, causing more warming."),
        ("Can we still stop global warming?", "Yes — rapidly reducing emissions through renewable energy, energy efficiency, and forest protection can limit warming. Every fraction of a degree we prevent matters."),
        ("What happens if we reach 3°C of warming?", "At 3°C, most ecosystems would be fundamentally reshaped, with widespread crop failures, mass migration, and cascading tipping points becoming likely."),
    ],
    "rising-sea-levels-coastal-crisis": [
        ("How much have sea levels risen?", "Global mean sea level has risen by 21-24 cm since 1880, with the rate more than doubling from 1.4 mm/year to 3.6 mm/year today."),
        ("What causes sea levels to rise?", "Two main drivers: thermal expansion (ocean water expands as it warms) and melting land-based ice from Greenland and Antarctica."),
        ("Which cities are most at risk?", "Jakarta, Lagos, Shanghai, Mumbai, Bangkok, Miami, New York, and Charleston face the highest flood risk from rising seas."),
        ("Can we stop sea level rise?", "Some rise is already locked in, but rapid emission reductions can slow the rate significantly — from 2 meters to 0.5 meters by 2100."),
        ("What is the 'Doomsday Glacier'?", "Thwaites Glacier in Antarctica is called the Doomsday Glacier because its collapse could raise sea levels by 2+ feet and unlock 10 more feet from the ice it restrains."),
    ],
    "heatwaves-climate-crisis": [
        ("Why are heatwaves called the silent killer?", "Heatwaves kill more people than hurricanes, tornadoes, and floods combined, but their impacts are less visually dramatic, making them easy to underestimate."),
        ("How does climate change affect heatwaves?", "Climate change has made heatwaves longer, hotter, and more frequent. A 2003-level European heatwave is now 10 times more likely due to global warming."),
        ("What is the urban heat island effect?", "Cities can be several degrees hotter than surrounding areas due to concrete, asphalt, and lack of tree cover, disproportionately affecting low-income neighborhoods."),
        ("How can communities protect against extreme heat?", "Early warning systems, cooling centers, tree canopy, green roofs, and reflective surfaces can reduce heatwave mortality by up to 80 percent."),
        ("What is the wet-bulb temperature limit?", "A wet-bulb temperature above 35°C makes human survival impossible even with shade and water, as the body cannot cool itself through sweating."),
    ],
    "will-we-be-part-of-the-climate-solution": [
        ("Can individual action really make a difference?", "Yes — high-impact lifestyle changes like plant-based diets and renewable energy can reduce individual emissions by up to 9 tonnes of CO2 per year."),
        ("What is the most impactful climate action I can take?", "Using your voice and your vote. Demand-side mitigation strategies could reduce global emissions by 40-70% by 2050 through collective political action."),
        ("Is voting really effective for climate action?", "Yes — electing climate-conscious leaders who implement carbon pricing, clean energy mandates, and public transit investment creates systemic change."),
        ("How can I reduce my carbon footprint?", "Switch to renewable energy, adopt a plant-based diet, avoid air travel, electrify your home and transport, and support climate-friendly policies."),
        ("What is the single most important thing to do?", "Talk about climate change. 63% of Americans rarely discuss it, yet those who do are far more likely to support ambitious policy."),
    ],
    "act-now-prevent-climate-catastrophe": [
        ("How much time do we have to act?", "Emissions must peak before 2025 and decline 43% by 2030 to limit warming to 1.5°C. The next decade is the critical window for climate action."),
        ("What are climate tipping points?", "Sixteen major tipping elements exist in the climate system, including the Greenland ice sheet and Amazon rainforest. Crossing them triggers self-accelerating warming."),
        ("How much will climate change cost the economy?", "Swiss Re estimates climate change could shave up to 18% off global GDP by 2050 if emissions remain unchecked."),
        ("What does immediate climate action look like?", "Triple renewable deployment, electrify transportation, adopt green hydrogen for industry, regenerative agriculture, and halt deforestation simultaneously."),
        ("Is the clean energy transition affordable?", "It requires roughly $4 trillion annually by 2030 — far less than the economic devastation of a 3°C+ world. It's the most prudent investment humanity can make."),
    ],
    "climate-catastrophe-time-to-act-now": [
        ("What is the remaining carbon budget?", "The Global Carbon Project estimates the remaining carbon budget for 1.5°C will be exhausted within 7-10 years at current emission rates."),
        ("Is the Amazon rainforest still a carbon sink?", "Parts of the Amazon now emit more CO2 than they absorb due to deforestation and drought, marking a dangerous tipping point."),
        ("How many times have coral reefs bleached?", "The Great Barrier Reef has experienced its 4th global bleaching event in 2024, with over 60% of reef systems impacted worldwide."),
        ("What technologies can solve climate change?", "Solar, wind, battery storage, electric vehicles, green steel, and sustainable aviation fuels already exist and are dropping in cost faster than predicted."),
        ("What is the biggest barrier to climate action?", "Political will and social mobilization. The technologies exist — what's lacking is the collective determination to deploy them at emergency speed."),
    ],
    "earths-climate-crisis-beyond-1c": [
        ("When did the Earth pass 1°C of warming?", "Global average temperatures crossed 1°C above pre-industrial levels around 2017 and have remained above it since."),
        ("What impacts have we already seen at 1.2°C?", "Sea levels up 20 cm, extreme precipitation intensified by 7% per 1°C, heatwaves 3x more frequent, and widespread coral bleaching."),
        ("What's the difference between 1.5°C and 2°C?", "420 million more people exposed to extreme heat, 10 million more affected by sea-level rise, and loss of virtually all coral reefs vs some surviving."),
        ("Who is most affected by 1°C of warming?", "The Arctic (warming 4x faster), small island states (existential sea-level threat), and agricultural zones in Africa and South Asia (food security)."),
        ("Can we still stay below 1.5°C?", "Yes — it remains technically achievable, but the emissions gap between current pledges and what's required gives us less than a decade to reverse course."),
    ],
    "make-or-break-decade-climate-food": [
        ("How does climate change affect crop yields?", "For every 1°C of warming, wheat yields decline by 6%, rice by 3%, and maize by 7%. Multiple breadbasket failures are becoming more common."),
        ("What is regenerative agriculture?", "Practices like cover cropping, no-till farming, agroforestry, and rotational grazing rebuild soil carbon, improve water retention, and boost long-term yields."),
        ("How much land do livestock use?", "Plant-based and cultivated meat alternatives require 75-95% less land and water than conventional livestock, freeing up land for ecosystem restoration."),
        ("What is precision agriculture?", "Using satellite imagery, soil sensors, and AI to apply water and fertilizer with surgical accuracy — projected to reach $43 billion by 2030."),
        ("How much must agricultural emissions drop?", "Agricultural emissions must drop 30-40% by 2035 to stay aligned with the 1.5°C pathway — requiring dietary shifts, halting deforestation, and clean fertilizer production."),
    ],
    "carbon-lockout-window": [
        ("What is carbon lock-in?", "Once fossil fuel infrastructure is built, it operates for 30-50 years, locking in emissions regardless of future climate goals."),
        ("How much investment is at stake?", "Over $11 trillion in new power sector investment is expected between 2025 and 2050. Every dollar spent on fossil fuels lengthens our carbon dependence."),
        ("What are stranded assets?", "$1.4 trillion in fossil fuel assets could be stranded under a Paris-aligned scenario — a systemic financial risk comparable to the 2008 mortgage crisis."),
        ("How much cheaper is renewable energy?", "Solar costs have fallen 90% and wind 70% since 2010. In most markets, new solar or wind is cheaper than running existing coal or gas plants."),
        ("What policies can accelerate carbon lockout?", "Carbon pricing (covering 25% of global emissions), green bank mandates, and clean procurement standards can accelerate the transition."),
    ],
    "4c-catastrophe-our-final-warning": [
        ("What would a 4°C world look like?", "A 4°C world means extreme heat across most land areas, crop collapses (maize down 40%), and large regions becoming uninhabitable during summer."),
        ("What climate tipping points would be crossed?", "Amazon rainforest dieback, Greenland/West Antarctic ice sheet collapse, and massive permafrost thaw releasing methane — all self-accelerating."),
        ("How many species face extinction at 4°C?", "A 2023 study in Science Advances found that 29% of species could face extinction at 4°C warming — a sixth mass extinction."),
        ("Can we still avoid 4°C warming?", "Yes — emissions must peak this decade and decline 50% by 2035. This means retiring coal, electrifying transport, halting deforestation, and deploying carbon removal."),
        ("How many people could be displaced?", "Climate migration could displace 200 million to 1 billion people by 2050 under high-warming scenarios, triggering unprecedented geopolitical instability."),
    ],
    "climate-crisis-time-to-act": [
        ("What does the IPCC say about climate action?", "The IPCC's 6th Assessment Report states emissions must peak before 2025 and decline 43% by 2030 to limit warming to 1.5°C."),
        ("Why isn't the world acting faster?", "Fossil fuel subsidies hit a record $7 trillion in 2025. Cognitive biases like present bias and vested interests from incumbent industries slow progress."),
        ("Is 1.5°C still achievable?", "While some scientists consider 1.5°C all but unattainable, every fraction of a degree matters — 1.5°C vs 2°C means 10M fewer displaced by sea level rise."),
        ("What progress is being made?", "Renewable capacity broke records in 2025, EV sales grew 35%, and Amazon deforestation fell 40%. Clean tech growth feeds on itself."),
        ("What can I personally do?", "Vote for climate leaders, divest from fossil fuels, electrify your home, reduce food waste, and most importantly — talk about climate change."),
    ],
    "climate-catastrophe-in-antarctica": [
        ("How fast is Antarctica melting?", "Antarctica has shed roughly 3 trillion tons of ice since 1992, and the rate of loss has tripled in the last decade."),
        ("What is the Thwaites Glacier?", "The Thwaites Glacier (Doomsday Glacier) spans the size of Florida and acts as a dam for the West Antarctic Ice Sheet. Its collapse could raise seas by 2+ feet."),
        ("How does ice melt contribute to sea level rise?", "Warm ocean water undercuts glaciers along their grounding lines, accelerating melting. This basal melting was underestimated in earlier climate models."),
        ("What did climate models miss about Antarctica?", "Most models failed to capture basal melting physics. New models including ice-cliff collapse double projected sea level contributions by 2100."),
        ("Can we stop Antarctic ice loss?", "Even with net-zero emissions, ocean heat already stored will continue to melt ice for decades. Aggressive mitigation reduces the risk of crossing tipping points."),
    ],
    "arctic-meltdown-our-final-warning": [
        ("How fast is the Arctic warming?", "The Arctic is warming approximately four times faster than the global average — parts have already exceeded 3°C of warming."),
        ("What is happening to Arctic sea ice?", "Sea ice extent has declined 13% per decade since 1979. The oldest multi-year ice has vanished. An ice-free Arctic summer could arrive by the 2030s."),
        ("What is the permafrost carbon bomb?", "Permafrost contains 1,500 billion tons of organic carbon — twice the amount in the atmosphere. Thawing could add 50-100 billion tons of CO2-equivalent by 2100."),
        ("How does Arctic meltdown affect global weather?", "Arctic warming weakens the polar vortex, causing more extreme weather events across the Northern Hemisphere — cold spells, heatwaves, and atmospheric blocking."),
        ("How much is Greenland contributing to sea level rise?", "Greenland lost 500 billion tons of ice in 2019 alone and currently contributes roughly 0.7 mm per year to global sea level rise."),
    ],
    "methane-emissions-threaten-our-planet": [
        ("Why is methane more dangerous than CO2?", "Methane is 80 times more potent than CO2 over a 20-year timeframe, making it the most powerful lever to slow near-term warming."),
        ("Where does methane come from?", "Human activities account for 60% of emissions: agriculture (livestock, rice), fossil fuel operations (venting, leaks), and landfills."),
        ("How much has atmospheric methane increased?", "Atmospheric methane has more than than doubled since pre-industrial times and is rising at its fastest rate on record."),
        ("Can cutting methane really make a difference?", "Yes — full implementation of existing technologies could cut emissions 45% by 2030, avoiding nearly 0.3°C of warming by 2045."),
        ("What is the Global Methane Pledge?", "Launched at COP26, over 150 nations committed to cutting methane emissions 30% by 2030. Current policies fall far short of that target."),
    ],
    "methane-leaks-the-untold-crisis": [
        ("How much methane leaks from oil and gas?", "The IEA estimates oil and gas operations emitted over 80 million tonnes of methane in 2024 — enough to meet the entire EU's natural gas demand."),
        ("What are super-emitters?", "Just 5% of oil and gas facilities are responsible for over 50% of total methane leaks. These are often from malfunctioning equipment or routine venting."),
        ("How big is the gap between reported and actual emissions?", "A 2024 Science study found actual emissions were on average 70% higher than what countries officially reported across 13 major gas-producing regions."),
        ("Can methane leaks be fixed cheaply?", "Yes — 40% of oil and gas methane emissions can be eliminated at no net cost because captured gas can be sold. It's the cheapest climate fix available."),
        ("What technologies detect methane leaks?", "Optical gas imaging cameras, aerial drone surveys, continuous monitoring sensors, and methane-detecting satellites like MethaneSAT and TROPOMI."),
    ],
    "climate-science-basics": [
        ("What is the greenhouse effect?", "Greenhouse gases (CO2, methane, water vapor) trap heat in Earth's atmosphere, keeping the planet at a livable 15°C. Without it, Earth would be -18°C."),
        ("How do humans cause climate change?", "Burning fossil fuels releases CO2 locked underground for millions of years. Deforestation removes trees that absorb CO2. This thickens the greenhouse blanket."),
        ("What are climate feedback loops?", "Ice-albedo feedback (melting ice exposes darker water that absorbs more heat), permafrost thaw (releases methane), and water vapor feedback all amplify warming."),
        ("What are climate tipping points?", "Thresholds beyond which changes become self-sustaining and irreversible — like the collapse of the Greenland ice sheet or Amazon rainforest dieback."),
        ("How much has the Earth warmed?", "Global average temperature has risen by 1.2°C since pre-industrial times. The 10 warmest years on record have all occurred since 2010."),
    ],
    "renewable-energy-solutions": [
        ("How cheap is solar energy now?", "Solar costs have dropped 90% over the past two decades, making it the cheapest source of electricity in history in many parts of the world."),
        ("Can renewables power the grid 24/7?", "Yes — combined with battery storage (costs down 80% since 2015), smart grids, and demand response, a 100% renewable grid is achievable by mid-century."),
        ("What is green hydrogen?", "Green hydrogen is produced by splitting water using renewable electricity. It can decarbonize steelmaking, shipping, and aviation — sectors hard to electrify."),
        ("How many jobs do renewables create?", "Renewable energy jobs now outnumber fossil fuel jobs in many countries, and the transition is creating millions of new jobs globally."),
        ("What is the biggest challenge for renewables?", "Intermittency is being solved by cheaper batteries and smarter grids. Political will and fossil fuel subsidies ($7 trillion in 2025) remain the real barriers."),
    ],
    "climate-news-2026": [
        ("What is the EU's Carbon Border Adjustment Mechanism?", "CBAM imposes tariffs on imported goods based on their carbon footprint, reshaping global supply chains toward cleaner production."),
        ("How is the US Inflation Reduction Act performing?", "Clean energy investments have exceeded $500 billion since passage. Solar and battery manufacturing capacity has tripled."),
        ("Has China's emissions peaked?", "China's coal consumption has plateaued as renewables meet all new electricity demand growth, suggesting emissions may have peaked earlier than expected."),
        ("What technology breakthroughs happened in 2026?", "Perovskite-silicon tandem solar cells reached 33% efficiency, iron-air batteries for 100+ hour storage moved to commercial scale, and regional electric aircraft entered service."),
        ("Is 2026 on track to be a record warm year?", "Yes — 2026 is on track to be one of the warmest years on record, with heatwaves exceeding 50°C in South Asia and severe drought in the Amazon."),
    ],
}

def parse_date_to_iso(date_str):
    for fmt in ("%B %d, %Y", "%B %d %Y"):
        try:
            return datetime.strptime(date_str.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return "2026-01-01"


def get_article_date(slug):
    for a in data:
        if a["slug"] == slug:
            return parse_date_to_iso(a["date"])
    return "2026-01-01"


def get_article_title(slug):
    for a in data:
        if a["slug"] == slug:
            return a["title"]
    return ""


def get_article_summary(slug):
    for a in data:
        if a["slug"] == slug:
            return a["summary"]
    return ""


def build_article_schema(slug, title, description, date_pub, date_mod):
    image_url = f"{BASE_URL}/media/articles/{slug}.png"
    video_id = None
    for a in data:
        if a["slug"] == slug:
            video_id = a.get("videoId")
            break
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description[:200],
        "image": image_url,
        "author": {
            "@type": "Organization",
            "name": "The Climate Line",
            "url": BASE_URL
        },
        "publisher": {
            "@type": "Organization",
            "name": "The Climate Line",
            "logo": {
                "@type": "ImageObject",
                "url": f"{BASE_URL}/media/hero/hero-1.png"
            }
        },
        "datePublished": date_pub,
        "dateModified": date_mod,
    }
    if video_id:
        schema["video"] = {
            "@type": "VideoObject",
            "name": title,
            "description": description[:200],
            "thumbnailUrl": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
            "embedUrl": f"https://www.youtube-nocookie.com/embed/{video_id}",
        }
    return json.dumps(schema, indent=2)


def build_organization_schema():
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "The Climate Line",
        "url": BASE_URL,
        "logo": f"{BASE_URL}/media/hero/hero-1.png",
        "sameAs": [
            "https://www.youtube.com/@theclimateline",
        ],
        "description": "Making climate science accessible, one story at a time."
    }, indent=2)


def build_faq_schema(slug):
    faqs = FAQ_CONTENT.get(slug, [])
    if not faqs:
        return ""
    items = []
    for q, a in faqs:
        items.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": items
    }, indent=2)


def build_faq_html(slug):
    faqs = FAQ_CONTENT.get(slug, [])
    if not faqs:
        return ""
    lines = ['    <h2>Frequently Asked Questions</h2>']
    for q, a in faqs:
        lines.append(f'    <h3>{q}</h3>')
        lines.append(f'    <p>{a}</p>')
    return '\n'.join(lines)


def optimize_article(slug):
    path = ARTICLES_DIR / f"{slug}.html"
    html = path.read_text(encoding="utf-8")

    title = get_article_title(slug)
    description = META_DESCRIPTIONS.get(slug, get_article_summary(slug))
    date_pub = get_article_date(slug)
    image_url = f"{BASE_URL}/media/articles/{slug}.png"
    article_url = f"{BASE_URL}/articles/{slug}.html"

    article_schema = build_article_schema(slug, title, description, date_pub, date_pub)
    org_schema = build_organization_schema()
    faq_schema = build_faq_schema(slug)
    faq_html = build_faq_html(slug)

    # ----- 1. Fix meta description -----
    meta_pattern = r"<meta name='description' content='[^']*'>"
    meta_replacement = f"<meta name='description' content='{description}'>"
    html = re.sub(meta_pattern, meta_replacement, html)

    # Also handle double-quoted meta descriptions
    meta_pattern2 = r'<meta name="description" content="[^"]*">'
    meta_replacement2 = f'<meta name="description" content="{description}">'
    html = re.sub(meta_pattern2, meta_replacement2, html)

    # ----- 2. Add OG and Twitter Card tags after meta description -----
    og_tags = f'''  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:image" content="{image_url}">
  <meta property="og:url" content="{article_url}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{image_url}">'''

    # Insert after the closing </head> tag or before the <link rel='stylesheet'>
    # Find the <link rel='stylesheet'> line and insert before it
    insert_point = re.search(r"<link rel='stylesheet' href='\.\./css/style\.css'>", html)
    if not insert_point:
        insert_point = re.search(r'<link rel="stylesheet" href="../css/style.css">', html)

    if insert_point:
        pos = insert_point.start()
        html = html[:pos] + og_tags + "\n  " + html[pos:]

    # ----- 3. Add schema JSON-LD before </head> -----
    schema_blocks = f'''  <script type="application/ld+json">
{article_schema}
  </script>
  <script type="application/ld+json">
{org_schema}
  </script>'''

    if faq_schema:
        schema_blocks += f'''
  <script type="application/ld+json">
{faq_schema}
  </script>'''

    html = html.replace("</head>", f"{schema_blocks}\n</head>")

    # ----- 4. Remove emoji from meta badges (hero-badge) for cleaner display -----
    # (Skip this — emojis are fine for display)

    # ----- 5. Add FAQ section before article-nav -----
    if faq_html and 'Frequently Asked Questions' not in html:
        faq_section = f'\n    {faq_html}\n'
        html = html.replace('<div class=\'article-nav\'>', f'{faq_section}\n  <div class=\'article-nav\'>')
        html = html.replace('<div class="article-nav">', f'{faq_section}\n  <div class="article-nav">')

    # ----- 6. Add author byline in article-meta -----
    author_tag = '<span>The Climate Line</span>'
    if 'The Climate Line' not in html.split('<div class=\'article-meta\'>')[1].split('</div>')[0] if '<div class=\'article-meta\'>' in html else '':
        html = html.replace('<span>Video Article</span>', '<span>Video Article</span>\n        <span>·</span>\n        <span>The Climate Line</span>')
        # Also handle double-quoted version
        # Actually let me look at the meta block more carefully
        # The meta block has three spans: date, separator, "Video Article" or "8 min read"
        # Let me just replace the closing </div> of article-meta with author tag inserted before it

    # Better approach for author: append to article-meta div
    # Find article-meta div and add author
    meta_end = re.search(r"<div class='article-meta'>.*?</div>", html, re.DOTALL)
    if meta_end and 'The Climate Line' not in meta_end.group():
        new_meta = meta_end.group().rstrip('</div>').rstrip() + '\n        <span>·</span>\n        <span>The Climate Line</span>\n      </div>'
        html = html[:meta_end.start()] + new_meta + html[meta_end.end():]

    # Also handle double-quoted version
    meta_end2 = re.search(r'<div class="article-meta">.*?</div>', html, re.DOTALL)
    if meta_end2 and 'The Climate Line' not in meta_end2.group():
        new_meta2 = meta_end2.group().rstrip('</div>').rstrip() + '\n        <span>·</span>\n        <span>The Climate Line</span>\n      </div>'
        html = html[:meta_end2.start()] + new_meta2 + html[meta_end2.end():]

    path.write_text(html, encoding="utf-8")
    print(f"  Optimized: {slug}.html")


def main():
    print("Optimizing articles...")
    for a in data:
        slug = a["slug"]
        optimize_article(slug)
    print(f"Done. {len(data)} articles optimized.")


if __name__ == "__main__":
    main()
