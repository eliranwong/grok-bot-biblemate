---
name: Promise Prayer
description: >-
  Use when writing a first-person pastoral prayer grounded in a Bible promise,
  in English and Cantonese, for self/family/church/world with one real same-day
  news item (no duplicate news that day) and a required clickable source URL in
  Remarks, or when running the scheduled promise-prayer routine. Avoids
  repeating verses logged in the last 30 days.
---
# Promise Prayer

Write a ready-to-pray first-person prayer grounded in a Bible promise. Output is for the pray-er to speak directly to God.

## Defaults
- English promise text: Christian Standard Bible (CSB)
- Chinese: Chinese Union Version (CUV) for the verse; prayer body in natural spoken Cantonese
- Warm pastoral tone: tender, honest, not theatrical; short enough to pray in a few minutes
- Verse log (required): `/workspace/biblemate_studies/prayers/promise-verse-log.txt`
- News log (required): `/workspace/biblemate_studies/prayers/promise-news-log.txt`
- Optional archive: `/workspace/biblemate_studies/prayers/`

## Steps
1. **Read and prune logs** — Open the verse log and news log. Drop dated entries older than 30 days (Europe/London). Keep header comments. Write pruned files back.
2. **Choose a fresh promise** — One clear Bible promise (or tightly related pair). Must **not** appear in the verse log for the last 30 days. Prefer assurance, presence, peace, provision, guidance, forgiveness, strength, shepherd care, or hope for the nations.
3. **Choose today’s world news (required)** — Use live web search (`WebSearch` / `WebFetch`) for a real current news item suitable for pastoral intercession (suffering, conflict, disaster, peacemaking, refugees, injustice, public grief, or gospel opportunity among the nations). Prefer reputable sources. Build a short `news-key` slug. **Capture a concrete article URL** (https://…) for the chosen story — required for Remarks and the news log.
   - **Same-day rule:** Do **not** reuse a `news-key` (or the same story) already listed in the news log for **today’s** Europe/London date. Pick a different story for later runs the same day.
   - Keep the item factual and pastoral — not partisan campaigning, not graphic sensationalism, not unverified rumor.
   - If search only yields vague headlines without a usable URL, pick another story that has a clear source link. Do not deliver without a link.
4. **Quote the promise first** — Prefer fetching exact text via the `bible` skill / retriever (never invent). English (CSB) with reference, then Chinese (CUV) with 經文出處.
5. **Write the English prayer** — First person (“I / my”):
   - Praise God for this specific promise.
   - Pray for **myself**.
   - Pray for **my family**.
   - Pray for **the church**.
   - Pray for **the world**, **integrating today’s chosen news** naturally (people affected, mercy, peace, wisdom for leaders, gospel hope) without turning the prayer into a news bulletin.
   - Close in Christ (Amen).
6. **Write the Cantonese prayer** — Same substance and first-person voice; natural spoken Cantonese; world section should reflect the same news.
7. **Enrich lightly** — Time of day, one concrete thanksgiving, soft rest in the promise.
8. **Deliver** in one message, this order:
   - Promise EN
   - Promise CUV
   - Prayer EN
   - 禱告粵語
   - **Remarks / Notes** (after both Amens): a brief plain-language note on what the news is about (2–4 sentences), **and always a clickable source link** (markdown `[Source name](https://…)` or bare URL). Label clearly, e.g. `Remarks (news)` / `備註（新聞）`. This is **not** part of the prayer to God. **Never omit the URL.**
9. **Update logs** — Append verse line to the verse log. Append news line to the news log: `YYYY-MM-DD\tHH:MM\tnews-key\tshort-headline\tsource-url` (**source-url is required**, not optional). Prune both to 30 days. Do this for manual and scheduled runs.
10. **Save full prayer text** only if asked.

## Log formats
Verse log:
```
2026-09-25	17:10	Isaiah 41:10	manual sample
```
News log (URL required):
```
2026-09-25	17:40	flooding-south-asia	Monsoon flooding displaces families in South Asia	https://example.com/article
```

## Do not
- Reuse a promise reference logged in the last 30 days
- Reuse the same news-key / same story on the same calendar day
- Invent Scripture, invent news, or skip the world news integration
- Skip the Remarks/Notes after the prayers
- Deliver Remarks without a working news source URL
- Delete or modify trading skills
- Shell-write `/home/box/agent-data/workflows/*/SKILL.md` (use `update_state` only)

## Enrollment notes
- Register with `update_state` (target `skill`, action `write`, id `promise-prayer`).
- **Do not** Shell-write `/home/box/agent-data/workflows/*/SKILL.md`. Edit this repo, then `update_state`.
- Repo backup: `/workspace/grok-bot-biblemate/skills/promise-prayer/SKILL.md`
