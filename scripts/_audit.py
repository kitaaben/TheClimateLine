from pathlib import Path
import re

ARTICLES_DIR = Path(r'C:\TheClimateLine\articles')

for path in sorted(ARTICLES_DIR.glob('*.html')):
    html = path.read_text(encoding='utf-8')

    # Step 1: Remove ALL faq-section and related-articles opening tags
    html = html.replace('<div class="faq-section">', '')
    html = html.replace('<div class="related-articles">', '')

    # Step 2: Remove closing </div> tags that are immediately adjacent to FAQ/Related h2 tags
    # These are the wrapper closings. Find patterns like:
    #   </div>
    #
    #   <h2>Frequently Asked Questions</h2>
    # or
    #   </div>
    # followed by </article> or blank line
    
    # Remove </div> that appears right before FAQ h2 (with whitespace between)
    html = re.sub(r'</div>\s*\n\s*(?=<h2>Frequently Asked Questions</h2>)', '', html)

    # Remove </div> that appears right after FAQ/Related content (before a blank line + next section or </article>)
    # Pattern: </div> that appears on its own line before </article>
    html = re.sub(r'</div>\s*\n\s*(?=</article>)', '', html)

    # Remove </div> that appears between FAQ end and Related start
    # Look for </div> followed by whitespace then <div or <h2
    html = re.sub(r'</div>\s*\n\s*(?=<h2>Related Articles)', '', html)
    html = re.sub(r'</div>\s*\n\s*(?=<h2>Frequently Asked)', '', html)
    
    # Remove </div> that appears right before blank lines followed by <h2>Related
    html = re.sub(r'</div>\s*\n\s*\n\s*(?=<h2>Related)', '', html)
    html = re.sub(r'</div>\s*\n\s*\n\s*(?=<h2>Frequently)', '', html)

    # Remove any remaining empty faq-section/related-articles wrapper divs that became empty
    html = re.sub(r'<div>\s*</div>', '', html)
    html = re.sub(r'<div>\s*\n\s*</div>', '', html)

    # Step 3: Now cleanly wrap the FAQ section
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

    # Indent content inside wrappers
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
    print(f'{path.stem}: Rebuilt clean wrappers')
