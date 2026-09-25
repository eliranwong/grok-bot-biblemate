# Grok Bot BibleMate Ecosystem — Agent Rules

This repository is an AI-driven Bible study ecosystem for **Grok Bot** (native skills), not Grok Build.

> Never invent Scripture text. Fetch every verse via the local `bible` skill / `bible_retriever.py`. Default translations when unspecified: **CSB** (English), **CUV** (Chinese). Prefer warm pastoral tone; prefer 粵語 for devotionals/check-ins when language preference suggests it.

## Prefer native skills

For `/promise-prayer` and the every-2-hour promise routine, follow [`docs/promise-prayer.md`](docs/promise-prayer.md) and keep `/workspace/biblemate_studies/prayers/promise-verse-log.txt` unique for 30 days. Register skills with `update_state` only — do **not** Shell-overwrite `/home/box/agent-data/workflows/*/SKILL.md`.

1. **Use native playbooks** under `/home/box/agent-data/biblemate-native-skills/<id>/SKILL.md` (installed from `skills/` in this repo).
2. **Catalog loaders** under `/home/box/agent-data/workflows/<id>/SKILL.md` are thin entry points — they `Read` the full playbook and execute it. **Never** put full playbooks in `workflows/`.
3. **Prefer native** playbooks — execute with Grok Bot tools yourself. Shell out to `grok`/`claude`/`agy` **only** via the [BibleMate Studies CLI](skills/biblemate-studies-cli/SKILL.md) fallback, or when the user explicitly asks for the CLI.
4. **Artifacts** — write the **full, uncompromised report** under `/workspace/grok-bot-biblemate/` in the matching folder (`biblemate/`, `devotions/`, `sermons/`, `studies/`). Do not shorten the on-disk report.
5. **Chat delivery** — when finished, `SendToUser` a short digest **and** a copy of the report in chat (paste or attach the saved `.md`) plus the concrete path.
6. **Never invent** verse text, lexicon glosses, or commentary quotes — every Scripture citation needs a local DB fetch.
7. **Git sync** — report folders are meant to be committed/pushed; do not treat them as disposable cache. Use `/gbm-ecosystem-sync` (not generic `/sync`).

## Tool mapping

| Need | Tool |
|------|------|
| Search / references | `WebSearch`, `WebFetch` |
| Read playbooks / studies | `Read` |
| Scripts / file ops / verse retrieval | `Shell` (`python3` helpers beside playbooks) |
| Parallel study steps | `Task` with `subagent_type: executor` |
| User-visible result | `SendToUser` |

## Common slash commands

| Command | Purpose |
|---------|---------|
| `/bible John 3:16` | Exact verse retrieval (SQLite) |
| `/devotion Rom 8` | Pastoral devotion + prayer |
| `/promise-prayer` | First-person EN+粵語 promise prayer (self/family/church/world) |
| `/sermon Matt 5` | Sermon outline + content |
| `/biblemate …` | Orchestrated multi-step study |
| `/Gen faith` | Book-scoped search (66 books) |
| `/gbm-ecosystem-sync` | Commit + push **this** repo only |
| `biblemate-studies-cli` | Prefer native; optional `grok` CLI fallback |

## Layout

```
skills/          # Full playbooks (source of truth for methodology)
catalog/         # Thin loaders → installed to workflows/
scripts/         # install_to_box.sh, convert_to_grok_bot.py
docs/            # setup guide
biblemate/       # General study reports
devotions/       # Devotion outputs
sermons/         # Sermon outputs
studies/         # Multi-step / thematic studies
```

## Distinction from biblemate-agentic-workspace

| | **This repo (Grok Bot)** | **biblemate-agentic-workspace (Grok Build)** |
|--|--------------------------|----------------------------------------------|
| Runtime | Grok Bot computer | Grok Build TUI/CLI |
| Skills | `skills/` → `biblemate-native-skills/` | `.grok/skills/` |
| Tools | WebSearch, Task/executor, SendToUser | web_search, spawn_subagent, … |

Do not mix path conventions. If both repos exist on the box, BibleMate work for Bot agents uses **this** repo.
