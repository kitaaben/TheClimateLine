from pathlib import Path

articles_dir = Path(r'C:\TheClimateLine\articles')

for path in sorted(articles_dir.glob('*.html')):
    html = path.read_text(encoding='utf-8')
    original = html

    # Remove orphaned </ul> that appears right after Related's <p> links
    # Pattern: </p>\n</ul> within the Related section (near </article>)
    rel_h2 = '<h2>Related Articles</h2>'
    rel_idx = html.find(rel_h2)
    article_close = html.find('</article>')
    
    if rel_idx != -1 and article_close != -1:
        # Find any </ul> between Related h2 and </article>
        # and remove it
        between = html[rel_idx:article_close]
        ul_pos = between.find('</ul>')
        if ul_pos != -1:
            abs_pos = rel_idx + ul_pos
            html = html[:abs_pos] + html[abs_pos + 5:]

    if html != original:
        path.write_text(html, encoding='utf-8')
        print(f'{path.stem}: cleaned')
    else:
        print(f'{path.stem}: OK')
