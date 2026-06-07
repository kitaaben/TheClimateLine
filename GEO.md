# Generative Engine Optimization (GEO) Agent Skill Specification

## Overview

Generative Engine Optimization (GEO) is a modern content optimization approach designed specifically for AI-driven search engines and generative models. Unlike traditional SEO, which focuses on keyword matching and backlinks, GEO prioritizes:

- Contextual relevance
- Information structure
- Authority signals
- Conversational query alignment
- Machine summarization efficiency

This skill transforms raw or unstructured content into a format optimized for AI interpretation and synthesis.

---

## Skill Identity

- **Name:** Generative Engine Optimization (GEO)
- **Category:** AI Content Optimization / SEO Agent Skill
- **Version:** 1.0
- **Target Systems:** Generative search engines, LLM-based ranking systems, AI assistants

---

## Goal of the Skill

The goal is to convert any input content into a format that:

- Can be easily summarized by AI systems
- Has strong informational hierarchy
- Contains authoritative signals (data, citations, expertise)
- Matches natural language search behavior
- Improves visibility in generative search results

---

## Input Definition

The skill accepts structured input as follows:

### Required Inputs
- **topic** → The main subject being optimized
- **content** → Raw text, draft article, or unstructured information

### Optional Inputs
- **intent** → The search or user intent type (e.g., informational, how-to, comparison, troubleshooting)

---

## Processing Pipeline

The GEO skill executes in the following phases:

---

### Phase 1: Content Structuring

The system restructures content for machine readability:

- Break content into logical sections
- Add clear **H2 and H3 headings**
- Ensure each section begins with a **direct 2–3 sentence answer**
- Convert long paragraphs into bullet points where necessary
- Maintain logical flow from general → specific

---

### Phase 2: Direct Answer Optimization

Each major section must include:

- A concise, direct explanation at the beginning
- Immediate answer to the implied user question
- No unnecessary introduction before the answer

This ensures AI systems can extract summary-ready content instantly.

---

### Phase 3: Information Density Enhancement

To improve authority and usefulness:

- Add **statistics and numerical data where possible**
- Include **credible external references or citations**
- Integrate **real-world examples or case studies**
- Replace vague statements with concrete facts
- Remove filler, redundancy, and fluff

---

### Phase 4: Authority Signal Injection (E-E-A-T)

The system strengthens trust signals based on:

#### Experience
- Real-world application examples
- Practical demonstrations

#### Expertise
- Technical accuracy
- Domain-specific terminology

#### Authoritativeness
- Citations from credible sources
- Industry references

#### Trustworthiness
- Clear, factual statements
- Avoidance of exaggerated claims

Additionally:

- Recommend schema types:
  - Article Schema
  - Organization Schema
  - Product Schema (if applicable)

---

### Phase 5: Conversational Intent Alignment

Content is rewritten to match how users interact with AI search engines:

- Use natural language phrasing
- Target long-form queries such as:
  - “how do I…”
  - “what is the best way to…”
  - “why does… happen”
- Avoid keyword stuffing
- Maintain human-readable tone

---

## Output Structure

The final output must include:

### 1. Optimized Content
Fully rewritten and structured GEO-friendly article or content block.

### 2. Structure Breakdown
A breakdown of:
- Direct answer sections
- Headings used (H2/H3)
- Key points extracted
- FAQ questions generated

### 3. Authority Report
Includes:
- Whether citations were used
- Whether statistics were included
- Whether E-E-A-T improvements were applied
- Suggested schema markup types

### 4. Intent Mapping
Defines:
- Target tone (formal, conversational, technical)
- Query types addressed (how-to, informational, comparison, troubleshooting)

---

## Output Format (JSON-like structure concept)

```json
{
  "optimized_content": "...",
  "structure_breakdown": {
    "direct_answer_sections": [],
    "headings": [],
    "faq_questions": [],
    "key_points": []
  },
  "authority_signals": {
    "citations_used": true,
    "stats_included": true,
    "eeat_enhanced": true,
    "schema_recommended": []
  },
  "intent_alignment": {
    "tone": "conversational",
    "query_type_targeted": []
  }
}