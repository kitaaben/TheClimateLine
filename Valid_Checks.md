# Daily Content Checklist (GEO-Optimized)

## Planning
- [ ] Select topic (see article backlog or trending climate news)
- [ ] Determine slug, title, meta description (150-160 chars with CTA)
- [ ] Define target intent: [Informational / How-to / Comparison / Troubleshooting]
- [ ] Define tone: [Formal / Conversational / Technical]

## Content Writing (GEO Optimization)

### Structure & Direct Answers
- [ ] Minimum 1500 words with clear H2/H3 structure
- [ ] **Each H2 section starts with direct 2-3 sentence answer**
- [ ] Questions answered before elaboration
- [ ] No unnecessary introduction before main point
- [ ] Average sentence length: 15-20 words (AI-friendly)

### Authority & E-E-A-T Signals
- [ ] External authority links (5+ minimum):
  - [ ] IPCC, NASA, NOAA, WMO, IEA, UNEP, World Bank
  - [ ] Peer-reviewed sources (Nature, Science)
  - [ ] International organizations (IMF, WHO)
- [ ] Blockquote from notable figure or credible report
- [ ] Statistics in `<div class='highlight-box'>` (3+ data points)
- [ ] Real-world examples/case studies (2-3 included)
- [ ] Domain-specific terminology used correctly (Expertise)

### Content Density
- [ ] Information density high (no filler/fluff)
- [ ] Key statistics with sources cited
- [ ] Practical examples supporting claims
- [ ] Factual statements (no exaggeration)

### Conversational Optimization
- [ ] Content matches natural language queries
- [ ] Covers "How to..." answers if applicable
- [ ] Explains "Why does..." for causal questions
- [ ] Tone conversational (not keyword-stuffed)
- [ ] FAQ section (5 Q&A pairs, no "Q:" / "A:" prefixes)

### Sections & Organization
- [ ] Related Articles section (`<p><a>` format, no `<ul>`)
- [ ] No wrapper divs around FAQ/Related sections
- [ ] Clear logical flow (general → specific)

## Authority Verification Report

### E-E-A-T Checklist
- [ ] **Experience**: Real-world applications demonstrated
- [ ] **Expertise**: Technical accuracy verified, domain terms used
- [ ] **Authoritativeness**: 5+ credible citations included
- [ ] **Trustworthiness**: Clear, factual, no exaggerated claims

### Data Points
- [ ] Statistics included: ___ count (target: 3+)
- [ ] Citations used: ___ count (target: 5+)
- [ ] Real examples: ___ count (target: 2+)
- [ ] Case studies: ___ count (target: 1+)

## Structure Breakdown Documentation

- [ ] **H2 Sections** (list):
  1. ___________
  2. ___________
  3. ___________

- [ ] **H3 Subsections** (count): ___

- [ ] **FAQ Questions Generated** (list):
  1. ___________
  2. ___________
  3. ___________
  4. ___________
  5. ___________

- [ ] **Key Points Extracted** (list):
  1. ___________
  2. ___________
  3. ___________

## AI Summarization Test

- [ ] Run article summary through Claude/ChatGPT
- [ ] Each H2 section can stand independently
- [ ] Key points extractable as bullet list
- [ ] Direct answers immediately identifiable

## OG Image & Media

- [ ] Find relevant image from `C:\media\climate\`
- [ ] Copy to `media/articles/{slug}.png`
- [ ] Verify `<meta property="og:image">` and `<meta name="twitter:image">` match

## YouTube Video (if applicable)

- [ ] Find relevant video from YouTube channel
- [ ] Add `videoId` to `articles.json`
- [ ] Add `<div class='video-embed'>` with `<iframe>` at top
- [ ] Add `"thumbnailUrl"` and `"embedUrl"` to schema
- [ ] Update hero badge to "Video Article"
- [ ] Add audio file and duration if available

## Inline Thumbnail

- [ ] Add `<div class='article-image'>` with `<img>`
- [ ] Image src: `https://theclimateline.pages.dev/media/articles/{slug}.png`

## HTML & Schema

- [ ] All OG tags (title, description, image, url, type, site_name)
- [ ] Twitter card tags (summary_large_image)
- [ ] Schema: Article + Organization + FAQPage
- [ ] Nav and footer present
- [ ] Hero section (badge, title, date, meta)
- [ ] Article nav (← Back to Articles / All Articles →)

## Registration & Deployment

- [ ] Add entry to `articles.json` (slug, title, summary, date, videoId)
- [ ] Run `python scripts/generate_sitemap.py`
- [ ] Deploy: `wrangler pages deploy . --branch=main --project-name=theclimateline`
- [ ] Verify OG images return 200
- [ ] Submit updated sitemap to Google Search Console
- [ ] Check article loads on live site
- [ ] Verify schema markup with Rich Results Test