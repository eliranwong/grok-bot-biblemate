---
name: Promise Prayer
description: >-
  Use when the user runs /promise-prayer or requests a first-person pastoral
  prayer grounded in a Bible promise (English + Cantonese; self/family/church/world;
  30-day verse log).
---
# Promise Prayer

Native Grok Bot entry for `promise-prayer`.

## Steps
1. Read the full playbook at `/home/box/agent-data/biblemate-native-skills/promise-prayer/SKILL.md` with `Read` (source of truth also in `/workspace/grok-bot-biblemate/skills/promise-prayer/SKILL.md`).
2. Execute that methodology with Grok Bot tools (`Read`, `Shell`, `WebSearch`, `WebFetch`, `Task`/executor as needed). Prefer fetching verses via the `bible` skill / retriever — never invent Scripture.
3. Do **not** call `grok`, `claude`, or `agy` for this skill.
4. Maintain `/workspace/biblemate_studies/prayers/promise-verse-log.txt` (prune to 30 days; append the reference used).
5. When finished, `SendToUser` the full prayer in the playbook order (Promise EN, Promise CUV, Prayer EN, 禱告粵語). Optionally archive under `/workspace/biblemate_studies/prayers/` if asked.
