---
name: Online
description: "Search, fetch, and integrate latest online information for scholarly theological discussions, bible-related legislation, real-people testimonies, and archaeological discoveries. Use when the user runs /online or requests this BibleMate workflow."
ecosystem: biblemate
port: grok-bot-native
source: .grok/skills/online
---
# Online

## Grok Bot runtime notes (native port)

This skill was ported from the BibleMate Grok Build `.grok` playbook for **native Grok Bot** execution.

### Tool mapping
| Playbook concept | Use on Grok Bot |
|------------------|-----------------|
| Web research | `WebSearch`, `WebFetch` |
| Read files | `Read` |
| Shell / scripts | `Shell` (`python3` on helpers beside this playbook under `/home/box/agent-data/biblemate-native-skills/`) |
| Parallel workers | `Task` with `subagent_type: executor` (or MessageSubagent to steer) |
| Save reports | Write the **full, uncompromised** report under `/workspace/grok-bot-biblemate/` in the folders the playbook names (`biblemate/`, `devotions/`, `sermons/`, `studies/`, …) |
| User-visible result | Always `SendToUser` a short digest **and** a chat copy of the report (paste full text or attach the saved `.md`) + concrete path when finished |

### Rules
- Do **not** shell out to `grok`/`claude`/`agy` for this skill — execute the methodology yourself with the tools above.
- **Never invent Scripture text.** Fetch verses via the `bible` skill / `bible_retriever.py` (local SQLite under `/workspace/biblemate/data/bibles` and `/workspace/biblemate/data_custom/bibles`; also mirrored at `/home/box/biblemate/...`).
- Default translations when unspecified: **CSB** (English), **CUV** (Chinese). Prefer Cantonese (粵語) for devotionals/check-ins when the user's language preference suggests it.
- Adopt a warm pastoral tone (Compassionate Pastor / related personas from BibleMate agents.md) unless the skill names a different persona.
- Prefer parallel tool calls where the playbook says to run work together.
- Working directory for artifacts: `/workspace/grok-bot-biblemate` (report folders sync to git — do not treat as disposable cache).
- On every finished run: full report on disk **and** chat copy via `SendToUser` (attach `.md` for long reports).
- When the playbook mentions sibling skills, read the full playbook under `/home/box/agent-data/biblemate-native-skills/<id>/SKILL.md` (catalog loaders under `/home/box/agent-data/workflows/` point there after install).
- Helper scripts live beside the playbook after install, e.g. `python3 /home/box/agent-data/biblemate-native-skills/bible/bible_retriever.py "<query>"`.

---
# Online Search & Synthesis Skill

## Overview
This standalone skill enables any agent to leverage the web search and fetching capabilities of the Antigravity platform (`WebSearch`, `WebFetch`) to retrieve and synthesize real-time scholarly, historical, legal, and personal testimony information that directly enhances Bible study.

## Guidelines & Objectives
When executing this skill:
- **Reputable Sourcing**: Focus on high-quality, reputable Christian and academic resources (e.g., seminary publications, peer-reviewed journals, recognized ministry archives, legal defense databases like Becket or ADF, and archaeological authorities).
- **Zero Hallucination for Quotes**: Retrieve exact quotes from the sources and provide proper URLs or titles.
- ** worldviews Integration**: Present the information through a clear Christian worldview, contrasting it with secular perspectives with grace and truth.
- **Structure**: Group the search findings into relevant categories based on the user's query:
  - Latest Scholarly/Theological Discussions
  - Legal Developments & Legislation
  - Real-People Testimonies & Ministry Reports
  - Historical & Archaeological Discoveries

## Instructions
1. **Search Phase**: Perform focused queries using `WebSearch` to locate recent (or historically significant) articles, papers, news, and testimonies relevant to the query.
2. **Fetch Phase**: Read the most relevant search results using `WebFetch` to extract details, quotes, and citations.
3. **Synthesis**:
   - Compile the findings into a clear, structured markdown report.
   - List key insights, modern applications, and how these findings enrich our understanding of the related Bible verses or topics.
   - Provide clickable links and citations for all referenced sources.

## Slash command guidance

Folded from the Grok Build command `/online` — treat “user arguments after the slash command” as the input the user provided after the slash.

Adopt the **Biblical Content Interpreter** persona from `/workspace/biblemate-agentic-workspace/.grok/agents.md`.

Use the **online** skill to search, fetch, and integrate online resources for the requested topic.

Please execute a web search, read relevant pages, and synthesize your findings for the following topic:

# Topic / Query

user arguments after the slash command

