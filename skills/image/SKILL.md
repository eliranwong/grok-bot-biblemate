---
name: Image
description: "Generate bible-related images with Grok Build Imagine tools and place them in the images/ directory. Use when the user runs /image or requests this BibleMate workflow."
ecosystem: biblemate
port: grok-bot-native
source: .grok/skills/image
---
# Image

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
# Image Generation Skill (Grok Bot)

## Overview
Generate bible-related images with **Grok Bot's native Imagine tools**
(`image_gen` / `image_edit`), then place a durable copy in the repository's
`images/` directory with a timestamped, slugified filename.

This skill is **self-contained for Grok Bot**. It does **not** use Google
Antigravity, the `google-antigravity` SDK, or any `.agents/` image script.

## Tools

| Situation | Tool |
|-----------|------|
| New image from a text prompt (default) | `image_gen` |
| Restyle, iterate, or vary an existing image | `image_edit` |
| Place the result under `images/` with BibleMate naming | `image_placer.py` (below) |

## Workflow

1. **Craft the prompt.** Prefer a concrete biblical scene, subject, setting,
   style, lighting, and mood in natural prose (about 2–5 sentences). If the user
   supplies a detailed prompt, use it (refined only if needed for clarity).
2. **Choose aspect ratio** for `image_gen` when helpful:
   - `16:9` — landscape scenes, banners
   - `1:1` — icons, social thumbnails
   - `9:16` — phone / story format
   - `4:3` / `3:4` — classic illustration framing
   - `auto` — when the user does not specify
3. **Generate** with the Grok tool (do **not** call any Antigravity API or script):
   - New image → `image_gen` with `prompt` and optional `aspect_ratio`
   - Edit / variation → `image_edit` with `prompt` and the source `image` path
4. **Place** the returned file into the repo `images/` directory:
   ```bash
   python3 /home/box/agent-data/biblemate-native-skills/image/image_placer.py "<absolute-or-relative-source-path>" "<original user prompt or title>"
   ```
   The helper prints a line like:
   `SUCCESS: Generated image saved at images/YYYY-MM-DD-HH-MM-SS_<slug>.png`
5. **Report** to the user: confirm the saved `images/...` path, briefly describe
   what was generated, and (when useful) show the session-relative path returned
   by `image_gen` / `image_edit` as well.

## Prompt craft (bible scenes)

- Lead with the subject (who / what), then action, place, era cues, style, and mood.
- Prefer historically and textually respectful depictions; avoid sensational or
  anachronistic detail unless the user asks for a specific artistic style.
- State what to include; avoid long negative-prompt lists.
- For labeled diagrams, charts, or exact scripture text on the image, prefer
  building the asset with code (HTML/CSS) rather than pure image generation —
  image models often garble precise text.

## Failures

- On a moderation or safety block: stop; do not rephrase to evade filters. Tell
  the user and offer a different creative direction.
- If generation succeeds but placement fails, report both the tool output path
  and the placer error so the user can still find the raw file.

## Do not

- Run `.agents/skills/image/image_generator.py` or any `google.antigravity` code.
- Invent image-tool parameters beyond those provided by Grok Bot.
- Quote or invent Bible verse text on the image unless the user explicitly wants
  on-image text (and even then, verify accuracy if text must be exact).

## Slash command guidance

Folded from the Grok Build command `/image` — treat “user arguments after the slash command” as the input the user provided after the slash.

Adopt the **Verse Scripter** persona from `/workspace/biblemate-agentic-workspace/.grok/agents.md`.

Use the **image** skill to generate the bible-related images.

Please generate a bible-related image based on the input prompt below:

# Input

user arguments after the slash command

