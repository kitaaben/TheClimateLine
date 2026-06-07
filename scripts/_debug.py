from pathlib import Path
import re

ARTICLES_DIR = Path(r'C:\TheClimateLine\articles')
CSS_PATH = Path(r'C:\TheClimateLine\css\style.css')

CSS_ADDITIONS = """

.faq-section {
  margin-top: 48px;
  padding-top: 32px;
  border-top: 2px solid var(--border);
}

.faq-section h3 {
  font-size: 1.05rem;
  margin: 24px 0 8px;
  color: var(--text);
  font-weight: 600;
}

.faq-section h3::before {
  content: "Q: ";
  color: var(--green);
  font-weight: 700;
}

.faq-section p {
  margin-bottom: 16px;
  color: var(--text-secondary);
  padding-left: 0;
}

.faq-section p::before {
  content: "A: ";
  color: var(--green-light);
  font-weight: 600;
}

.related-articles {
  margin-top: 48px;
  padding: 24px;
  background: #e8f5e9;
  border: 1px solid #c8e6c9;
  border-radius: var(--radius);
}

.related-articles h2 {
  margin-top: 0 !important;
}

.related-articles > p {
  margin-bottom: 0 !important;
}

.related-articles a {
  display: block;
  padding: 14px 16px;
  margin-bottom: 8px;
  background: white;
  border: 1px solid var(--border);
  border-radius: 8px;
  text-decoration: none;
  color: var(--text);
  transition: all 0.2s ease;
  font-weight: 500;
}

.related-articles a:last-child {
  margin-bottom: 0;
}

.related-articles a:hover {
  border-color: var(--green);
  background: #f1f8f1;
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(46, 125, 50, 0.15);
}

.related-articles a small {
  display: block;
  font-weight: 400;
  color: var(--text-secondary);
  margin-top: 4px;
  font-size: 0.9rem;
}
"""

# Add CSS
css = CSS_PATH.read_text(encoding='utf-8')
if '.faq-section' not in css:
    css = css.rstrip() + '\n' + CSS_ADDITIONS
    CSS_PATH.write_text(css, encoding='utf-8')
    print('CSS added')
else:
    print('CSS already exists')

# Fix each article
for path in sorted(ARTICLES_DIR.glob('*.html')):
    html = path.read_text(encoding='utf-8')

    # Find positions
    idx_faq = html.find('<h2>Frequently Asked Questions</h2>')
    idx_rel = html.find('<h2>Related Articles</h2>')
    idx_article_close = html.find('</article>')

    if idx_faq == -1 or idx_rel == -1:
        print(f'{path.stem}: FAQ or Related not found')
        continue

    # Extract indentation
    line_start_faq = html.rfind('\n', 0, idx_faq) + 1
    indent_faq = html[line_start_faq:idx_faq]

    # FAQ content: from FAQ h2 to just before Related h2
    faq_content = html[idx_faq:idx_rel].rstrip()

    # Related content: from Related h2 to just before </article>
    rel_content = html[idx_rel:idx_article_close].rstrip()

    # Ensure content is indented properly inside the wrapper divs
    faq_indented = ''
    for line in faq_content.split('\n'):
        if line.strip():
            faq_indented += indent_faq + line.strip() + '\n'
        else:
            faq_indented += '\n'

    rel_indented = ''
    for line in rel_content.split('\n'):
        if line.strip():
            rel_indented += indent_faq + line.strip() + '\n'
        else:
            rel_indented += '\n'

    new_html = (
        html[:line_start_faq]
        + f'{indent_faq}<div class="faq-section">\n'
        + faq_indented
        + f'{indent_faq}</div>\n'
        + f'\n{indent_faq}<div class="related-articles">\n'
        + rel_indented
        + f'{indent_faq}</div>\n  '
        + html[idx_article_close:]
    )

    path.write_text(new_html, encoding='utf-8')
    print(f'{path.stem}: Wrapped in styled divs')
