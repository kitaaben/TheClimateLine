from pathlib import Path

articles_dir = Path(r'C:\TheClimateLine\articles')
indent = '    '

for path in sorted(articles_dir.glob('*.html')):
    html = path.read_text(encoding='utf-8')
    original = html

    # Normalize indentation of FAQ content (between FAQ h2 and Related h2)
    faq_h2 = '<h2>Frequently Asked Questions</h2>'
    rel_h2 = '<h2>Related Articles</h2>'
    
    faq_pos = html.find(faq_h2)
    rel_pos = html.find(rel_h2)
    
    if faq_pos != -1 and rel_pos != -1:
        # Get lines between FAQ h2 and Related h2
        before_faq = html[:faq_pos]
        faq_to_rel = html[faq_pos:rel_pos]
        after_rel = html[rel_pos:]
        
        # Re-indent FAQ content
        faq_lines = faq_to_rel.split('\n')
        new_faq_lines = []
        for line in faq_lines:
            stripped = line.strip()
            if stripped:
                new_faq_lines.append(indent + stripped)
            else:
                new_faq_lines.append('')
        faq_indented = '\n'.join(new_faq_lines)
        
        # Re-indent Related content (including any ul/li/p)
        rel_lines = after_rel.split('\n')
        new_rel_lines = []
        in_related = True
        for line in rel_lines:
            stripped = line.strip()
            if stripped == '</article>' or stripped.startswith('<div'):
                in_related = False
            if stripped and in_related:
                new_rel_lines.append(indent + stripped)
            else:
                new_rel_lines.append(line)
        rel_indented = '\n'.join(new_rel_lines)
        
        # Also ensure the FAQ h2 itself has consistent indent relative to surrounding content
        html = before_faq.rstrip() + '\n' + faq_indented + '\n' + rel_indented

    if html != original:
        path.write_text(html, encoding='utf-8')
        print(f'{path.stem}: indented')
    else:
        print(f'{path.stem}: OK')
