# Promise Prayer (`/promise-prayer`)

Bilingual first-person pastoral prayers grounded in a Bible promise — for Eliran (pastor) to pray aloud for self, family, church, and the world.

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
| `/workspace/biblemate_studies/prayers/` | Optional dated prayer archives |
| `/workspace/biblemate_studies/prayers/PROMISE_PRAYER_SKILL.md` | Working archive copy (safe to edit) |

## Scheduled routine

- **Name:** Promise prayers (every 2h)
- **Folder id:** `promise-prayers-every-2h`
- **Cron (Europe/London):** `0 9,11,13,15,17,19,21,23 * * *`
- **Times:** 9:00, 11:00, 13:00, 15:00, 17:00, 19:00, 21:00, 23:00 daily (including weekends)

Each run should follow the playbook, deliver the prayer in chat, and update the verse log.

## Verse log

- Format: `YYYY-MM-DD\tHH:MM\treference(s)\tnote`
- On every run (manual or scheduled): prune entries older than 30 days, choose a promise **not** in the log, append the new reference.
- Do not reuse the same normalized reference within 30 days (e.g. `Isaiah 41:10`, `Philippians 4:6-7`).

## Defaults

- CSB (English) + CUV (Chinese) for the quoted promise
- Spoken Cantonese for the prayer body
- Warm pastoral tone; first person (“I / my”)
- Never invent Scripture — fetch via `/bible` / `bible_retriever.py` when possible

## Register / refresh

```text
update_state → target skill, action write, id promise-prayer
```

**Do not** Shell-copy or overwrite `/home/box/agent-data/workflows/*/SKILL.md` for this skill — that path has caused brain-docs catalog “without a size” errors. Prefer repo edit + `update_state`. After `install_to_box.sh`, still call `update_state` for autocomplete.

## Related

- Older `/prayer` playbook (different skill) remains in this pack for general prayer study content.
- Trading skills must never be deleted or overwritten by BibleMate work.
