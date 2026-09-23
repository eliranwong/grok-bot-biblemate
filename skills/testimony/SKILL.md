---
name: Testimony
description: "Retrieve verified real-life and missionary testimonies from local database or online research, including background details and fact-checking sources. Use when the user runs /testimony or requests this BibleMate workflow."
ecosystem: biblemate
port: grok-bot-native
source: .grok/skills/testimony
---
# Testimony

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
# Testimony Retrieval & Generation Skill

## Overview
This standalone skill enables any agent to find, verify, and write real-life or missionary-historical testimonies that address the user's specific input, struggle, or sermon topic. All testimonies must be completely real and verified.

## Guidelines & Objectives
When executing this skill:
- **Absolute Integrity**: The testimony must be completely real. Never fabricate or embellish details.
- **Background & Context**: Provide historical context, biographical details of the key persons, and locations.
- **Verification & Sources**: List books, articles, or reputable website URLs along with brief notes on how a user can fact-check the testimony.
- **Scripture Integrity**: Retrieve all related scriptures using the local `bible` skill (e.g. `python3 /home/box/agent-data/biblemate-native-skills/bible/bible_retriever.py "<query>"`). Never quote scripture from memory.
- **Save Study Output**: Save the complete final testimony document to the `biblemate/` directory with the timestamp prefix in the format `YYYY-MM-DD-HH-MM-SS_testimony_<slug>.md` and confirm the path.

## Instructions
1. **Search Local Registry**:
   Run the local python retriever script first to see if a matching historical/missionary testimony is available in the local database:
   ```bash
   python3 /home/box/agent-data/biblemate-native-skills/testimony/testimony_retriever.py "<query>"
   ```
2. **Perform Online Search (if needed)**:
   If no direct match is found in the local registry, or if a specific modern scenario is queried:
   - Use the `WebSearch` tool to search for real-life testimonies, modern missionary reports, or news articles.
   - Use the `WebFetch` tool to fetch pages and verify the details.
   - Compile the narrative, biographical background, and fact-checking sources.
   - Never invent or embellish a testimony when sources cannot be verified.
3. **Retrieve and Quote Bible Passages**:
   Identify the theological themes or verses connected to the testimony, and retrieve the exact text of those verses using the local `bible` skill.
4. **Draft and Integrate**:
   - Write a compelling narrative fit for encouragement or preaching.
   - Structure the output clearly: Title, Biographical Info, Narrative Story, Scripture Connection, and Verification/Sources.
5. **Save the Output**:
   - If not saved automatically by the script, save the compiled testimony document to the `biblemate/` directory as `biblemate/YYYY-MM-DD-HH-MM-SS_testimony_<slug>.md`.
   - Confirm the saved file path.

## Slash command guidance

Folded from the Grok Build command `/testimony` — treat “user arguments after the slash command” as the input the user provided after the slash.

Adopt the **Passionate Evangelist** persona from `/workspace/biblemate-agentic-workspace/.grok/agents.md`.

Use the **testimony** skill to retrieve or research the testimony.

Please write a verified, real-life or missionary-historical testimony matching the user's input. The testimony must be completely real (never fake or fabricated) and must be structured with biographical background details and clickable sources for user fact-checking.

In your final response:
1. Present the testimony narrative in an encouraging and powerful evangelistic style.
2. Outline the historical, biographical, and geographical context.
3. List connected Bible verses, making sure to fetch their exact text using the `/bible` command (do not quote from memory).
4. Provide the list of books, articles, and websites where users can verify and fact-check the testimony.
5. Save the output to the `biblemate/` directory with a timestamp prefix and confirm the file path.

# User Input

user arguments after the slash command

