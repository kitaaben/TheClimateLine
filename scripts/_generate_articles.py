import json, os
from pathlib import Path
from datetime import datetime

ARTICLES_DIR = Path(r'C:\TheClimateLine\articles')
ARTICLES_JSON = Path(r'C:\TheClimateLine\articles.json')

ARTICLES = [
    {
        "slug": "ocean-acidification-the-silent-threat",
        "title": "Ocean Acidification: The Silent Threat Beneath the Waves",
        "summary": "CO\u2082 is not just warming the planet \u2014 it is acidifying the oceans. Discover how this hidden crisis threatens marine life, food security, and the climate system.",
        "badge": "\ud83c\udf0a Ocean Science"
    },
    {
        "slug": "climate-migration-global-displacement",
        "title": "Climate Migration: The Coming Wave of Global Displacement",
        "summary": "As seas rise and lands dry, millions will be forced to move. Explore the causes, scale, and human cost of climate-driven migration.",
        "badge": "\ud83c\udf0d Global Impact"
    },
    {
        "slug": "deforestation-climate-change",
        "title": "Deforestation and Climate Change: How Forest Loss Fuels the Crisis",
        "summary": "Forests are our greatest natural ally against climate change \u2014 and we are destroying them. Learn why protecting forests is essential to a stable climate.",
        "badge": "\ud83c\udf33 Forests"
    },
    {
        "slug": "climate-change-human-health",
        "title": "Climate Change and Human Health: The Growing Crisis",
        "summary": "From heat stress to infectious disease, climate change is reshaping global health. Understand the risks and what can be done to protect communities.",
        "badge": "\ud83c\udf0e Health"
    },
    {
        "slug": "climate-policy-global-action",
        "title": "Climate Policy: The Global Fight for a Livable Planet",
        "summary": "Carbon pricing, Paris pledges, COP summits \u2014 how international policy shapes our climate future. A guide to the mechanisms driving global action.",
        "badge": "\ud83c\udfdb\ufe0f Policy"
    }
]

def make_og_description(summary):
    if len(summary) + 3 <= 160:
        return summary
    return summary[:157] + "..."

def generate_html(a):
    slug = a["slug"]
    title = a["title"]
    summary = a["summary"]
    badge = a["badge"]
    og_desc = make_og_description(summary)
    date = datetime.now().strftime("%B %d, %Y")
    url = f"https://theclimateline.pages.dev/articles/{slug}.html"
    img = f"https://theclimateline.pages.dev/media/articles/{slug}.png"
    
    # External links used in content
    links = {
        "ipcc": "<a href='https://ipcc.ch' target='_blank' rel='noopener'>IPCC</a>",
        "nasa": "<a href='https://nasa.gov' target='_blank' rel='noopener'>NASA</a>",
        "noaa": "<a href='https://noaa.gov' target='_blank' rel='noopener'>NOAA</a>",
        "wmo": "<a href='https://wmo.int' target='_blank' rel='noopener'>WMO</a>",
        "unep": "<a href='https://unep.org' target='_blank' rel='noopener'>UNEP</a>",
        "iea": "<a href='https://iea.org' target='_blank' rel='noopener'>IEA</a>",
        "worldbank": "<a href='https://worldbank.org' target='_blank' rel='noopener'>World Bank</a>",
        "nature": "<a href='https://nature.com' target='_blank' rel='noopener'>Nature</a>",
        "science": "<a href='https://science.org' target='_blank' rel='noopener'>Science</a>",
        "imf": "<a href='https://imf.org' target='_blank' rel='noopener'>IMF</a>",
    }
    
    HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <meta name='description' content='{og_desc}'>
  <title>{title} — The Climate Line</title>
    <meta property="og:title" content="{title}">
  <meta property="og:description" content="{og_desc}">
  <meta property="og:image" content="{img}">
  <meta property="og:url" content="{url}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="The Climate Line">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{og_desc}">
  <meta name="twitter:image" content="{img}">
  <link rel='stylesheet' href='../css/style.css'>
  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "description": "{og_desc}",
  "image": "{img}",
  "author": {{
    "@type": "Organization",
    "name": "The Climate Line",
    "url": "https://theclimateline.pages.dev"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "The Climate Line",
    "logo": {{
      "@type": "ImageObject",
      "url": "https://theclimateline.pages.dev/media/hero/hero-1.png"
    }}
  }},
  "datePublished": "{date_str}",
  "dateModified": "{date_str}"
}}
  </script>
  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "The Climate Line",
  "url": "https://theclimateline.pages.dev",
  "logo": "https://theclimateline.pages.dev/media/hero/hero-1.png",
  "sameAs": [
    "https://www.youtube.com/@theclimateline"
  ],
  "description": "Making climate science accessible, one story at a time."
}}
  </script>
  <script type="application/ld+json">
  </script>
</head>
<body>
  <nav>
    <div class='nav-inner'>
      <a href='../index.html' class='nav-logo'>TheClimateLine</a>
      <div class='nav-right'>
        <a href='../index.html#articles'>Articles</a>
        <a href='../index.html#updates'>Updates</a>
        <a href='https://www.youtube.com/@theclimateline' target='_blank' rel='noopener'>YouTube</a>
      </div>
    </div>
  </nav>

  <section class='article-page-hero'>
    <div class='section-inner'>
      <div class='hero-badge'>{badge}</div>
      <h1>{title}</h1>
      <div class='article-meta'>
        <span>{date}</span>
        <span>·</span>
        <span>Article</span>
        <span>·</span>
        <span>The Climate Line</span>
      </div>
    </div>
  </section>

  <article class='article-content'>
    {content}
  </article>

  <div class='article-nav'>
    <a href='../index.html'>\u2190 Back to Articles</a>
    <a href='../index.html#updates'>All Articles \u2192</a>
  </div>

  <footer>
    <div class='footer-inner'>
      <div class='footer-col'>
        <h4>TheClimateLine</h4>
        <p>Making climate science accessible, one story at a time.</p>
      </div>
      <div class='footer-col'>
        <h4>Explore</h4>
        <a href='../index.html'>Home</a>
        <a href='../index.html#articles'>Articles</a>
        <a href='../index.html#updates'>Updates</a>
      </div>
      <div class='footer-col'>
        <h4>Connect</h4>
        <a href='https://www.youtube.com/@theclimateline' target='_blank' rel='noopener'>YouTube</a>
      </div>
    </div>
    <div class='footer-bottom'>
      <span>&copy; 2026 The Climate Line</span>
    </div>
  </footer>

  <script src='../js/media-list.js'></script>
  <script src='../js/channel-videos.js'></script>
  <script src='../js/articles.js'></script>
  <script src='../js/main.js'></script>
</body>
</html>'''
    
    return HTML_TEMPLATE

print("Ready to generate. Use task agents to create the article content.")
