---
name: Promise Prayer
description: >-
  Use when writing a first-person pastoral prayer grounded in a Bible promise,
  in English and Cantonese, for self/family/church/world, or when running the
  scheduled promise-prayer routine. Avoids repeating verses logged in the last
  30 days.
id: promise-prayer
source: biblemate-native (Grok Bot)
---
# Promise Prayer

Native Grok Bot skill (not from upstream `.grok`). Writes a ready-to-pray first-person prayer grounded in a Bible promise, for the pray-er to speak directly to God.

## Defaults
- English promise text: Christian Standard Bible (CSB)
- Chinese: Chinese Union Version (CUV) for the verse; prayer body in natural spoken Cantonese
- Warm pastoral tone: tender, honest, not theatrical; short enough to pray in a few minutes
- Verse log (required): `/workspace/biblemate_studies/prayers/promise-verse-log.txt`
- Optional archive of full prayers: `/workspace/biblemate_studies/prayers/` (dated `.md`)
- Repo backup of this playbook: `/workspace/grok-bot-biblemate/skills/promise-prayer/SKILL.md`

## Related routine
- Grok Bot routine folder: `promise-prayers-every-2h`
- Schedule (Europe/London): `0 9,11,13,15,17,19,21,23 * * *` (9:00–23:00 every 2 hours, daily)
- Each fire should follow this playbook and deliver the prayer in chat

## Steps
1. **Read and prune the verse log** — Open `/workspace/biblemate_studies/prayers/promise-verse-log.txt`. Drop any dated entries older than 30 days (Europe/London). Keep the header comments. Write the pruned file back.
2. **Choose a fresh promise** — Pick one clear Bible promise (or a tightly related pair). Prefer assurance, presence, peace, provision, guidance, forgiveness, strength, shepherd care, or hope for the nations. The reference(s) must **not** appear in any log entry from the last 30 days (match by normalized reference, e.g. `Isaiah 41:10` or `Philippians 4:6-7`). If a candidate was used recently, pick another.
3. **Quote the promise first** — Prefer fetching exact text via the `bible` skill / `bible_retriever.py` (never invent). English (CSB) with reference, then Chinese (CUV) with 經文出處. Do not paraphrase the quote block.
4. **Write the English prayer** — First person singular (“I / my”). Structure:
   - Praise God for this specific promise.
   - Pray for **myself** (heart, pastoral calling when fitting, obedience, rest).
   - Pray for **my family** (unity, protection, faith, love).
   - Pray for **the church** (congregation, leaders, the weary, unity and witness).
   - Pray for **the world** (nations, peace, the suffering, gospel light, justice tempered with mercy — concrete and pastoral, not partisan).
   - Close with confidence in Christ (Amen).
5. **Write the Cantonese prayer** — Same substance and first-person voice; natural spoken Cantonese.
6. **Enrich lightly** — Time-of-day awareness, one concrete thanksgiving, soft rest in the promise. No third-person “the pastor” narration.
7. **Deliver** in one message, this order: Promise EN → Promise CUV → Prayer EN → 禱告粵語.
8. **Update the verse log** — Append one line: `YYYY-MM-DD\tHH:MM\treference(s)\toptional short note` (Europe/London). Then prune again to 30 days. Do this even for manual `/promise-prayer` runs so the schedule stays unique.
9. **Save full prayer text** only if asked (optional archive under `/workspace/biblemate_studies/prayers/`).

## Log format
```
# comments allowed
2026-09-25	17:10	Isaiah 41:10	manual sample
2026-09-26	09:00	Philippians 4:6-7	scheduled
```

## Enrollment notes
- Register with `update_state` (target `skill`, action `write`, id `promise-prayer`).
- **Do not** Shell-write `/home/box/agent-data/workflows/*/SKILL.md` — that can corrupt the skill catalog snapshot. Edit this repo, then `update_state`.

## Do not
- Reuse a promise reference logged in the last 30 days
- Invent or alter Scripture wording in the quote block
- Skip praying for the world
- Delete or modify trading skills
