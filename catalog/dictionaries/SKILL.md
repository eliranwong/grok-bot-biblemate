---
name: Dictionaries
description: >-
  Use when the user runs /dictionaries or requests this BibleMate workflow (native Grok Bot port).
---
# Dictionaries

Native Grok Bot port of the BibleMate playbook `dictionaries`.

## Steps
1. Read the full playbook at `/home/box/agent-data/biblemate-native-skills/dictionaries/SKILL.md` with `Read`.
2. Execute that methodology with Grok Bot tools (`Read`, `Shell`, `WebSearch`, `WebFetch`, `Task`/executor as needed).
3. Do **not** call `grok`, `claude`, or `agy` for this skill.
4. Write the full report under `/workspace/grok-bot-biblemate/` in the folders the playbook specifies.
5. When finished, `SendToUser` a short digest **and** a chat copy of the report (paste or attach) plus concrete paths.

