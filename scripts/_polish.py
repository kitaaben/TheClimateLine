from pathlib import Path
import re

ARTICLES_DIR = Path(r'C:\TheClimateLine\articles')

for path in sorted(ARTICLES_DIR.glob('*.html')):
    html = path.read_text(encoding='utf-8')
    original = html
    name = path.stem

    # Fix climate-news-2026 broken </article>
    html = html.replace(
        '<div class="\n    </div>\n  </article>article-nav">',
        '</article>\n  <div class="article-nav">'
    )
    html = html.replace('</article><div', '</article>\n  <div')

    # Dedup: remove duplicate h2+ul blocks inside related-articles
    # Pattern: after </ul>, if there's blank lines then another <h2>Related...<ul>...</ul>, remove the duplicate
    def dedup_related(content):
        """Remove duplicate Related h2+ul blocks inside related-articles divs."""
        ra_start = content.find('<div class="related-articles">')
        if ra_start == -1:
            return content
        
        ra_end = content.find('</div>', ra_start)
        if ra_end == -1:
            return content
        ra_end += 6  # include </div>
        
        inside = content[ra_start:ra_end]
        
        # Find all h2+ul blocks
        h2_positions = []
        idx = 0
        while True:
            h2_pos = inside.find('<h2>Related Articles</h2>', idx)
            if h2_pos == -1:
                break
            ul_start = inside.find('<ul>', h2_pos)
            ul_end = inside.find('</ul>', h2_pos)
            if ul_start != -1 and ul_end != -1:
                h2_positions.append((h2_pos, ul_end + 5))
            idx = h2_pos + 1
        
        # Keep only the first h2+ul block, remove rest
        if len(h2_positions) > 1:
            first_end = h2_positions[0][1]
            # Remove everything from after first block to before </div>
            # Find the last h2+ul block end
            last_end = h2_positions[-1][1]
            # Remove content between first_end and last_end
            new_inside = inside[:first_end] + inside[last_end:]
            content = content[:ra_start] + new_inside + content[ra_end:]
        
        return content
    
    html = dedup_related(html)

    # Also handle inverted order if still present
    first_rel = html.find('<h2>Related Articles</h2>')
    faq_h2 = '<h2>Frequently Asked Questions</h2>'
    first_faq = html.find(faq_h2)
    article_close = html.find('</article>')

    if first_rel != -1 and first_faq != -1 and article_close != -1 and first_rel < first_faq:
        section = html[first_rel:article_close]
        faq_in_section = section.find(faq_h2)
        
        if faq_in_section != -1:
            raw_related = section[:faq_in_section]
            raw_faq = section[faq_in_section:]
            
            for div_class in ['related-articles', 'faq-section']:
                raw_related = raw_related.replace(f'<div class="{div_class}">', '').replace('</div>', '')
                raw_faq = raw_faq.replace(f'<div class="{div_class}">', '').replace('</div>', '')
            
            # Dedup Related (only if multiple h2 blocks)
            rel_blocks = [l for l in raw_related.split('\n') if l.strip() and not l.strip() == '<ul>' and not l.strip().startswith('<li>') and not l.strip() == '</ul>']
            h2_count = raw_related.count('<h2>Related Articles</h2>')
            if h2_count > 1:
                # Find first h2 and keep up to its next </ul>
                first_h2 = raw_related.find('<h2>Related Articles</h2>')
                after_first_h2 = raw_related[first_h2:]
                first_ul_end = after_first_h2.find('</ul>')
                if first_ul_end != -1:
                    raw_related = after_first_h2[:first_ul_end + 5]
            
            clean_related = '\n'.join(l.strip() for l in raw_related.split('\n') if l.strip())
            clean_faq = '\n'.join(l.strip() for l in raw_faq.split('\n') if l.strip())
            
            indent = '    '
            faq_indented = '\n'.join(indent + l for l in clean_faq.split('\n'))
            rel_indented = '\n'.join(indent + l for l in clean_related.split('\n'))
            
            new_section = (
                f'{indent}<div class="faq-section">\n'
                + faq_indented + '\n'
                + f'{indent}</div>\n'
                + f'{indent}<div class="related-articles">\n'
                + rel_indented + '\n'
                + f'{indent}</div>\n'
            )
            
            html = html[:first_rel].rstrip() + '\n' + new_section + html[article_close:].lstrip()

    if html != original:
        path.write_text(html, encoding='utf-8')
        print(f'{name}: Fixed')
    else:
        print(f'{name}: OK')
