from pathlib import Path

articles_dir = Path(r'C:\TheClimateLine\articles')

for path in sorted(articles_dir.glob('*.html')):
    html = path.read_text(encoding='utf-8')
    original = html

    # Remove opening wrapper divs
    html = html.replace('<div class="faq-section">', '', 1)
    html = html.replace('<div class="related-articles">', '', 1)

    # Remove the closing </div> of faq-section (first </div> after FAQ h2 that's before Related)
    faq_h2 = '<h2>Frequently Asked Questions</h2>'
    rel_h2 = '<h2>Related Articles</h2>'
    
    faq_pos = html.find(faq_h2)
    rel_pos = html.find(rel_h2)
    
    if faq_pos != -1 and rel_pos != -1:
        # Between FAQ h2 and Related h2, find the </div> that closes faq-section
        between = html[faq_pos:rel_pos]
        close_div = between.rfind('</div>')
        if close_div != -1:
            abs_pos = faq_pos + close_div
            html = html[:abs_pos] + html[abs_pos + 6:]
    
    # Remove the closing </div> of related-articles (last </div> before </article>)
    article_close = html.find('</article>')
    rel_pos2 = html.find('<h2>Related Articles</h2>')
    
    if rel_pos2 != -1 and article_close != -1:
        between = html[rel_pos2:article_close]
        close_div = between.rfind('</div>')
        if close_div != -1:
            abs_pos = rel_pos2 + close_div
            html = html[:abs_pos] + html[abs_pos + 6:]

    if html != original:
        path.write_text(html, encoding='utf-8')
        print(f'{path.stem}: stripped')

# CSS cleanup
css_path = Path(r'C:\TheClimateLine\css\style.css')
css = css_path.read_text(encoding='utf-8')

for cls in ['.faq-section', '.related-articles']:
    while cls + ' {' in css:
        start = css.find(cls + ' {')
        end = css.find('\n}', start)
        if end != -1:
            css = css[:start] + css[end+2:]
        else:
            break

css = '\n'.join(l for l in css.split('\n') if l.strip() or l == '')
css_path.write_text(css, encoding='utf-8')
print('CSS cleaned')
