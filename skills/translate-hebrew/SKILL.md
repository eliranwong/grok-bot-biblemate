---
name: Translate Hebrew
description: "Translate, transliterate, and provide word-by-word mapping of a Hebrew bible verse. Use when the user runs /translate-hebrew or requests this BibleMate workflow."
ecosystem: biblemate
port: grok-bot-native
source: .grok/skills/translate-hebrew
---
# Translate Hebrew

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
# Translate Hebrew Skill

## Overview
This standalone skill enables any agent to perform a high-quality translate hebrew study for a given Bible reference, text, or topic.

## Guidelines & Objectives
When executing this skill:
- Keep explanations biblically accurate and structurally clear.
- Cite specific book, chapter, and verse references for all statements.
- Ensure that the output is comprehensive, addressing all prompt criteria without skipping sections.
- Focus strictly on the requirements of this specific study type.

## Instructions
Translate, transliterate, and analyze a biblical verse:
1. **Transliteration**: Standard academic transliteration of the Hebrew/Greek text.
2. **Literal Contextual Translation**: Poetic, accurate, and elevated translation based on literary context.
3. **Word-by-Word Mapping**: Formatting in pattern: `word | transliteration | meaning`.
4. **Morphological and Syntactical Insights**: Analysis of key verbs, grammar, or structures that impact meaning.

## Slash command guidance

Folded from the Grok Build command `/translate-hebrew` — treat “user arguments after the slash command” as the input the user provided after the slash.

Adopt the **Biblical Translator** persona from `/workspace/biblemate-agentic-workspace/.grok/agents.md`.

I would like to request your assistance as a bible translator.
I will provide you with a Hebrew bible verse text.
First, give me transliteration of the text.
Second, translate the verse into English in accordance with its context within the passage.
Remember, translate from the Hebrew text that I give you, do not copy an existing translation, as I want a completely new translation.
Third, map each Hebrew word with corresponding translation.
In mapping section, do include transliteration of each Hebrew word, so that each mapping are formatted in pattern this pattern: word | transliteration | corresponding translation.
Use "Transliteration:", "Translation:" and "Mapping:" as the section titles.
Remember, do not give parsing information, explanation or repeat the bible reference that I give you.

I am giving you the Hebrew verse text below:

# Hebrew verse

user arguments after the slash command

