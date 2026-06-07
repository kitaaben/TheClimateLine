import re
from pathlib import Path

ARTICLES_DIR = Path(r'C:\TheClimateLine\articles')

for slug in ['rising-temperatures-global-warming', 'heatwaves-climate-crisis', 'climate-news-2026']:
    path = ARTICLES_DIR / f'{slug}.html'
    html = path.read_text(encoding='utf-8')

    # Find </article> close
    idx_close = html.find('</article>')
    
    # Find article-nav div start (search backwards from "article-nav" to find '<div')
    idx_nav_str = html.find("article-nav", idx_close)
    idx_nav_div = html.rfind("<div", 0, idx_nav_str + 1)
    
    between = html[idx_close + 10:idx_nav_div]
    
    has_faq = 'Frequently Asked' in between
    has_related = 'Related Articles' in between
    print(f'{slug}: FAQ={has_faq}, Related={has_related}')

    if has_faq or has_related:
        new_html = (
            html[:idx_close]
            + '\n    ' + between.strip() + '\n\n  '
            + '\n  </article>'
            + html[idx_nav_div:]
        )
        path.write_text(new_html, encoding='utf-8')
        print(f'  Fixed!')
