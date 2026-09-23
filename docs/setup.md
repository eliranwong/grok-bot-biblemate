# Setup: Fresh Grok Bot Computer (BibleMate)

Primary install guide for **grok-bot-biblemate** — native BibleMate skills for Grok Bot (not Grok Build).

## Prerequisites

- A Grok Bot computer (box) with access to `/workspace` and `/home/box/agent-data/`
- Bible SQLite data at `/workspace/biblemate/data/bibles` (and optionally `data_custom/`)
- `git` and `bash` (Python 3 needed to re-convert from upstream `.grok`)

## 1. Clone this repo

```bash
cd /workspace
git clone <YOUR_FORK_OR_REMOTE_URL> grok-bot-biblemate
cd grok-bot-biblemate
```

Target path should be exactly:

```text
/workspace/grok-bot-biblemate
```

## 2. Run the install script

```bash
bash scripts/install_to_box.sh
```

What it does (idempotent — safe to re-run):

1. Syncs `skills/` → `/home/box/agent-data/biblemate-native-skills/` (full playbooks; replace within that tree only)
2. Copies each `catalog/<id>/SKILL.md` → `/home/box/agent-data/workflows/<id>/SKILL.md` **without** deleting unrelated workflows (trading, etc.)
3. Creates report folders: `biblemate/`, `devotions/`, `sermons/`, `studies/`

## 3. Tell your Grok Bot agent

> I installed the grok-bot-biblemate ecosystem; please verify BibleMate skills are available and prefer native skills over CLI.

See [scripts/register_skills.md](../scripts/register_skills.md) for the agent checklist.

## 4. Defaults

- Translations when unspecified: **CSB** (English), **CUV** (Chinese)
- Tone: warm pastoral (Compassionate Pastor)
- Never invent Scripture — always use `/bible` / `bible_retriever.py`
- Dual delivery: full report on disk + `SendToUser` digest/copy

## 5. Optional CLI fallback

If native path is insufficient, `biblemate-studies-cli` can run `grok --always-approve -p "…"` against `/workspace/biblemate-agentic-workspace` or `/workspace/biblemate_studies`.
