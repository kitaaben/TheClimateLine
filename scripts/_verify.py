from pathlib import Path
import re

ARTICLES_DIR = Path(r'C:\TheClimateLine\articles')

for path in sorted(ARTICLES_DIR.glob('*.html')):
    html = path.read_text(encoding='utf-8')
    issues = []
    
    faq_count = len(re.findall(r'faq-section', html))
    if faq_count > 0:
        issues.append(f'{faq_count} faq-section refs')
    
    rel_count = len(re.findall(r'related-articles', html))
    if rel_count > 0:
        issues.append(f'{rel_count} related-articles refs')
    
    has_faq = 'Frequently Asked Questions</h2>' in html
    has_rel = 'Related Articles</h2>' in html
    
    if not has_faq:
        issues.append('MISSING FAQ')
    if not has_rel:
        issues.append('MISSING Related')
    
    # Check for duplicate Related/FAQ sections  
    rel_count_h2 = html.count('<h2>Related Articles</h2>')
    if rel_count_h2 > 1:
        issues.append(f'{rel_count_h2}x Related sections')
    
    faq_count_h2 = html.count('<h2>Frequently Asked Questions</h2>')
    if faq_count_h2 > 1:
        issues.append(f'{faq_count_h2}x FAQ sections')
    
    # Check for broken div structure near article end
    close_idx = html.find('</article>')
    before_close = html[max(0, close_idx-100):close_idx]
    extra_divs = before_close.count('</div>')
    if extra_divs > 1:
        issues.append(f'{extra_divs} close-divs before </article>')
    
    if issues:
        print(f'{path.stem}: {", ".join(issues)}')
    else:
        print(f'{path.stem}: OK')
