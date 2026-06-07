from pathlib import Path
path = Path(r'C:\TheClimateLine\articles\4c-catastrophe-our-final-warning.html')
html = path.read_text(encoding='utf-8')
idx = html.find('<div class="faq-section">')
if idx >= 0:
    print('Found at', idx)
    print(repr(html[idx-30:idx+200]))
else:
    print('Not found, trying other quote...')
    idx2 = html.find("faq-section")
    if idx2 >= 0:
        print('faq-section at', idx2)
        print(repr(html[idx2-50:idx2+200]))
