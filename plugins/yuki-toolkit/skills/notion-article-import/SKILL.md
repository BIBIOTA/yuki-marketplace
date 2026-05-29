---
name: notion-article-import
description: Use when given a Notion article URL and asked to import it into the bibiota-blog. Covers fetching Notion content, converting to VitePress Markdown, creating the post file, and registering the article in the pinned index.
---

# Notion Article Import

## Overview

Fetches a Notion page, converts it to a VitePress-compatible Markdown post, and registers the article in the pinned Daily Questions Challenge index.

## Step 1 — Fetch the Notion page

Use the `mcp__claude_ai_Notion__notion-fetch` tool with the provided Notion URL.

If the URL is a Notion page link (e.g. `https://www.notion.so/...`), pass it directly as the `url` parameter.

Extract from the result:
- **Title** (the page's H1 / title property)
- **Body content** (all blocks)
- **Any external reference links** at the bottom

## Step 2 — Determine article metadata

Ask (or infer from context):

| Field | How to determine |
|-------|-----------------|
| `date` | Ask the user, or use today's date (`YYYY-MM-DD`) |
| `category` | `tech` (default), `travel`, or `running` — ask if unclear |
| `serial` | For Daily Questions Challenge articles: the next challenge number (scan `docs/tech/posts/` for the highest `Challenge NN` number) |
| `slug` | Kebab-case summary of the title (e.g. `jwt-token`, `space-complexity`) |
| `tags` | Infer from content topic (e.g. `Algorithm`, `Backend`, `Python`, `Authentication`) |
| `description` | One-sentence summary of the article in Traditional Chinese |
| `index-category` | The section heading to add the link under in the pinned index (e.g. `演算法`, `Backend`, `Database`) |

File naming convention: `YYYY-MM-DD-<slug>.md`

## Step 2.5 — Confirm tags and index-category with the user

**Before writing any files**, present a confirmation prompt to the user.

Show exactly:

```
以下是我推薦的文章設定，請確認是否 OK：

**Tags（文章標籤）：**
- Tag1
- Tag2
（說明：根據 <理由> 推薦）

**置頂索引分類（index-category）：**
- <index-category>
（說明：會加入 ## 題目 > ### <index-category> 區塊）

請確認以上設定，或告訴我你想調整的部分。
```

**Wait for the user's explicit confirmation before proceeding.**

If the user adjusts tags or index-category, update the metadata accordingly.

Only continue to Step 3 after receiving approval.

## Step 3 — Convert Notion content to Markdown

Rules:
- Keep all Traditional Chinese wording as-is
- Convert Notion numbered sections → `##` / `###` headings
- Convert Notion bullet lists → standard `- ` Markdown lists
- Convert tables → GFM Markdown tables
- Preserve code blocks as fenced ` ``` ` blocks with language hint
- Preserve horizontal rules (`---`)
- Keep reference links under a `## 參考` section at the bottom
- Remove empty Notion blocks
- Replace any external URLs that point to the same blog content with relative repo links (e.g. replace a ChatGPT or Notion URL that refers to another blog article with `./YYYY-MM-DD-slug.md`)

## Step 4 — Create the post file

**Path:** `docs/<category>/posts/<date>-<slug>.md`

**Template:**

```markdown
---
layout: doc
title: "<title>"
description: <description>
date: <YYYY-MM-DD>
tags:
  - <Tag1>
  - <Tag2>
head:
  - - meta
    - property: og:title
      content: "<title>"
  - - meta
    - property: og:description
      content: <description>
  - - meta
    - name: twitter:title
      content: "<title>"
  - - meta
    - name: twitter:description
      content: <description>
---

<script setup>
  import ArticleTitle from '@theme/components/ArticleTitle.vue'
  import ScrollToTopBtn from '@theme/components/ScrollToTopBtn.vue'
</script>

<ArticleTitle />

<ScrollToTopBtn />

<converted article body>
```

## Step 5 — Register in the pinned index

**Pinned index file:** `docs/tech/posts/2026-05-26-daily-questions-challenge-2026.md`

Locate the `## 題目` section. Find the matching `### <index-category>` subsection (create it if it doesn't exist). Append the new link:

```markdown
- [<short title>](./<date>-<slug>.md)
```

Example — adding to an existing section:
```markdown
### 演算法

- [解釋時間複雜度 (Time Complexity)](./2026-05-26-time-complexity.md)
- [解釋空間複雜度 (Space Complexity)](./2026-05-28-space-complexity.md)  ← new
```

Example — creating a new section:
```markdown
### Database

- [解釋 Database Index](./2026-05-30-database-index.md)  ← new section + link
```

## Step 6 — Verify

```bash
npm run docs:build
```

Confirm:
- Build succeeds with no errors
- New post file exists under `docs/.vitepress/dist/<category>/posts/`
- Pinned index page contains the new link

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `pinned: true` missing on the index file | Don't touch the index frontmatter — it already has `pinned: true` |
| External Notion/ChatGPT link left in body | Replace with relative path if the target is another blog post |
| Wrong `layout` value | Always `layout: doc` for posts |
| Category `index-category` doesn't match existing headings | Check exact heading text before adding a new section |
| Forgetting `<ScrollToTopBtn />` | All posts include both `<ArticleTitle />` and `<ScrollToTopBtn />` |
