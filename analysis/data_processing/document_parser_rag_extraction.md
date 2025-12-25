# Precision Document Parser for Structured Data Extraction

## Metadata
- **Category:** Analysis > Data Processing
- **Complexity:** Advanced
- **Estimated Time:** 1–45 minutes (depending on document length)
- **Dependencies:** None
- **Version:** 1.0
- **Last Updated:** 2025-12-25
- **Tags:** #document-extraction #rag #ml-training #structured-data #markdown #zero-hallucination

---

## Purpose
Extract all content from attached documents into **Structured Semantic Markdown** optimized for:
- ML training datasets
- RAG (Retrieval Augmented Generation) vector databases

**Priorities:** accuracy, verbatim extraction, and explicit flagging of limitations.

---

## Prerequisites
- [ ] Document file ready (PDF, image, or text)
- [ ] Understanding of Markdown syntax
- [ ] Familiarity with RAG / ML training concepts (helpful but not required)

---

## Input Requirements
- A document (PDF, image, or text file) to be extracted
- Intended use (ML training, RAG database, etc.)
- Any specific formatting preferences

---

## Prompt

### ROLE
**PRECISION DOCUMENT PARSER FOR STRUCTURED DATA EXTRACTION**

### OBJECTIVE
Extract all content from the attached document into **Structured Semantic Markdown** for ML training sets and RAG vector databases.

---

## Core Principles (Non-Negotiable)

1. **ZERO HALLUCINATION**  
   If something cannot be read, mark it `[UNREADABLE]`. Never guess.

2. **ZERO SUMMARIZATION**  
   Extract verbatim. Do not condense, paraphrase, or clean up.

3. **ZERO ASSUMPTION**  
   If data is ambiguous, flag it. Do not resolve ambiguity silently.

4. **PRESERVE ERRORS**  
   Keep all typos, grammatical errors, and inconsistencies.

---

## Phase 1: Content Block Classification

Before extracting, classify each page’s content blocks:

| Block Type | Definition |
|-----------|------------|
| TEXT | Paragraphs, headers, bullet points, footnotes |
| TABLE | Structured rows and columns |
| VISUAL | Charts, graphs, diagrams, images, icons |
| HYBRID | Mixed content (e.g., annotated chart with text overlay) |

---

## Phase 2: Extraction Rules by Content Type

### 2A. Text Blocks
- Extract **verbatim**, including typos
- Preserve hierarchy (`# H1`, `## H2`, `### H3`)
- Sidebars/callouts → use blockquotes
- Footnotes → `[^1]` Markdown syntax
- Partially obscured → `[PARTIAL: visible text...]`
- Fully unreadable → `[UNREADABLE: location description]`

---

### 2B. Table Blocks
- Use **GitHub Flavored Markdown (GFM)** tables
- Preserve **exact** column headers
- Empty cells → `[EMPTY]`
- Merged cells:
  - `[MERGED→R]` (spans right)
  - `[MERGED↓D]` (spans down)
- Multi-page tables → `[TABLE_CONTINUES: see Page X]`
- Unclear values → `[UNCLEAR: best guess?]`

---

### 2C. Visual Blocks (Charts, Graphs, Diagrams)

> ⚠️ **CRITICAL:** Do **NOT** fabricate numeric coordinates from images. Do **NOT** fabricate data points, prices, or exact values.

#### What to Extract

**1. Visual Metadata**
- Chart type
- Title (or `[NO_TITLE]`)
- Axis labels (verbatim)
- Timeframe (if visible)
- Data source (if cited)

**2. Readable Numeric Values** (ONLY if clearly printed on chart)
- Axis scale endpoints (only if printed) (e.g., "Y-axis ranges from 0 to 100")
- Explicitly labeled values (e.g., "Peak labeled '52,000'")
- Legend values

**3. Qualitative Visual Description**
- Overall trend (Rising / Falling / Sideways / Volatile/ etc)
- Notable patterns (Describe what is visually evident)
  Example: "Two peaks of similar height followed by decline"
- Indicator relationships (qualitative only) (e.g., "RSI line trends downward while price trends upward" — but DO NOT assign coordinates)

**4. Annotations & Overlays**
- Trendlines
- Text annotations (verbatim)
- Arrows, highlights, shapes

#### Prohibited
- Invented coordinates
- Fabricated percentages
- Calculated slopes
- Asserting specific divergence angles

---

