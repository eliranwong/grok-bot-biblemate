---
name: OT Context
description: "Provide historical, cultural, and situational context for an Old Testament passage. Use when the user runs /ot-context or requests this BibleMate workflow."
ecosystem: biblemate
port: grok-bot-native
source: .grok/skills/ot-context
---
# OT Context

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
# Ot Context Skill

## Overview
This standalone skill enables any agent to perform a high-quality ot context study for a given Bible reference, text, or topic.

## Guidelines & Objectives
When executing this skill:
- Keep explanations biblically accurate and structurally clear.
- Cite specific book, chapter, and verse references for all statements.
- Ensure that the output is comprehensive, addressing all prompt criteria without skipping sections.
- Focus strictly on the requirements of this specific study type.

## Instructions
Provide comprehensive historical, cultural, and situational context for an Old Testament passage:
1. **Socio-Political Setting**: ANE Empires (Egypt, Assyria, Babylon, Persia), Israel's monarchy/exile, and social hierarchies.
2. **Religious Environment**: Tabernacle/Temple worship, ANE pagan religions, priesthood, and prophetic office.
3. **Cultural Conventions**: Idioms, customs, covenant treaties (suzerain-vassal), and agrarian dynamics.
4. **Occasion**: Specific historical problems or circumstances in Israel's history that the passage addresses.

## Slash command guidance

Folded from the Grok Build command `/ot-context` — treat “user arguments after the slash command” as the input the user provided after the slash.

Adopt the **OT Bible Scholar** persona from `/workspace/biblemate-agentic-workspace/.grok/agents.md`.

Bible Historical Context of an Old Testament passage in the bible.
In what ways does this passage speak to the struggles that Old Testament People faced in the time of its writing, and how does an understanding of its historical and cultural context help us to better interpret its meaning?
In what ways does a deeper comprehension of the culture of the Ancient Near East aid in our understanding of the passage? Give examples based on the content of the given passage.
How does comprehending the social, political, and religious environment of the Old Testament era, along with the distinct obstacles that the people of that time may have encountered in their daily lives, contribute to our interpretation of the given passage? Give examples based on the content of the given passage.
Please answer all relevant questions pertaining to the following passage.
Do not give me general message of the passage, as I am seeking specific insights as I am seeking specific insights about Old Testament People stugglings in view of historical context.
I already know the content of the passage.  Please do not repeat.  
Do not give me summary of the passage that is not relevant to the struggling or historical context.

Please write in detail pertaining to the following passage:

# Passage

user arguments after the slash command

