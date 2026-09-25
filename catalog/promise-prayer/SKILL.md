---
name: Promise Prayer
description: >-
  Use when the user runs /promise-prayer or requests a first-person pastoral
  prayer grounded in a Bible promise (English + Cantonese; self/family/church/world
  with one real same-day news item, required source URL in Remarks, and 30-day verse log).
---
# Promise Prayer

Native Grok Bot entry for `promise-prayer`.

## Steps
1. Read `/home/box/agent-data/biblemate-native-skills/promise-prayer/SKILL.md` (also `/workspace/grok-bot-biblemate/skills/promise-prayer/SKILL.md`).
2. Execute with Grok Bot tools. Fetch verses via `bible` / retriever — never invent Scripture.
3. Use `WebSearch`/`WebFetch` for one real news item with a concrete https URL; check `promise-news-log.txt` so the same news is not reused on the same Europe/London day.
4. Do **not** call `grok`, `claude`, or `agy`.
5. Deliver Promise EN, Promise CUV, Prayer EN, 禱告粵語, then Remarks/Notes **with clickable source link**. Update verse + news logs (URL required).
