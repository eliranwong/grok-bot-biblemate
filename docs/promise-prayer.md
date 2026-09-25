# Promise Prayer (`/promise-prayer`)

Bilingual first-person pastoral prayers grounded in a Bible promise — for Eliran (pastor) to pray aloud for self, family, church, and the world, with one real news item for the day woven into the world section.

## Files in this repo

| Path | Role |
|------|------|
| `skills/promise-prayer/SKILL.md` | Full playbook (source of truth) |
| `catalog/promise-prayer/SKILL.md` | Thin slash loader |
| `docs/promise-prayer.md` | This guide |

## Runtime paths (box)

| Path | Role |
|------|------|
| `/home/box/agent-data/biblemate-native-skills/promise-prayer/SKILL.md` | Installed playbook |
| Enrolled skill id `promise-prayer` | `/` autocomplete via `update_state` only |
| `/workspace/biblemate_studies/prayers/promise-verse-log.txt` | 30-day verse uniqueness log |
| `/workspace/biblemate_studies/prayers/promise-news-log.txt` | Same-day news uniqueness log |
| `/workspace/biblemate_studies/prayers/` | Optional dated prayer archives |

## Scheduled routine

- **Name:** Promise prayers (every 2h)
- **Folder id:** `promise-prayers-every-2h`
- **Cron (Europe/London):** `0 9,11,13,15,17,19,21,23 * * *`

## World news (required)

1. Look up a real current news item (`WebSearch` / `WebFetch`) suitable for pastoral intercession.
2. Integrate it into the **world** section of both English and Cantonese prayers (people, mercy, peace, wisdom — not a partisan rant).
3. After both Amens, add **Remarks / Notes** (備註) briefly explaining the news (2–4 sentences) with source when available. Remarks are for the reader, not prayed to God.
4. **Same-day rule:** do not reuse the same `news-key` / story already in `promise-news-log.txt` for today’s Europe/London date. Later runs the same day need a different story.

### News log format
```
YYYY-MM-DD\tHH:MM\tnews-key\tshort-headline\tsource-url-optional
```

## Verse log

- Avoid repeating the same promise reference within 30 days.
- Format: `YYYY-MM-DD\tHH:MM\treference(s)\tnote`

## Defaults

- CSB + CUV for the quoted promise; spoken Cantonese for the prayer body
- Warm pastoral first-person tone
- Never invent Scripture or invent news

## Register / refresh

`update_state` → skill write, id `promise-prayer`. Do **not** Shell-overwrite `workflows/*/SKILL.md`.

## Related

- Trading skills must never be deleted or overwritten by BibleMate work.
