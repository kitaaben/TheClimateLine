from pathlib import Path
import json, re, html as html_mod
from datetime import datetime

ARTICLES_DIR = Path(r'C:\TheClimateLine\articles')
date = datetime.now().strftime("%B %d, %Y")
date_fmt = datetime.now().strftime("%Y-%m-%d")

FRAGMENTS = [
    {
        "slug": "ocean-acidification-the-silent-threat",
        "title": "Ocean Acidification: The Silent Threat Beneath the Waves",
        "summary": "CO\u2082 is not just warming the planet \u2014 it is acidifying the oceans. Discover how this hidden crisis threatens marine life, food security, and the climate system.",
        "badge": "\u2606 Ocean Science"
    },
    {
        "slug": "climate-change-human-health",
        "title": "Climate Change and Human Health: The Growing Crisis",
        "summary": "From heat stress to infectious disease, climate change is reshaping global health. Understand the risks and what can be done to protect communities.",
        "badge": "\u2606 Health"
    },
    {
        "slug": "climate-policy-global-action",
        "title": "Climate Policy: The Global Fight for a Livable Planet",
        "summary": "Carbon pricing, Paris pledges, COP summits \u2014 how international policy shapes our climate future. A guide to the mechanisms driving global action.",
        "badge": "\u2606 Policy"
    }
]

def extract_faqs(content):
    """Extract Q&A pairs from FAQ section."""
    faqs = []
    faq_section = content[content.find('<h2>Frequently Asked Questions</h2>'):]
    q_matches = re.findall(r'<h3>(.*?)</h3>\s*<p>(.*?)</p>', faq_section, re.DOTALL)
    for q, a in q_matches:
        faqs.append({
            "name": html_mod.unescape(q.strip()),
            "text": html_mod.unescape(a.strip().replace('\n', ' '))
        })
    return faqs

def make_faq_schema(faqs):
    if not faqs:
        return ''
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": []
    }
    for f in faqs:
        schema["mainEntity"].append({
            "@type": "Question",
            "name": f["name"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f["text"]
            }
        })
    return '  <script type="application/ld+json">\n' + json.dumps(schema, indent=2) + '\n  </script>'

def wrap_article(slug, title, summary, badge, content):
    og_desc = summary if len(summary) <= 160 else summary[:157] + "..."
    url = f"https://theclimateline.pages.dev/articles/{slug}.html"
    img = f"https://theclimateline.pages.dev/media/articles/{slug}.png"
    
    faqs = extract_faqs(content)
    faq_schema = make_faq_schema(faqs)
    
    # Ensure content starts with a newline then 4-space indent
    content_lines = content.strip().split('\n')
    indented = '\n'.join('    ' + l for l in content_lines)
    
    # Build the full HTML
    html = f'''<!DOCTYPE html>
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
  "datePublished": "{date_fmt}",
  "dateModified": "{date_fmt}"
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
{faq_schema}</head>
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
{indented}
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
    return html

for f in FRAGMENTS:
    path = ARTICLES_DIR / f'{f["slug"]}.html'
    if not path.exists():
        print(f'{f["slug"]}: not found')
        continue
    
    raw = path.read_text(encoding='utf-8')
    
    # Strip any existing HTML shell if present
    content = raw
    if '<article' in content:
        start = content.find('<article')
        content = content[content.find('>', start) + 1:]
    if '</article>' in content:
        content = content[:content.find('</article>')]
    
    content = content.strip()
    
    html = wrap_article(f['slug'], f['title'], f['summary'], f['badge'], content)
    path.write_text(html, encoding='utf-8')
    wc = len(content.split())
    print(f'{f["slug"]}: wrapped ({wc} words, {len(extract_faqs(content))} FAQs)')
