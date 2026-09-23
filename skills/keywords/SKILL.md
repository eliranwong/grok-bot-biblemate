---
name: Keywords
description: "Extract key words, theological terms, and analyze original Greek/Hebrew meanings. Use when the user runs /keywords or requests this BibleMate workflow."
ecosystem: biblemate
port: grok-bot-native
source: .grok/skills/keywords
---
# Keywords

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
# Keywords Skill

## Overview
This standalone skill enables any agent to perform a high-quality keywords study for a given Bible reference, text, or topic.

## Guidelines & Objectives
When executing this skill:
- Keep explanations biblically accurate and structurally clear.
- Cite specific book, chapter, and verse references for all statements.
- Ensure that the output is comprehensive, addressing all prompt criteria without skipping sections.
- Focus strictly on the requirements of this specific study type.

## Instructions
Identify and analyze key words and theological terms in a passage. For each term:
1. **Original Languages**: Provide the Hebrew/Greek lemma, transliteration, and morphology.
2. **Semantic Range**: Explain how the word is used in the ancient world, both biblically and extrabiblically.
3. **Contextual Meaning**: Determine the specific nuance of the term in this passage.
4. **Theological Significance**: Link the word to broader doctrines and theological concepts.

## Slash command guidance

Folded from the Grok Build command `/keywords` — treat “user arguments after the slash command” as the input the user provided after the slash.

Adopt the **OT Bible Scholar** (for Old Testament passages) or **NT Bible Scholar** (for New Testament passages) persona from `/workspace/biblemate-agentic-workspace/.grok/agents.md`.

Identify key words in the content given below.
Elaborate on their importance in comprehending the context and the bible as a whole.
I want your elaboration to be comprehensive and informative.
Remember, in your writing, please provide me with concrete examples from the Bible and the bible references from the text you are citing.

# Content

user arguments after the slash command

