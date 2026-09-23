---
name: GBM Ecosystem Sync
description: "Commit and push the Grok Bot BibleMate ecosystem git repo to its remote. Use when the user runs /gbm-ecosystem-sync or /biblemate-ecosystem-sync or asks to sync, commit, or push grok-bot-biblemate (reports, skills, docs) — not a generic /sync for other repos. Use when the user runs /gbm-ecosystem-sync."
ecosystem: biblemate
port: grok-bot-native
---
# GBM Ecosystem Sync

Stage, commit, and push **only** `/workspace/grok-bot-biblemate` so the remote always has the latest skills, docs, and study reports. Counterpart to the Grok Build repo's `/sync`, with a scoped name so it does not collide with other systems.

> **Repo root (fixed):** `/workspace/grok-bot-biblemate`
> Do **not** run this against `biblemate-agentic-workspace`, `biblemate_studies`, `grok-bot-trading-ecosystem`, or any other path.
> Slash names: **`/gbm-ecosystem-sync`** or **`/biblemate-ecosystem-sync`** (not `/sync`).

## Steps

### Phase 0: Safety

1. `cd /workspace/grok-bot-biblemate` (confirm with `pwd` / `git rev-parse --show-toplevel`).
2. If the cwd is not this repo, **stop** and tell the user.
3. Do **not** change `git config`. Do **not** force-push. Do **not** amend unless the user explicitly asks and the amend rules allow it.
4. Never commit secrets (`.env`, credentials, tokens). If such files appear in `git status`, warn and exclude them.

### Phase 1: Commit any uncommitted changes

5. Run `git status --short`.
6. If there are no uncommitted changes, skip to Phase 2.
7. Run `git add -A` to stage all changes (new, modified, deleted) under this repo.
8. Review `git diff --cached --stat` and draft a concise commit message:
   - Skills / catalog / scripts / docs changes → say what changed
   - New or updated reports under `biblemate/`, `devotions/`, `sermons/`, `studies/` → mention count and type
   - Keep the first line under ~100 characters; optional short body after a blank line
   - No `Co-Authored-By` trailer
9. Commit with a HEREDOC (do not use interactive git flags):

```bash
git commit -m "$(cat <<'EOF'
<message here>

EOF
)"
```

10. If the commit fails (hooks), fix and create a **new** commit — do not amend unless the user asked.

### Phase 2: Push any unpushed commits

11. Check ahead of upstream, e.g. `git rev-list --count @{upstream}..HEAD` and/or `git log --oneline origin/main..HEAD`.
12. If there are unpushed commits, `git push`. If the remote rejected due to new commits, `git pull --rebase` then `git push` again (still no force-push).
13. If nothing to push, note that the branch is already up to date with the remote.

### Phase 3: Report

14. `SendToUser` the result: files changed (if any), commit hash (if any), push success/failure, and final `git status -sb`.
15. Sync is **not** complete until there are no unpushed commits on the tracking branch.

## CRITICAL

- **Never skip Phase 2.** Unpushed commits from earlier in the session still need a push.
- Scope is **only** `grok-bot-biblemate`. For the Grok Build BibleMate repo, use that ecosystem's own `/sync`.
- Slash name is **`/gbm-ecosystem-sync`** (alias `/biblemate-ecosystem-sync`) — not `/sync`.

