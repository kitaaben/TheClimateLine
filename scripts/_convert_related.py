from pathlib import Path
import re

articles_dir = Path(r'C:\TheClimateLine\articles')

for path in sorted(articles_dir.glob('*.html')):
    html = path.read_text(encoding='utf-8')
    original = html

    rel_h2 = '<h2>Related Articles</h2>'
    rel_idx = html.find(rel_h2)
    if rel_idx == -1:
        continue

    after_h2 = html[rel_idx + len(rel_h2):]
    stripped = after_h2.lstrip()
    if stripped.startswith('<ul>'):
        ul_match = re.search(r'<ul>(.*?)</ul>', stripped, re.DOTALL)
        if ul_match:
            ul_content = ul_match.group(1)
            links = re.findall(r'<li>\s*<a\s+href=[\'"]([^\'"]+)[\'"]>(.*?)</a>\s*</li>', ul_content)
            
            indent = '    '
            p_lines = []
            for href, text in links:
                p_lines.append(f'{indent}<p><a href=\'{href}\'>{text}</a></p>')
            p_section = '\n'.join(p_lines)
            
            whitespace_count = len(after_h2) - len(stripped)
            ul_start = rel_idx + len(rel_h2) + whitespace_count
            
            # Find </ul> directly
            close_ul = after_h2.find('</ul>')
            if close_ul != -1:
                ul_end = rel_idx + len(rel_h2) + close_ul + 5  # +5 for </ul>
                html = html[:ul_start] + '\n' + p_section + '\n' + html[ul_end:]

    if html != original:
        path.write_text(html, encoding='utf-8')
        print(f'{path.stem}: converted')
    else:
        print(f'{path.stem}: OK')
