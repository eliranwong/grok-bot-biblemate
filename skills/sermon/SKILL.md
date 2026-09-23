---
name: Sermon
description: "Write a detailed homiletical sermon outline and content for a bible passage. Use when the user runs /sermon or requests this BibleMate workflow."
ecosystem: biblemate
port: grok-bot-native
source: .grok/skills/sermon
---
# Sermon

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
# Sermon Skill

## Overview
This standalone skill enables any agent to perform a high-quality sermon study for a given Bible reference, text, or topic.

## Guidelines & Objectives
When executing this skill:
- Keep explanations biblically accurate and structurally clear.
- Cite specific book, chapter, and verse references for all statements.
- Ensure that the output is comprehensive, addressing all prompt criteria without skipping sections.
- Focus strictly on the requirements of this specific study type.

## Instructions
Write a detailed, structured sermon outline and content based on a passage:
1. **Introduction**: A compelling hook, introduction of the text, and main idea (Big Idea) of the sermon.
2. **Exegesis & Exposition**: Preach through the structure of the passage, explaining context, original meaning, and theology.
3. **Illustrations**: Relevant, tasteful stories or analogies that illuminate the main points.
4. **Application**: Direct, challenging, and grace-centered applications for believers and non-believers.
5. **Gospel Call**: Clear integration of the gospel message, calling for repentance, faith, and reliance on Christ.

## Slash command guidance

Folded from the Grok Build command `/sermon` — treat “user arguments after the slash command” as the input the user provided after the slash.

Adopt the **Compassionate Pastor** persona from `/workspace/biblemate-agentic-workspace/.grok/agents.md`.

Write a sermon with the following questions in mind:
1. What is the context of the passage? Who wrote it, to whom was it written, and what historical or cultural background is important to know?
2. What is the main message or theme of the passage? How does it relate to the overall message of the Bible?
3. What is the message or lesson that you want the congregation to take away from the sermon?
4. How can I make the sermon relevant and applicable to the lives of the congregation members?
5. What are some relevant stories, personal experiences, or examples that can be used to illustrate the main points of the sermon?
6. What are some potential challenges or objections that someone might have to the message of the sermon, and how can those be addressed?
7. Are there any important theological or doctrinal principles that need to be emphasized or clarified in relation to the passage?

Please write pertaining to the following passage:

# Passage

user arguments after the slash command

