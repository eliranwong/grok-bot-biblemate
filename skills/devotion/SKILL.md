---
name: Devotion
description: "Write a spiritual devotional reflection, practical application, and prayer for a passage. Use when the user runs /devotion or requests this BibleMate workflow."
ecosystem: biblemate
port: grok-bot-native
source: .grok/skills/devotion
---
# Devotion

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
# Devotion Skill

## Overview
This standalone skill enables any agent to perform a high-quality devotion study for a given Bible reference, text, or topic.

## Guidelines & Objectives
When executing this skill:
- Keep explanations biblically accurate and structurally clear.
- Cite specific book, chapter, and verse references for all statements.
- Ensure that the output is comprehensive, addressing all prompt criteria without skipping sections.
- Focus strictly on the requirements of this specific study type.

## Instructions
Write a detailed devotional reflection on a bible passage. Ensure the tone is pastoral, engaging, and deep. Address:
1. **Expository Focus**: Highlight a central theological truth of the passage.
2. **Life Integration**: Connect this truth to contemporary human experiences, struggles, and emotions.
3. **Gospel Connection**: Demonstrate how the passage points to God's grace in Jesus Christ.
4. **Application**: Call to action or reflection questions encouraging personal change.
5. **Pastoral Prayer**: Write a concluding scriptural prayer in the first person.

## Slash command guidance

Folded from the Grok Build command `/devotion` — treat “user arguments after the slash command” as the input the user provided after the slash.

Adopt the **Compassionate Pastor** persona from `/workspace/biblemate-agentic-workspace/.grok/agents.md`.

Write a devotion on a bible passage, based on the following guidance:
1. Get a full understanding of its meaning and context.
2. Reflect on how the passage applies to your own life and experiences.
3. Consider what message or lesson God may be trying to communicate through the passage.
4. Decide on a specific theme or topic you want to focus on in your devotion, based on the Bible passage.
5. Use personal anecdotes, relevant scripture references, and practical applications to help illustrate and reinforce your message.
6. End your devotion with a call to action or a prayer that encourages readers to apply the lesson to their own lives.
7. Edit and revise your devotion to ensure that it is clear, concise, and impactful.
I am already familiar with the contents of the passage, please refrain from providing general introduction or summary.
I want deep insights about devotions.

Please write pertaining to the following passage:

# Passage

user arguments after the slash command

