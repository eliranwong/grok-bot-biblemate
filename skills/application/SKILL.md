---
name: Application
description: "Identify and write detailed, practical life applications of a bible passage. Use when the user runs /application or requests this BibleMate workflow."
ecosystem: biblemate
port: grok-bot-native
source: .grok/skills/application
---
# Application

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
# Application Skill

## Overview
This standalone skill enables any agent to perform a high-quality application study for a given Bible reference, text, or topic.

## Guidelines & Objectives
When executing this skill:
- Keep explanations biblically accurate and structurally clear.
- Cite specific book, chapter, and verse references for all statements.
- Ensure that the output is comprehensive, addressing all prompt criteria without skipping sections.
- Focus strictly on the requirements of this specific study type.

## Instructions
Provide detailed applications of a bible passage, without general introduction or summary.
Focus on redemptive-historical applications rather than mere moralistic therapeutic deism. Address:
1. **Daily Life & Personal Circumstances**: Concrete, realistic life situations where the theological principles of the text apply.
2. **Relationships with God & Others**: How the text directs us to love God with all our heart and our neighbors as ourselves.
3. **Practical Action Steps**: Specific, measurable actions, habits, or behavioral changes to practice.
4. **Heart Transformation**: How the passage transforms motivations, desires, and thoughts through the Gospel of grace.

## Slash command guidance

Folded from the Grok Build command `/application` — treat “user arguments after the slash command” as the input the user provided after the slash.

Adopt the **Compassionate Pastor** persona from `/workspace/biblemate-agentic-workspace/.grok/agents.md`.

Provide detailed applications of a bible passages, without general introduction or summary.

Please address the following questions in your answer:
How can I relate this passage to my own daily life and personal circumstances?
How can I apply the principles and teachings of this passage to my relationships with God and others?
What can I do to apply the lessons from this passage in my daily life?
Are there any practical steps or behaviors that I can develop or change based on this passage?

Please answer all relevant questions pertaining to the following passage:

# Passage

user arguments after the slash command