### 2D. Hybrid Blocks
- Separate text and visual components
- Note relationships explicitly
  Example: "Text annotation A refers to chart element B"

---

## Phase 3: Metadata & RAG Optimization

Each page must include:

```html
<!--
PAGE_META:
  page_number: [N]
  content_types: [TEXT, TABLE, VISUAL]
  primary_topic: [Brief descriptor]
  extraction_confidence: [HIGH | MEDIUM | LOW]
  confidence_reason: [Explanation]
-->
````

At the end of each semantic section:

```
[CHUNK_TAGS: keyword, content_type, subtopic]
```

---

## Phase 4: Validation & Warnings

Each page must end with:

### Extraction Warnings

| Issue Type        | Location    | Description                         |
| ----------------- | ----------- | ----------------------------------- |
| TYPO_PRESERVED    | Para 2      | "gooch" appears — may be "good"     |
| UNREADABLE        | Table row 5 | Low resolution                      |
| VISUAL_LIMITATION | Chart 1     | Coordinates unavailable             |
| AMBIGUOUS         | Header      | Could be "Section 1" or "Section I" |
| OVERLAP           | Footer      | Text overlaps page number           |

---

## Phase 5: Output Template

```markdown
---

<!--
PAGE_META:
  page_number: 1
  content_types: [TEXT, TABLE, VISUAL]
  primary_topic: RSI Divergence Patterns
  extraction_confidence: MEDIUM
  confidence_reason: Chart present; coordinates not extractable
-->

# [Page Title]

## Text Content
[Verbatim text with hierarchy preserved]

> [Sidebar or callout]

## Tables

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Data | Data | [EMPTY] |
| Data | [UNCLEAR: 45?] | Data |

## Visual Content
### Visual 1: [Title]

**Type:** Candlestick chart with RSI oscillator panel below

**Axis Labels:**
- X-axis: "Date" (range: Jan 2024 — Mar 2024)
- Y-axis (price): Scale shows 40,000 to 60,000
- Y-axis (RSI): Scale shows 0 to 100

**Readable Values:**
- RSI oversold line marked at 30
- RSI overbought line marked at 70
- No specific price points labeled

**Visual Description:**
- Price action: Series of lower lows from left to right
- RSI behavior: Forms higher lows while price makes lower lows
- Annotations: Arrow pointing to RSI trough with text "Bullish Signal"
- Trendlines: Diagonal line connecting two RSI lows, sloping upward

**Limitations:**
- [CANNOT_EXTRACT: Precise price values at each candle]
- [CANNOT_EXTRACT: Exact RSI numerical readings per bar]

[CHUNK_TAGS: example]
---

### Extraction Warnings

| Issue Type | Location | Description |
|------------|----------|-------------|
| VISUAL_LIMITATION | Visual 1 | Coordinate extraction not possible |
| TYPO_PRESERVED | Para 3 | Original shows "bullisch" |

---

## Final Instructions

1. Process pages sequentially
2. Never skip boilerplate
3. If context limit is reached, state stopping point
4. Merge multi-page tables if possible
5. End with `DOCUMENT_SUMMARY`

---

## Document Summary Template

```html
<!--
DOCUMENT_SUMMARY:
  total_pages_processed: [N]
  total_text_blocks: [N]
  total_tables: [N]
  total_visuals: [N]
  overall_extraction_confidence: [HIGH | MEDIUM | LOW]
  known_limitations: [List]
-->
```

---

## Tips for Best Results

* Read entire document before extracting
* Use classification consistently
* Flag ambiguity immediately
* Prefer `[UNREADABLE]` over guessing
* Preserve all formatting quirks
* Tag strategically for RAG retrieval

---

## Common Issues & Solutions

| Issue               | Solution                          |
| ------------------- | --------------------------------- |
| Hallucinated values | Use qualitative descriptions only |
| Summarization       | Copy verbatim                     |
| Missing boilerplate | Include headers/footers           |
| Unclear tables      | Use `[UNCLEAR]`                   |
| Multi-page tables   | Use continuation markers          |

---

## Validation Checklist

* Verbatim text
* Preserved hierarchy
* GFM tables
* Visual metadata present
* No invented values
* Warnings included
* Chunk tags added
* Document summary included

---

## Changelog

* **v1.0 (2025-12-25)** — Initial release

---

## How to Use

1. Copy the **Prompt** section
2. Paste into AI chat
3. Attach document
4. Run extraction
5. Validate output
6. Ingest into ML/RAG pipeline