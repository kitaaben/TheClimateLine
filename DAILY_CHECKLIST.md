# Daily Content Checklist (GEO + SEO + QA)

## Planning
- [ ] Select topic
- [ ] Determine slug, title, meta description (150-160 chars with CTA)
- [ ] Define target intent: [Informational / How-to / Comparison / Troubleshooting]
- [ ] Define tone: [Formal / Conversational / Technical]
- [ ] Add entry to `articles.json` (slug, title, summary, date, videoId/audio/null)

## Content Writing (GEO Optimization — see GEO.md)

### Direct Answer Pattern
- [ ] Minimum 1500 words (2,000-3,500 sweet spot)
- [ ] **Each H2 section starts with direct 2-3 sentence answer** before elaboration
- [ ] Questions answered before elaboration, no unnecessary intro
- [ ] Average sentence length: 15-20 words (AI-friendly)
- [ ] Clear logical flow: general → specific

### Authority & E-E-A-T Signals
- [ ] External authority links (5+ minimum): IPCC, NASA, NOAA, WMO, IEA, UNEP, World Bank, Nature, Science, IMF, WHO
- [ ] Internal links: 3-5 per article with keyword-rich anchor text
- [ ] Blockquote from notable figure or credible report
- [ ] Statistics in `<div class='highlight-box'>` (3+ data points with sources)
- [ ] Real-world examples/case studies (2-3 included)
- [ ] Domain-specific terminology used correctly

### Content Density
- [ ] High information density (no filler/fluff, replace vague statements with facts)
- [ ] Key statistics with sources cited
- [ ] Practical examples supporting claims
- [ ] Factual, conservative language (no exaggeration)

### Conversational Optimization
- [ ] Content matches natural language queries ("how does...", "what is...", "why does...")
- [ ] Tone conversational (not keyword-stuffed)
- [ ] FAQ section: 5 Q&A pairs, no "Q:" / "A:" prefixes
- [ ] Related Articles: `<p><a>` format, no `<ul>`
- [ ] No wrapper divs around FAQ/Related — direct h2/h3/p under `.article-content`

## Traditional SEO (see Ranking.md)

### Keyword Placement
- [ ] Primary keyword in: title, first 100 words, first H2, meta description
- [ ] Keyword density 0.5-2% (natural)
- [ ] Primary keyword in URL slug

### Schema Markup
- [ ] **Article Schema**: headline, description, image, author, publisher, date
- [ ] **Organization Schema**: name, url, logo, sameAs, description
- [ ] **FAQPage Schema**: mainEntity with Question/Answer (only if FAQ present)
- [ ] FAQ schema `name` / `text` fields match FAQ HTML exactly (no Q:/A: prefixes)
- [ ] Validate with Google Rich Results Test after deploy

## Article QA (learned from fixes)
- [ ] `<article class='article-content'>` is NOT empty — has actual paragraphs
- [ ] HTML is valid (no broken tags, no unclosed elements)
- [ ] FAQ section: no "Q:" / "A:" prefixes in HTML headings or schema
- [ ] No `media/hero/` paths exist anywhere (all images use `media/articles/`)

## OG Image & Media
- [ ] Find relevant image from `C:\media\climate\`
- [ ] Copy to `media/articles/{slug}.png`
- [ ] Verify `<meta property="og:image">` and `<meta name="twitter:image">` match

## Inline Thumbnail
- [ ] Add `<div class='article-image'>` with `<img>` as first child of `<article class='article-content'>`
- [ ] Image src: `https://theclimateline.pages.dev/media/articles/{slug}.png`

## YouTube Video (if videoId set)
- [ ] Add `<div class='video-embed'>` with `<iframe>` at top of article
- [ ] Add `"thumbnailUrl"` and `"embedUrl"` to Article schema
- [ ] Update hero badge to "Video Article"
- [ ] Add audio file path and duration to `articles.json`

## HTML Shell
- [ ] OG tags: title, description, image, url, type, site_name
- [ ] Twitter card tags: summary_large_image
- [ ] Nav and footer present
- [ ] Hero section: badge, title, date, meta
- [ ] Article nav: ← Back to Articles / All Articles →

## Homepage Integration
- [ ] `js/main.js:getArticleImg()` always uses `media/articles/{slug}.png` (never `media/hero/`)
- [ ] `renderFeaturedArticles()` includes all articles (not filtered by `videoId`)
- [ ] Directory listing thumbnails show on live site after deploy

## Deployment
- [ ] Run `python scripts/generate_sitemap.py`
- [ ] Deploy: `wrangler pages deploy . --branch=main --project-name=theclimateline`
- [ ] Verify OG images return 200
- [ ] Verify directory thumbnails render on homepage
- [ ] Submit updated sitemap to Google Search Console
- [ ] Check article loads on live site
- [ ] Validate schema with Rich Results Test

## Post-Deployment
- [ ] Monitor rank position weekly
- [ ] Build backlinks (2-3 per week)
- [ ] Analyze CTR + engagement
- [ ] Plan quarterly content updates with latest stats
