from pathlib import Path
import re

articles_dir = Path(r'C:\TheClimateLine\articles')

for path in sorted(articles_dir.glob('*.html')):
    html = path.read_text(encoding='utf-8')
    original = html

    # Clean up excessive blank lines (3+ consecutive newlines -> 2)
    html = re.sub(r'\n{3,}', '\n\n', html)
    
    # Ensure </article> has correct indent (2 spaces to match <article>)
    html = html.replace('\n</article>', '\n  </article>')

    if html != original:
        path.write_text(html, encoding='utf-8')
        print(f'{path.stem}: cleaned')
    else:
        print(f'{path.stem}: OK')
