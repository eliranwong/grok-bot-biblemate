# Grok Bot BibleMate Ecosystem

Native Bible study skills and playbooks for **Grok Bot** computers — verse retrieval, devotionals, sermons, book studies, and orchestration slash commands your agents run with WebSearch / WebFetch / Read / Shell / Task (executor).

| Surface | Skills / commands | Project rules |
|---------|-------------------|---------------|
| **Grok Bot** | `skills/` + `catalog/` → installed to `biblemate-native-skills/` + `workflows/` | [`AGENTS.md`](AGENTS.md) |

> Pastoral / educational Bible study tools. Never invent Scripture text — always fetch from local SQLite via the `bible` skill.

## What this is

- **Native Grok Bot skills** — full methodology in `skills/<id>/SKILL.md`, thin catalog loaders in `catalog/<id>/SKILL.md`
- **Not** the Grok Build package (`.grok/`). That lives in **biblemate-agentic-workspace** (and optionally `biblemate_studies`)
- Install once onto a Grok Bot box; agents invoke `/bible`, `/devotion`, `/sermon`, `/biblemate`, `/Gen`, etc. without calling external CLIs

## Components

| Path | Role |
|------|------|
| `skills/` | Full playbook packages (source of truth). Install → `/home/box/agent-data/biblemate-native-skills/` |
| `catalog/` | Thin slash-command loaders. Install → `/home/box/agent-data/workflows/` (non-destructive; trading left alone) |
| `scripts/` | `install_to_box.sh`, `convert_to_grok_bot.py`, `register_skills.md` |
| `docs/` | Setup guide |
| Report folders | `biblemate/`, `devotions/`, `sermons/`, `studies/` — **full reports saved here and syncable to GitHub** |

## Quick start

Follow **[`docs/setup.md`](docs/setup.md)**.

```bash
cd /workspace
git clone <REMOTE> grok-bot-biblemate
cd grok-bot-biblemate
bash scripts/install_to_box.sh
```

Then tell your agent:

> I installed the grok-bot-biblemate ecosystem; please verify BibleMate skills are available and prefer native skills over CLI.

## Report storage

Every skill run writes a **full report** under `/workspace/grok-bot-biblemate/`:

| Folder | Typical slash commands |
|--------|------------------------|
| `biblemate/` | General studies, orchestration (`/biblemate`, `/biblemate-super`, most analysis skills) |
| `devotions/` | `/devotion`, `/daily-read`, `/prayer`, `/short-prayer` |
| `sermons/` | `/sermon`, `/outline`, `/flow` |
| `studies/` | Multi-step studies, book deep-dives, thematic work |

In Grok Bot chat, the agent also sends a **copy** of the report (inline or attached `.md`).

## Common slash commands

**Core**

- `/bible [VERSION…] REF` — retrieve exact verses from local SQLite (never invent text)
- `/devotion [passage]` — pastoral devotion + prayer
- `/sermon [passage]` — homiletical outline and content
- `/biblemate [request]` — multi-step orchestrated study
- `/biblemate-super [request]` — enhanced orchestration
- `/Gen`, `/John`, `/Rom`, … — book-scoped search (66 books)

**Defaults when translation unspecified:** **CSB** (English), **CUV** (Chinese). Prefer 粵語 for devotionals/check-ins when language preference suggests it.

**CLI fallback (optional)**

- `biblemate-studies-cli` — prefer native skills; fall back to `grok --always-approve` in `/workspace/biblemate-agentic-workspace` or `/workspace/biblemate_studies`.

**Repo sync**

- `/gbm-ecosystem-sync` (alias `/biblemate-ecosystem-sync`) — commit + push **this** repo only. Not a generic `/sync`.

## Tool mapping (Grok Bot)

| Playbook concept | Use on Grok Bot |
|------------------|-----------------|
| Web research | `WebSearch`, `WebFetch` |
| Files | `Read`, `Shell` |
| Parallel | `Task` / executor |
| Scripts | `Shell` `python3` on helpers under `/home/box/agent-data/biblemate-native-skills/<id>/` |
| Artifacts | `/workspace/grok-bot-biblemate/` (`biblemate/`, `devotions/`, `sermons/`, `studies/`) |
| Delivery | `SendToUser` digest + chat copy/attach + paths |

## Distinction from biblemate-agentic-workspace

| | **This repo (Grok Bot)** | **biblemate-agentic-workspace (Grok Build)** |
|--|--------------------------|----------------------------------------------|
| Runtime | Grok Bot computer | Grok Build TUI/CLI |
| Skills | `skills/` → `biblemate-native-skills/` | `.grok/skills/` |
| Tools | WebSearch, Task/executor, SendToUser | web_search, spawn_subagent, … |

Do not mix path conventions. Full playbooks never go into `workflows/` — only thin loaders.

## Bible data

Verse retrieval uses SQLite under:

- `/workspace/biblemate/data/bibles` and `/workspace/biblemate/data_custom/bibles`
- Mirrored at `/home/box/biblemate/...` (`~/biblemate` typically symlinks here)

## Re-convert from upstream

If `.grok` skills change:

```bash
python3 scripts/convert_to_grok_bot.py
bash scripts/install_to_box.sh
```
