# Register / refresh BibleMate skills on Grok Bot

After `bash scripts/install_to_box.sh`, catalog loaders live under `/home/box/agent-data/workflows/<id>/SKILL.md` and full playbooks under `/home/box/agent-data/biblemate-native-skills/<id>/SKILL.md`.

**File copy alone does NOT put skills in `/` autocomplete.** The agent must also call `update_state` (target `skill`, action `write`) for each catalog id so the shared skill catalog registers them. A successful `update_state` often refreshes `/` autocomplete **in the same conversation** (Market pattern). The app has no New Chat control; only ask for a refresh if the picker stays stale.

## What the agent should do

When the user says they installed **grok-bot-biblemate**, or slash autocomplete is missing:

1. Confirm playbooks exist (`ls /home/box/agent-data/biblemate-native-skills | head`).
2. Confirm thin loaders exist under `/home/box/agent-data/workflows/` for `bible`, `devotion`, `sermon`, `Gen`, `gbm-ecosystem-sync`, `biblemate-studies-cli`, etc.
3. **Register** each BibleMate catalog skill with `update_state` (target `skill`, action `write`): pass `id` (folder slug), `name`, `description` (must say when to use / slash), and a thin `body` that `Read`s the playbook under `biblemate-native-skills` and runs it with Bot tools only (no `grok`/`claude`/`agy`). Updating an existing id refreshes it; omit `id` only when creating a brand-new skill.
4. Prefer **native** skill execution over the BibleMate Studies CLI unless the user asks for CLI.
5. Confirm report folders under `/workspace/grok-bot-biblemate/` (`biblemate/`, `devotions/`, `sermons/`, `studies/`).
6. Confirm trading skills were **not** wiped.
7. Dual-delivery: full report on disk + `SendToUser` digest + chat copy + paths.
8. After `update_state`, check `/` autocomplete in the same chat; only ask for a refresh if the picker stays stale.
9. Smoke test only if asked: `/bible John 3:16` — never invent verses.

## Scoped sync

Use `/gbm-ecosystem-sync` (alias `/biblemate-ecosystem-sync`) for the Bot repo. Do **not** rely on a bare `/sync` for this pack.

## Do not

- Delete unrelated workflows (trading skills, etc.).
- Dump full playbooks into `workflows/` — only thin loaders belong there.
- Rewrite playbooks only under `/home/box/agent-data/` — edit this repo’s `skills/` / `catalog/`, then re-run install, then re-`update_state`.
- Invent Scripture during verification.
- Use generic `/sync` for this repo — use `/gbm-ecosystem-sync`.

## Promise Prayer (special)

- Playbook: `skills/promise-prayer/`; docs: `docs/promise-prayer.md`
- Enroll with `update_state` id `promise-prayer` (slash `/promise-prayer`)
- **Never** Shell-write `/home/box/agent-data/workflows/*/SKILL.md` — that can regenerate the brain-docs “without a size” catalog glitch. Edit the repo, then `update_state`.
- Verse log: `/workspace/biblemate_studies/prayers/promise-verse-log.txt` (30-day uniqueness)
- Scheduled routine (separate from skills): folder `promise-prayers-every-2h`, cron `0 9,11,13,15,17,19,21,23 * * *` Europe/London
- Autocomplete often refreshes **in the same conversation** after a successful `update_state` (no new-chat control in the app UI)
