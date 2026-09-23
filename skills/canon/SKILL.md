---
name: Canon
description: "Analyze the canonical context and narrative fit of a book, chapter, or passage in light of the whole Bible. Use when the user runs /canon or requests this BibleMate workflow."
ecosystem: biblemate
port: grok-bot-native
source: .grok/skills/canon
---
# Canon

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
# Canon Skill

## Overview
This standalone skill enables any agent to perform a high-quality canon study for a given Bible reference, text, or topic.

## Guidelines & Objectives
When executing this skill:
- Keep explanations biblically accurate and structurally clear.
- Cite specific book, chapter, and verse references for all statements.
- Ensure that the output is comprehensive, addressing all prompt criteria without skipping sections.
- Focus strictly on the requirements of this specific study type.

## Instructions
Analyze the canonical context and narrative fit of a book, chapter, or passage in light of the whole Bible.
Address:
1. **Redemptive-Historical Progression**: Trace how this text fits into the grand narrative of Creation, Fall, Redemption, and Consummation.
2. **Intertextual Connections**: Identify direct citations, allusions, or echoes to previous scriptures, and how later scriptures cite or build on this text.
3. **Covenantal Context**: Explain where this passage lies in relation to the biblical covenants (Noahic, Abrahamic, Mosaic, Davidic, New Covenant).
4. **Typology & Christological Links**: Explain how the narratives, offices (prophet, priest, king), or institutions point typologically to Jesus Christ.

## Slash command guidance

Folded from the Grok Build command `/canon` — treat “user arguments after the slash command” as the input the user provided after the slash.

Adopt the **OT Bible Scholar** (for Old Testament passages/books) or **NT Bible Scholar** (for New Testament passages/books) persona from `/workspace/biblemate-agentic-workspace/.grok/agents.md`.

Bible Canonical Context of a bible book / chapter / passage.
How is this book / chapter / passage connected or linked with other books in the Bible?
What is the canonical context of this given book / chapter / passage in light of the whole canon of the bible?
How does this book / chapter / passage fit into the larger Biblical story in light of the whole canon of the bible?
                               
Please answer all relevant questions pertaining to the following book / chapter / passage with concrete examples:

# Book / Chapter / Passage

user arguments after the slash command

