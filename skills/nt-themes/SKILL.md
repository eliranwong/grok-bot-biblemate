---
name: NT Themes
description: "Analyze the theological and doctrinal themes of a New Testament passage. Use when the user runs /nt-themes or requests this BibleMate workflow."
ecosystem: biblemate
port: grok-bot-native
source: .grok/skills/nt-themes
---
# NT Themes

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
# Nt Themes Skill

## Overview
This standalone skill enables any agent to perform a high-quality nt themes study for a given Bible reference, text, or topic.

## Guidelines & Objectives
When executing this skill:
- Keep explanations biblically accurate and structurally clear.
- Cite specific book, chapter, and verse references for all statements.
- Ensure that the output is comprehensive, addressing all prompt criteria without skipping sections.
- Focus strictly on the requirements of this specific study type.

## Instructions
Analyze key theological and doctrinal themes in a New Testament passage:
1. **Doctrinal Identification**: Trace specific themes (e.g., Grace, Justification, Sanctification, Kingdom).
2. **Intertextual Support**: Contrast or link these themes with other parts of the Bible.
3. **Christological Resolution**: How the themes find their ultimate fulfillment in the person and work of Jesus Christ.

## Slash command guidance

Folded from the Grok Build command `/nt-themes` — treat “user arguments after the slash command” as the input the user provided after the slash.

Adopt the **Systematic Theologian** persona from `/workspace/biblemate-agentic-workspace/.grok/agents.md`.

Bible Themes in a New Testament passage.
What are the key themes expressed in this passage?  Please elaborate on each theme in details.  
Explain how biblical Greek studies help us understand each theme.  Povide illustration that aid our understanding, if possible.
What are the theological implications of this passage, and how does it contribute to our understanding of God's character and plan for humanity?
How does the Old Testament contribute to our comprehension of this New Testament passage? Give examples and quote related Old Testament passages.
How does the message conveyed in this passage impact our connection with God?
Please answer all relevant questions pertaining to the following passage.
Do not give me historical context of the passage, as I already know them. 
Do not give me general information about the passage, as I am seeking specific themes, theological implications and connection with God.

Please answer all relevant questions pertaining to the following passage:

# Passage

user arguments after the slash command

