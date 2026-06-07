#!/usr/bin/env python3
"""Move FAQ and Related Articles inside <article> tag so they inherit CSS."""
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).resolve().parent.parent / "articles"

def fix_article(slug):
    path = ARTICLES_DIR / f"{slug}.html"
    html = path.read_text(encoding="utf-8")

    # Pattern: </article> followed by FAQ and Related Articles, then <div class='article-nav'>
    # We need to move the FAQ and Related Articles before </article>

    # Find the </article> closing tag
    article_close = "</article>"

    # Find what comes after </article> and before <div class='article-nav'>
    pattern = re.compile(
        r'(</article>)\s*\n\s*((?:<h2>Frequently Asked Questions.*?(?=<div class=\'article-nav\'>|<div class="article-nav">)))',
        re.DOTALL
    )

    def move_inside(m):
        article_end = m.group(1)
        extra_content = m.group(2)
        return extra_content + "\n\n  " + article_end

    new_html = pattern.sub(move_inside, html)

    if new_html != html:
        path.write_text(new_html, encoding="utf-8")
        print(f"  Fixed: {slug}.html")
        return True
    else:
        print(f"  Skipped: {slug}.html (no change)")
        return False

def main():
    slugs = [
        "rising-temperatures-global-warming",
        "rising-sea-levels-coastal-crisis",
        "heatwaves-climate-crisis",
        "will-we-be-part-of-the-climate-solution",
        "act-now-prevent-climate-catastrophe",
        "climate-catastrophe-time-to-act-now",
        "earths-climate-crisis-beyond-1c",
        "make-or-break-decade-climate-food",
        "carbon-lockout-window",
        "4c-catastrophe-our-final-warning",
        "climate-crisis-time-to-act",
        "climate-catastrophe-in-antarctica",
        "arctic-meltdown-our-final-warning",
        "methane-emissions-threaten-our-planet",
        "methane-leaks-the-untold-crisis",
        "climate-science-basics",
        "renewable-energy-solutions",
        "climate-news-2026",
    ]
    count = 0
    for slug in slugs:
        if fix_article(slug):
            count += 1
    print(f"Done. {count} articles fixed.")

if __name__ == "__main__":
    main()
