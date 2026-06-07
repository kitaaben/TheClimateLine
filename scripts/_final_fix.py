from pathlib import Path
import re

ARTICLES_DIR = Path(r'C:\TheClimateLine\articles')

for path in sorted(ARTICLES_DIR.glob('*.html')):
    html = path.read_text(encoding='utf-8')
    
    # Remove all wrapper opening divs
    html = html.replace('<div class="faq-section">', '')
    html = html.replace('<div class="related-articles">', '')
    
    # Remove </div> that closes faq-section (appears right before Related h2)
    html = re.sub(r'</div>\s*\n\s*<h2>Related Articles', '<h2>Related Articles', html)
    
    # Remove </div> that closes related-articles (appears right before </article>)
    html = re.sub(r'</div>\s*\n\s*</article>', '\n  </article>', html)
    
    # Remove </div> that closes related-articles when FAQ comes after (if FAQ before Related)
    html = re.sub(r'</div>\s*\n\s*<h2>Frequently Asked', '<h2>Frequently Asked', html)
    
    # Remove duplicate Related Articles sections
    # If there are multiple <h2>Related Articles</h2>, keep only the last one and its content
    while True:
        # Find all positions of "Related Articles" h2
        first = html.find('<h2>Related Articles</h2>')
        if first == -1:
            break
        second = html.find('<h2>Related Articles</h2>', first + 5)
        if second == -1:
            break
        
        # Remove from first h2 to just before second h2
        html = html[:first] + html[second:]
    
    # Remove duplicate FAQ sections
    while True:
        first = html.find('<h2>Frequently Asked Questions</h2>')
        if first == -1:
            break
        second = html.find('<h2>Frequently Asked Questions</h2>', first + 5)
        if second == -1:
            break
        html = html[:first] + html[second:]
    
    path.write_text(html, encoding='utf-8')
    print(f'{path.stem}: Cleaned')
