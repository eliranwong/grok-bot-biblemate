---
name: Chapter Summary
description: "Generate a detailed summary, structure, and theological interpretation of a bible chapter. Use when the user runs /chapter-summary or requests this BibleMate workflow."
ecosystem: biblemate
port: grok-bot-native
source: .grok/skills/chapter-summary
---
# Chapter Summary

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
# Chapter Summary Skill

## Overview
This standalone skill enables any agent to perform a high-quality chapter summary study for a given Bible reference, text, or topic.

## Guidelines & Objectives
When executing this skill:
- Always run the python script located at `/home/box/agent-data/biblemate-native-skills/chapter-summary/chapter_summary_retriever.py` to search the local database for baseline chapter summaries.
- Execute the script using: `python3 /home/box/agent-data/biblemate-native-skills/chapter-summary/chapter_summary_retriever.py "<Book> <Chapter>"` (you can also pass language options like `--sc` or `--tc` if a Chinese translation is preferred, or the script will auto-detect Chinese characters).
- Retrieve and use the local database output as the baseline information. Combine it with your assigned persona, theological perspective, and relevant Scripture references to fully expound the chapter in detail.
- Keep explanations biblically accurate and structurally clear.
- Cite specific book, chapter, and verse references for all statements.
- Ensure that the output is comprehensive, addressing all prompt criteria without skipping sections.
- Focus strictly on the requirements of this specific study type.

## Instructions
Write a detailed, scholarly interpretation on a bible chapter. Provide a structured and comprehensive analysis using these sections:
1. **Overview & Context**: Setting the chapter's historical, cultural, and literary location in the book. Expand upon the retrieved baseline summary's overview.
2. **Structural Outline**: Detailed division of the chapter into passages, highlighting logical progression and chiasms. Elaborate on the structural outline retrieved from the database.
3. **Thematic Exegesis**: In-depth analysis of major theological themes, quoting key words or phrases from the original text (or standard English/Chinese versions). Deepen the themes retrieved from the database.
4. **Comparative Interpretations**: How major historical and contemporary scholars or theologians have interpreted key debates within this chapter.
5. **Canonical & Covenantal Links**: Connecting this chapter to the broader redemptive storyline of Scripture.
6. **Pastoral & Practical Application**: Life applications grounded in the chapter's theological message.


## Slash command guidance

Folded from the Grok Build command `/chapter-summary` — treat “user arguments after the slash command” as the input the user provided after the slash.

Adopt the **OT Bible Scholar** (for Old Testament chapters) or **NT Bible Scholar** (for New Testament chapters) persona from `/workspace/biblemate-agentic-workspace/.grok/agents.md`.

Use the **chapter-summary** skill to retrieve baseline chapter summary data.

Always execute:
`python3 /home/box/agent-data/biblemate-native-skills/chapter-summary/chapter_summary_retriever.py "$1 $2 $3 $4 $5"`
(and add any language options like `--sc` or `--tc` if the input is in Chinese or requested).

Use the retrieved database output as the baseline information. Combine it with your assigned scholar persona and relevant scripture references to write a detailed, comprehensive, and informative interpretation on the bible chapter, addressing all of the following questions:
1. What is the overview of the chapter? (Expand on the overview retrieved from the database)
2. How are the verses in this chapter structured or organized? (Elaborate on the structural outline retrieved from the database)
3. Are there any key verses or passages in the chapter? (Cite and explain them)
4. Are there any significant characters, events, or symbols in the chapter?
5. What is the main themes or messages of the chapter? (Deepen the themes retrieved from the database)
6. What historical or cultural context is important to understand the chapter?
7. How have theologians, scholars, or religious leaders interpreted this chapter?
8. Are there any popular interpretations or controversies related to this chapter?
9. How does this chapter relate to other chapters, books, or themes in the Bible?
10. What lessons or morals can be taken from the chapter?

When you explain, quote specific words or phrases from relevant bible verses. All quoted verse content must be verified and retrieved using the local `bible` skill rather than from memory.

# Bible chapter

user arguments after the slash command

