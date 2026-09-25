---
name: BibleMate
description: >-
  Use when the user runs /biblemate or asks for a full BibleMate study (passage,
  book, topical, or sermon/devotion pipeline). Orchestrates many unenrolled leaf
  playbooks under biblemate-native-skills across fixed study phases — not a
  single skill.
---
# BibleMate

Native Grok Bot entry for `biblemate`.

## Steps
1. Read `/home/box/agent-data/biblemate-native-skills/biblemate/SKILL.md`.
2. Orchestrate **multiple** leaf playbooks (never one skill). Use Grok Bot tools only.
3. Do **not** call `grok`, `claude`, or `agy`.
4. Deliver digest + final report; artifacts under `/workspace/grok-bot-biblemate/biblemate/`.
