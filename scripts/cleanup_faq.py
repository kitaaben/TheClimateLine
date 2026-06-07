from pathlib import Path
import re

ARTICLES_DIR = Path(r'C:\TheClimateLine\articles')

for path in sorted(ARTICLES_DIR.glob('*.html')):
    html = path.read_text(encoding='utf-8')
    original = html

    # Remove all faq-section and related-articles wrapper tags
    html = re.sub(r'<div class="faq-section">\s*', '', html, flags=re.DOTALL)
    html = re.sub(r'<div class="related-articles">\s*', '', html, flags=re.DOTALL)
    # Remove all </div> that belong to these wrappers (they appear right before blank lines before next section or </article>)
    # Actually let's just remove </div> that appears between FAQ/Related content
  
    # Strategy: remove any </div> that appears on its own line before a blank line or </article>
    # Pattern: </div> followed by optional whitespace and newline
    html = re.sub(r'\s*</div>\s*\n\s*', '\n', html)

    # Now add clean wrappers
    idx_faq = html.find('<h2>Frequently Asked Questions</h2>')
    idx_rel = html.find('<h2>Related Articles</h2>')
    idx_close = html.find('</article>')

    if idx_faq == -1 or idx_rel == -1:
        print(f'{path.stem}: FAQ/Related not found')
        continue

    line_start = html.rfind('\n', 0, idx_faq) + 1
    indent = html[line_start:idx_faq]

    faq_block = html[idx_faq:idx_rel].strip()
    rel_block = html[idx_rel:idx_close].strip()

    faq_indented = '\n'.join(indent + l for l in faq_block.split('\n'))
    rel_indented = '\n'.join(indent + l for l in rel_block.split('\n'))

    new_html = (
        html[:line_start]
        + f'{indent}<div class="faq-section">\n'
        + faq_indented + '\n'
        + f'{indent}</div>\n'
        + f'{indent}<div class="related-articles">\n'
        + rel_indented + '\n'
        + f'{indent}</div>\n  '
        + html[idx_close:]
    )

    path.write_text(new_html, encoding='utf-8')
    print(f'{path.stem}: Cleaned and re-wrapped')
