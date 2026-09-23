#!/usr/bin/env bash
# Install grok-bot-biblemate onto this Grok Bot computer.
# Idempotent: safe to re-run after git pull.
# NON-destructive to trading-native-skills and unrelated workflows.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

PLAYBOOK_DEST="/home/box/agent-data/biblemate-native-skills"
CATALOG_DEST="/home/box/agent-data/workflows"
ARTIFACT_DIRS=(biblemate devotions sermons studies)

echo "==> grok-bot-biblemate install"
echo "    REPO_ROOT=$REPO_ROOT"

if [[ ! -d "$REPO_ROOT/skills" ]]; then
  echo "ERROR: skills/ missing under $REPO_ROOT" >&2
  exit 1
fi
if [[ ! -d "$REPO_ROOT/catalog" ]]; then
  echo "ERROR: catalog/ missing under $REPO_ROOT" >&2
  exit 1
fi

mkdir -p "$PLAYBOOK_DEST" "$CATALOG_DEST"

echo "==> Syncing full playbooks → $PLAYBOOK_DEST"
if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete \
    --exclude 'README.md' \
    "$REPO_ROOT/skills/" "$PLAYBOOK_DEST/"
else
  find "$PLAYBOOK_DEST" -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} +
  find "$PLAYBOOK_DEST" -mindepth 1 -maxdepth 1 -type f -name 'SKILL.md' -delete 2>/dev/null || true
  cp -a "$REPO_ROOT/skills/." "$PLAYBOOK_DEST/"
fi
if [[ -f "$REPO_ROOT/skills/README.md" ]]; then
  cp -a "$REPO_ROOT/skills/README.md" "$PLAYBOOK_DEST/README.md"
fi

echo "==> Installing catalog loaders → $CATALOG_DEST (non-destructive; trading left alone)"
installed=0
for skill_dir in "$REPO_ROOT/catalog"/*/; do
  [[ -d "$skill_dir" ]] || continue
  id="$(basename "$skill_dir")"
  mkdir -p "$CATALOG_DEST/$id"
  if [[ -f "$skill_dir/SKILL.md" ]]; then
    cp -a "$skill_dir/SKILL.md" "$CATALOG_DEST/$id/SKILL.md"
    installed=$((installed + 1))
  fi
done
echo "    catalog entries installed: $installed"

echo "==> Creating report output directories"
for d in "${ARTIFACT_DIRS[@]}"; do
  mkdir -p "$REPO_ROOT/artifacts/$d"
  mkdir -p "$REPO_ROOT/$d"
  if [[ ! -f "$REPO_ROOT/$d/README.md" ]]; then
    cat > "$REPO_ROOT/$d/README.md" << RD
# $d

Full BibleMate skill reports for this folder are saved here as markdown
(often \`YYYY-MM-DD-HH-MM-SS_<short-name>.md\` or a study subfolder).

Dual delivery: agents write the complete report on disk **and** send a chat
copy (or attach the \`.md\`) in Grok Bot. These files are intended to be
committed and synced to the remote.
RD
  fi
  touch "$REPO_ROOT/artifacts/$d/.gitkeep"
done

skill_count="$(find "$PLAYBOOK_DEST" -mindepth 2 -maxdepth 2 -name SKILL.md 2>/dev/null | wc -l | tr -d ' ')"
trading_count="$(find /home/box/agent-data/trading-native-skills -mindepth 2 -maxdepth 2 -name SKILL.md 2>/dev/null | wc -l | tr -d ' ')"
echo ""
echo "==> Install complete"
echo "    Full BibleMate playbooks with SKILL.md: $skill_count under $PLAYBOOK_DEST"
echo "    Catalog loaders updated under $CATALOG_DEST (non-biblemate / trading workflows left alone)"
echo "    Trading playbooks still present: $trading_count under trading-native-skills/"
echo "    Report folders ready under $REPO_ROOT (biblemate/, devotions/, sermons/, studies/)"

echo "==> Verifying BibleMate ecosystem CLI + sync skills"
ok=1
for id in biblemate-studies-cli gbm-ecosystem-sync; do
  if [[ -f "$PLAYBOOK_DEST/$id/SKILL.md" && -f "$CATALOG_DEST/$id/SKILL.md" ]]; then
    echo "    OK: $id playbook + catalog installed"
  else
    echo "ERROR: $id missing after install" >&2
    ok=0
  fi
done
if [[ "$ok" != "1" ]]; then
  exit 1
fi

# Spot-check core skills
for id in bible devotion sermon Gen; do
  if [[ -f "$PLAYBOOK_DEST/$id/SKILL.md" && -f "$CATALOG_DEST/$id/SKILL.md" ]]; then
    echo "    OK: $id playbook + catalog"
  else
    echo "ERROR: $id missing" >&2
    exit 1
  fi
done

if [[ -d /workspace/biblemate/data/bibles ]]; then
  echo "    OK: Bible data at /workspace/biblemate/data/bibles"
else
  echo "    NOTE: /workspace/biblemate/data/bibles not found — verse retrieval needs SQLite bibles"
fi
if [[ -d /workspace/biblemate-agentic-workspace/.grok ]]; then
  echo "    OK: Grok Build BibleMate pack found (CLI fallback ready)"
else
  echo "    NOTE: biblemate-agentic-workspace/.grok not found — native skills still work"
fi

echo ""
echo "Dual-delivery contract (encoded in AGENTS.md + catalog loaders):"
echo "  - Full uncompromised report → matching folder under this repo"
echo "  - Chat: digest + copy/attach of the report via SendToUser"
echo ""
echo "Next steps:"
echo "  1. Tell your Grok Bot agent:"
echo "     \"I installed the grok-bot-biblemate ecosystem; please verify BibleMate skills"
echo "      are available and prefer native skills over CLI.\""
echo "  2. Start a fresh conversation so slash commands like /bible, /devotion, /sermon appear."
echo "  3. Optional smoke test: /bible John 3:16 — confirm verse from SQLite + chat copy."
echo "  4. See docs/setup.md and scripts/register_skills.md."
