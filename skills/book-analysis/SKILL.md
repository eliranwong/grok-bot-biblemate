---
name: Book Analysis
description: "Produce a comprehensive introduction, historical background, and overview of a bible book. Use when the user runs /book-analysis or requests this BibleMate workflow."
ecosystem: biblemate
port: grok-bot-native
source: .grok/skills/book-analysis
---
# Book Analysis

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
# Book Analysis Skill

## Overview
This standalone skill enables any agent to perform a high-quality introduce book study for a given Bible reference, text, or topic.

## Guidelines & Objectives
When executing this skill:
- Always run the python script located at `/home/box/agent-data/biblemate-native-skills/book-analysis/book_analysis_retriever.py` to search the local database for baseline book introductions.
- Execute the script using: `python3 /home/box/agent-data/biblemate-native-skills/book-analysis/book_analysis_retriever.py "<Book>"` (you can also pass language options like `--sc` or `--tc` if a Chinese translation is preferred, or the script will auto-detect Chinese characters).
- Retrieve and use the local database output as the baseline information. Combine it with your assigned persona, theological perspective, and relevant Scripture references to fully expound the book in detail.
- Keep explanations biblically accurate and structurally clear.
- Cite specific book, chapter, and verse references for all statements.
- Ensure that the output is comprehensive, addressing all prompt criteria without skipping sections.
- Focus strictly on the requirements of this specific study type.

## Instructions
Produce a comprehensive scholarly introduction and overview of a bible book. Integrate and fully expound the retrieved baseline data (Overview, Structural Outline, Logical Flow, Historical Setting, Themes, Keywords, Theology, Canonical Placement, Practical Living, Summary) to address:
1. **Historical Background**: Authorship, date, provenance, and target audience. Expand upon the retrieved Historical Setting and Overview.
2. **Literary Context**: Genre, structure, and style. Elaborate on the Structural Outline and Logical Flow retrieved from the database.
3. **Occasion and Purpose**: Why the book was written and the issues it addresses.
4. **Theological Themes**: Core doctrines, covenantal focus, and major teachings. Deepen the Themes, Keywords, and Theology retrieved from the database.
5. **Christological Focus**: How the book reveals Jesus Christ and the Gospel.
6. **Canonical Placement & Practical Application**: Setting the book's location in the grand storyline of scripture and outline practical applications for modern living. Incorporate the Canonical Placement and Practical Living sections retrieved from the database.

## Slash command guidance

Folded from the Grok Build command `/book-analysis` — treat “user arguments after the slash command” as the input the user provided after the slash.

Adopt the **OT Bible Scholar** (for Old Testament books) or **NT Bible Scholar** (for New Testament books) persona from `/workspace/biblemate-agentic-workspace/.grok/agents.md`.

First, run the database retriever script to search the local database for baseline book introduction data:
`python3 /home/box/agent-data/biblemate-native-skills/book-analysis/book_analysis_retriever.py "$1"` (use language flags like `--sc` or `--tc` if query is in Chinese).

Then, write a detailed introduction on the book in the bible, integrating and fully expounding the retrieved baseline database contents (Overview, Structural Outline, Logical Flow, Historical Setting, Themes, Keywords, Theology, Canonical Placement, Practical Living, Summary) while considering all the following questions:
1. Who is the author or attributed author of the book?
2. What is the date or time period when the book was written?
3. What is the main theme or purpose of the book?
4. What are the significant historical events or context surrounding the book?
5. Are there any key characters or figures in the book?
6. What are some well-known or significant passages from the book?
7. How does the book fit into the overall structure and narrative of the Bible?
8. What lessons or messages can be learned from the book?
9. What is the literary form or genre of the book (e.g. historical, prophetic, poetic, epistle, etc.)?
10. Are there any unique features or controversies surrounding the book?
I want the introduction to be comprehensive and informative, fully expounding the retrieved details.
When you explain, quote specific words or phrases from relevant bible verses, if any.
Answer all these relevant questions mentioned above, in the introduction, pertaining to the following bible book.

# Bible book name

user arguments after the slash command

