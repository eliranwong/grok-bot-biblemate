#!/usr/bin/env python3
"""Convert BibleMate Grok Build .grok skills into Grok Bot native SKILL.md packages.

Writes full playbooks into this repo's skills/ and thin catalog/ loaders.
After convert, run scripts/install_to_box.sh to install onto the Grok Bot computer.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

# Upstream BibleMate Grok Build pack
ROOT = Path("/workspace/biblemate-agentic-workspace")
SRC = ROOT / ".grok" / "skills"
CMD_SRC = ROOT / ".grok" / "commands"

# This repo
REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "skills"
STAGING = REPO / "scripts" / "out"
CATALOG_OUT = REPO / "catalog"
STAGING.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
CATALOG_OUT.mkdir(parents=True, exist_ok=True)

ARTIFACT_ROOT = "/workspace/grok-bot-biblemate"
PLAYBOOK_ROOT = "/home/box/agent-data/biblemate-native-skills"
WORKFLOWS_ROOT = "/home/box/agent-data/workflows"

# Canonical book slug → display name (frontmatter name often is the abbreviation)
BOOK_NAMES = {
    "Gen": "Genesis", "Exod": "Exodus", "Lev": "Leviticus", "Num": "Numbers",
    "Deut": "Deuteronomy", "Josh": "Joshua", "Judg": "Judges", "Ruth": "Ruth",
    "1Sam": "1 Samuel", "2Sam": "2 Samuel", "1Kgs": "1 Kings", "2Kgs": "2 Kings",
    "1Chr": "1 Chronicles", "2Chr": "2 Chronicles", "Ezra": "Ezra", "Neh": "Nehemiah",
    "Esth": "Esther", "Job": "Job", "Ps": "Psalms", "Prov": "Proverbs",
    "Eccl": "Ecclesiastes", "Song": "Song of Songs", "Isa": "Isaiah", "Jer": "Jeremiah",
    "Lam": "Lamentations", "Ezek": "Ezekiel", "Dan": "Daniel", "Hos": "Hosea",
    "Joel": "Joel", "Amos": "Amos", "Obad": "Obadiah", "Jonah": "Jonah",
    "Mic": "Micah", "Nah": "Nahum", "Hab": "Habakkuk", "Zeph": "Zephaniah",
    "Hag": "Haggai", "Zech": "Zechariah", "Mal": "Malachi", "Matt": "Matthew",
    "Mark": "Mark", "Luke": "Luke", "John": "John", "Acts": "Acts", "Rom": "Romans",
    "1Cor": "1 Corinthians", "2Cor": "2 Corinthians", "Gal": "Galatians",
    "Eph": "Ephesians", "Phil": "Philippians", "Col": "Colossians",
    "1Thess": "1 Thessalonians", "2Thess": "2 Thessalonians", "1Tim": "1 Timothy",
    "2Tim": "2 Timothy", "Titus": "Titus", "Phlm": "Philemon", "Heb": "Hebrews",
    "Jas": "James", "1Pet": "1 Peter", "2Pet": "2 Peter", "1John": "1 John",
    "2John": "2 John", "3John": "3 John", "Jude": "Jude", "Rev": "Revelation",
}

SPECIAL_NAMES = {
    "biblemate": "BibleMate",
    "biblemate-super": "BibleMate Super",
    "nt-context": "NT Context",
    "nt-highlights": "NT Highlights",
    "nt-meaning": "NT Meaning",
    "nt-themes": "NT Themes",
    "ot-context": "OT Context",
    "ot-highlights": "OT Highlights",
    "ot-highligths": "OT Highlights (legacy slug)",
    "ot-meaning": "OT Meaning",
    "ot-themes": "OT Themes",
    "book-analysis": "Book Analysis",
    "chapter-summary": "Chapter Summary",
    "daily-read": "Daily Read",
    "short-prayer": "Short Prayer",
    "translate-greek": "Translate Greek",
    "translate-hebrew": "Translate Hebrew",
    "xrefs": "Xrefs",
    "md": "MD",
    "docx": "DOCX",
    "zip": "ZIP",
}

NATIVE_PREAMBLE = f"""
## Grok Bot runtime notes (native port)

This skill was ported from the BibleMate Grok Build `.grok` playbook for **native Grok Bot** execution.

### Tool mapping
| Playbook concept | Use on Grok Bot |
|------------------|-----------------|
| Web research | `WebSearch`, `WebFetch` |
| Read files | `Read` |
| Shell / scripts | `Shell` (`python3` on helpers beside this playbook under `{PLAYBOOK_ROOT}/`) |
| Parallel workers | `Task` with `subagent_type: executor` (or MessageSubagent to steer) |
| Save reports | Write the **full, uncompromised** report under `{ARTIFACT_ROOT}/` in the folders the playbook names (`biblemate/`, `devotions/`, `sermons/`, `studies/`, …) |
| User-visible result | Always `SendToUser` a short digest **and** a chat copy of the report (paste full text or attach the saved `.md`) + concrete path when finished |

### Rules
- Do **not** shell out to `grok`/`claude`/`agy` for this skill — execute the methodology yourself with the tools above.
- **Never invent Scripture text.** Fetch verses via the `bible` skill / `bible_retriever.py` (local SQLite under `/workspace/biblemate/data/bibles` and `/workspace/biblemate/data_custom/bibles`; also mirrored at `/home/box/biblemate/...`).
- Default translations when unspecified: **CSB** (English), **CUV** (Chinese). Prefer Cantonese (粵語) for devotionals/check-ins when the user's language preference suggests it.
- Adopt a warm pastoral tone (Compassionate Pastor / related personas from BibleMate agents.md) unless the skill names a different persona.
- Prefer parallel tool calls where the playbook says to run work together.
- Working directory for artifacts: `{ARTIFACT_ROOT}` (report folders sync to git — do not treat as disposable cache).
- On every finished run: full report on disk **and** chat copy via `SendToUser` (attach `.md` for long reports).
- When the playbook mentions sibling skills, read the full playbook under `{PLAYBOOK_ROOT}/<id>/SKILL.md` (catalog loaders under `{WORKFLOWS_ROOT}/` point there after install).
- Helper scripts live beside the playbook after install, e.g. `python3 {PLAYBOOK_ROOT}/bible/bible_retriever.py "<query>"`.

---
"""


def extract_frontmatter(content: str) -> tuple[dict[str, str], str]:
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content
    meta: dict[str, str] = {}
    key = None
    buf: list[str] = []
    for line in match.group(1).split("\n"):
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            if key:
                meta[key] = "\n".join(buf).strip().strip('"').strip("'")
            key = m.group(1)
            buf = [m.group(2)]
        elif key:
            buf.append(line)
    if key:
        meta[key] = "\n".join(buf).strip().strip('"').strip("'")
    return meta, match.group(2)


def human_name(slug: str) -> str:
    if slug in BOOK_NAMES:
        return BOOK_NAMES[slug]
    if slug in SPECIAL_NAMES:
        return SPECIAL_NAMES[slug]
    parts = []
    for p in slug.split("-"):
        if p.upper() in {"NT", "OT", "AI", "CLI", "GBM", "CUV", "CSB", "NET", "KJV"}:
            parts.append(p.upper())
        else:
            parts.append(p.capitalize())
    return " ".join(parts)


def yaml_quote(s: str) -> str:
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


def fold_command_guidance(slug: str) -> str:
    cmd_path = CMD_SRC / f"{slug}.md"
    if not cmd_path.exists():
        return ""
    raw = cmd_path.read_text(encoding="utf-8")
    _, body = extract_frontmatter(raw)
    body = body.strip()
    if not body:
        return ""
    # Map $ARGUMENTS and persona refs
    body = body.replace("$ARGUMENTS", "user arguments after the slash command")
    # Avoid double-rewriting already-absolute agents.md paths
    body = re.sub(
        r"(?<!biblemate-agentic-workspace/)\.grok/agents\.md",
        "/workspace/biblemate-agentic-workspace/.grok/agents.md",
        body,
    )
    body = rewrite_body(body)
    # Clean any accidental doubled path from prior runs / replace chains
    body = body.replace(
        "/workspace/biblemate-agentic-workspace//workspace/biblemate-agentic-workspace/.grok/agents.md",
        "/workspace/biblemate-agentic-workspace/.grok/agents.md",
    )
    body = body.replace(
        "/workspace/biblemate-agentic-workspace/workspace/biblemate-agentic-workspace/.grok/agents.md",
        "/workspace/biblemate-agentic-workspace/.grok/agents.md",
    )
    return (
        "\n## Slash command guidance\n\n"
        f"Folded from the Grok Build command `/{slug}` — treat “user arguments after the slash command” "
        "as the input the user provided after the slash.\n\n"
        f"{body}\n"
    )


def rewrite_script_invocations(body: str, slug: str) -> str:
    """Rewrite python3 .grok/skills/<id>/<script> to installed absolute paths."""
    def repl(m: re.Match) -> str:
        skill_id = m.group(1)
        script = m.group(2)
        return f"python3 {PLAYBOOK_ROOT}/{skill_id}/{script}"

    body = re.sub(
        r"python3\s+\.grok/skills/([A-Za-z0-9_-]+)/([A-Za-z0-9_.-]+\.py)",
        repl,
        body,
    )
    # Relative path mentions without python3
    body = re.sub(
        r"(?<![\w/])\.grok/skills/([A-Za-z0-9_-]+)/([A-Za-z0-9_.-]+\.py)",
        lambda m: f"{PLAYBOOK_ROOT}/{m.group(1)}/{m.group(2)}",
        body,
    )
    return body


def rewrite_body(body: str) -> str:
    body = re.sub(r"##\s*INSTRUCTIONS FOR GROK(\s+BOT)?\b", "## INSTRUCTIONS FOR GROK BOT", body)
    body = re.sub(r"INSTRUCTIONS FOR GROK(\s+BOT)?\b", "INSTRUCTIONS FOR GROK BOT", body)

    reps = [
        ("`web_search`", "`WebSearch`"),
        ("web_search", "WebSearch"),
        ("`web_fetch` / `open_page`", "`WebFetch`"),
        ("`web_fetch`", "`WebFetch`"),
        ("web_fetch / open_page", "WebFetch"),
        ("web_fetch", "WebFetch"),
        ("`open_page`", "`WebFetch`"),
        ("open_page", "WebFetch"),
        ("`read_file`", "`Read`"),
        ("read_file", "Read"),
        ("`run_terminal_command`", "`Shell`"),
        ("run_terminal_command", "Shell"),
        ("`run_terminal_cmd`", "`Shell`"),
        ("run_terminal_cmd", "Shell"),
        ("`spawn_subagent`", "`Task` (executor)"),
        ("spawn_subagent", "Task/executor"),
        ("`search_replace`", "file edits"),
        ("search_replace", "file edits"),
        ("`Write` tool", "file write"),
        ("Write tool", "file write"),
        ("`write` tool", "file write"),
        (" write tool", " file write"),
        ("Grok Build BibleMate Skill:", "Grok Bot BibleMate Skill:"),
        ("Grok Build BibleMate Skill", "Grok Bot BibleMate Skill"),
        ("running inside Grok Build", "running as Grok Bot (BibleMate)"),
        ("inside Grok Build", "as Grok Bot"),
        ("Grok Build", "Grok Bot"),
        ("Claude CLI BibleMate Skill:", "Grok Bot BibleMate Skill:"),
        ("Claude CLI", "Grok Bot"),
        ("~/biblemate/data/bibles", "/workspace/biblemate/data/bibles"),
        ("~/biblemate/data_custom/bibles", "/workspace/biblemate/data_custom/bibles"),
        ("~/biblemate/", "/workspace/biblemate/"),
        ("`~/biblemate`", "`/workspace/biblemate`"),
        ("/workspace/biblemate-agentic-workspace/biblemate/", f"{ARTIFACT_ROOT}/biblemate/"),
    ]
    for old, new in reps:
        body = body.replace(old, new)

    body = body.replace("WebFetch / WebFetch", "WebFetch")
    body = body.replace("`WebFetch` / `WebFetch`", "`WebFetch`")
    body = body.replace("GROK BOT BOT", "GROK BOT")
    body = body.replace("Grok Bot Bot", "Grok Bot")
    body = re.sub(r"INSTRUCTIONS FOR GROK BOT(\s+BOT)+", "INSTRUCTIONS FOR GROK BOT", body)

    body = rewrite_script_invocations(body, "")

    # Remaining .grok/skills/ and .grok/commands/ refs → absolute native paths
    body = body.replace("python3 .grok/build_grok.py", "python3 /workspace/biblemate-agentic-workspace/.grok/build_grok.py")
    body = body.replace(".grok/build_grok.py", "/workspace/biblemate-agentic-workspace/.grok/build_grok.py")
    body = body.replace(".grok/skills/", f"{PLAYBOOK_ROOT}/")
    body = body.replace(".grok/commands/", f"{WORKFLOWS_ROOT}/")
    body = body.replace(
        "/workspace/biblemate-agentic-workspace//workspace/biblemate-agentic-workspace/.grok/agents.md",
        "/workspace/biblemate-agentic-workspace/.grok/agents.md",
    )

    # Output-saving rule: biblemate/ under Bot repo
    body = re.sub(
        r"(?<![\w/])biblemate/subdirectory",
        f"{ARTIFACT_ROOT}/biblemate/ subdirectory",
        body,
    )
    return body


def patch_helper_script(text: str) -> str:
    """Ensure helpers resolve /workspace/biblemate and /home/box/biblemate."""
    # Replace the common expanduser + BIBLEMATE_DATA pattern with a multi-root resolver
    old_block = (
        "home = os.path.expanduser('~')\n"
        "    base = os.environ.get('BIBLEMATE_DATA') or os.path.join(home, 'biblemate')"
    )
    new_block = (
        "def _biblemate_base():\n"
        "        candidates = []\n"
        "        env = os.environ.get('BIBLEMATE_DATA')\n"
        "        if env:\n"
        "            candidates.append(env)\n"
        "        candidates.extend(['/workspace/biblemate', '/home/box/biblemate', os.path.join(os.path.expanduser('~'), 'biblemate')])\n"
        "        for c in candidates:\n"
        "            if c and os.path.isdir(c):\n"
        "                return c\n"
        "        return candidates[0] if candidates else '/workspace/biblemate'\n"
        "    base = _biblemate_base()"
    )
    if old_block in text:
        text = text.replace(old_block, new_block)

    # One-liner variants
    text = text.replace(
        "os.environ.get('BIBLEMATE_DATA') or os.path.join(os.path.expanduser('~'), 'biblemate')",
        "(os.environ.get('BIBLEMATE_DATA') or next((p for p in ['/workspace/biblemate','/home/box/biblemate',os.path.join(os.path.expanduser('~'),'biblemate')] if os.path.isdir(p)), '/workspace/biblemate'))",
    )
    text = text.replace("~/biblemate/data/bibles", "/workspace/biblemate/data/bibles")
    text = text.replace("~/biblemate/data_custom/bibles", "/workspace/biblemate/data_custom/bibles")
    text = text.replace("~/biblemate/data/lexicons", "/workspace/biblemate/data/lexicons")
    text = text.replace("~/biblemate/data_custom/lexicons", "/workspace/biblemate/data_custom/lexicons")
    text = text.replace("~/biblemate/data/commentaries", "/workspace/biblemate/data/commentaries")
    text = text.replace("~/biblemate/data_custom/commentaries", "/workspace/biblemate/data_custom/commentaries")
    text = text.replace("`~/biblemate/data/", "`/workspace/biblemate/data/")
    text = text.replace("`~/biblemate/data_custom/", "`/workspace/biblemate/data_custom/")
    return text


def copy_helpers(src_dir: Path, dest_dir: Path) -> int:
    """Copy all non-SKILL.md files/dirs from source skill folder; patch .py helpers."""
    count = 0
    for item in src_dir.iterdir():
        if item.name == "SKILL.md":
            continue
        dest = dest_dir / item.name
        if item.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)
            # Patch any .py under data/ or nested
            for py in dest.rglob("*.py"):
                py.write_text(patch_helper_script(py.read_text(encoding="utf-8")), encoding="utf-8")
                count += 1
            # Count data files too
            for f in dest.rglob("*"):
                if f.is_file() and f.suffix != ".py":
                    count += 1
        elif item.is_file():
            if item.suffix == ".py":
                dest.write_text(patch_helper_script(item.read_text(encoding="utf-8")), encoding="utf-8")
            else:
                shutil.copy2(item, dest)
            count += 1
    return count


def build_skill(slug: str, src_path: Path) -> tuple[str, str, str]:
    raw = src_path.read_text(encoding="utf-8")
    meta, body = extract_frontmatter(raw)
    # Prefer frontmatter name for books (Gen) but human_name for display title
    fm_name = meta.get("name") or slug
    if slug in BOOK_NAMES:
        name = BOOK_NAMES[slug]  # Genesis etc. for Title Case display
    elif slug in SPECIAL_NAMES:
        name = SPECIAL_NAMES[slug]
    else:
        # Use frontmatter if it's already human-ish, else Title Case from slug
        name = fm_name if fm_name != slug or "-" not in slug else human_name(slug)
        if name == slug and slug not in BOOK_NAMES:
            name = human_name(slug)

    desc = meta.get("description") or f"Use when running the {slug} BibleMate study playbook."
    desc = desc.replace('\\"', '"').replace("\\\\", "\\")
    if f"/{slug}" not in desc and f"runs /{slug}" not in desc.lower():
        desc = f"{desc.rstrip('. ')}. Use when the user runs /{slug}."

    body = NATIVE_PREAMBLE + rewrite_body(body.lstrip("\n"))
    body = body + fold_command_guidance(slug)

    content = (
        "---\n"
        f"name: {name}\n"
        f"description: {yaml_quote(desc)}\n"
        "ecosystem: biblemate\n"
        "port: grok-bot-native\n"
        f"source: .grok/skills/{slug}\n"
        "---\n"
        f"# {name}\n\n"
        f"{body.lstrip()}\n"
    )
    return name, desc, content


def build_catalog_loader(slug: str, name: str) -> str:
    desc = (
        f"Use when the user runs /{slug} or requests this BibleMate workflow "
        "(native Grok Bot port)."
    )
    body = f"""# {name}

Native Grok Bot port of the BibleMate playbook `{slug}`.

## Steps
1. Read the full playbook at `{PLAYBOOK_ROOT}/{slug}/SKILL.md` with `Read`.
2. Execute that methodology with Grok Bot tools (`Read`, `Shell`, `WebSearch`, `WebFetch`, `Task`/executor as needed).
3. Do **not** call `grok`, `claude`, or `agy` for this skill.
4. Write the full report under `{ARTIFACT_ROOT}/` in the folders the playbook specifies.
5. When finished, `SendToUser` a short digest **and** a chat copy of the report (paste or attach) plus concrete paths.
"""
    return (
        "---\n"
        f"name: {name}\n"
        f"description: >-\n"
        f"  {desc}\n"
        "---\n"
        f"{body}\n"
    )


def write_pkg(slug: str, content: str) -> Path:
    dest = OUT / slug
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / "SKILL.md"
    path.write_text(content, encoding="utf-8")
    (STAGING / f"{slug}.md").write_text(content, encoding="utf-8")
    return path


def write_catalog(slug: str, content: str) -> Path:
    dest = CATALOG_OUT / slug
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / "SKILL.md"
    path.write_text(content, encoding="utf-8")
    return path


def write_special_skills() -> list[dict]:
    """Add biblemate-studies-cli and gbm-ecosystem-sync (not from upstream .grok)."""
    extras = []

    cli_name = "BibleMate Studies CLI"
    cli_slug = "biblemate-studies-cli"
    cli_desc = (
        "Use when the user asks to run a Bible study, devotion, sermon prep, slash "
        "command, or any query against the BibleMate agentic workspace — prefer native "
        "Grok Bot skills, else grok/claude/agy CLIs as fallback. Use when the user runs "
        "/biblemate-studies-cli."
    )
    cli_body = f"""# {cli_name}

Prefer **native** Grok Bot BibleMate playbooks. Fall back to the agentic workspace CLIs (`grok` / `claude` / `agy`) when the user asks for the CLI path, a native skill is missing/broken, or you need the Grok Build `.grok` surface.

## Defaults

| Mode | Working directory | When |
|------|-------------------|------|
| **Native (preferred)** | Playbooks in `{PLAYBOOK_ROOT}/`; reports under `{ARTIFACT_ROOT}/` | Known slash commands (`/bible`, `/devotion`, `/sermon`, `/biblemate`, `/Gen`, …) |
| **CLI fallback** | `/workspace/biblemate-agentic-workspace` (must contain `.grok/`) or `/workspace/biblemate_studies` | User asks for CLI, native path unavailable, or Build-only workflow |

### CLI flags (pre-cleared for this ecosystem)

- Primary: `grok --always-approve -p "<query>"`
- If asked or grok fails: `claude -p "<query>"`
- Last resort: `agy --dangerously-skip-permissions -p "<query>"`
- Do **not** re-ask for per-step approval on routine studies/devotions/sermons.
- Only confirm first if the query is clearly destructive (wipe, reset, force-push, mass delete).

## Steps (native path)

1. Match the ask to a catalog / playbook id (e.g. `devotion`, `sermon`, `bible`, `Gen`).
2. Read `{PLAYBOOK_ROOT}/<id>/SKILL.md` and execute with Grok Bot tools (`WebSearch`, `WebFetch`, `Read`, `Shell`, `Task`/executor).
3. Never invent Scripture — fetch via `bible` / `bible_retriever.py`. Defaults when unspecified: **CSB** (English), **CUV** (Chinese).
4. Write the **full, uncompromised report** under `{ARTIFACT_ROOT}/` in the folder the playbook names (`biblemate/`, `devotions/`, `sermons/`, `studies/`).
5. `SendToUser` a short pastoral digest **and** a chat copy of the report (paste or attach the `.md`) plus the concrete path.

## Steps (CLI fallback)

1. Prefer `/workspace/biblemate-agentic-workspace/.grok` if present; else `/workspace/biblemate_studies`. If neither exists, tell the user — do not invent a CLI run against the Bot-only repo.
2. `cd` into the chosen Build/studies repo.
3. Translate the ask into a clear `-p` query (keep slash forms like `/bible`, `/sermon`, `/devotion`, `/biblemate`, `/Gen`).
4. Quote safely (HEREDOC or carefully escaped quotes).
5. Run with a long enough timeout; background if needed; notify when finished.
6. Inspect new/changed report files under `biblemate/` (or the repo's study output folders).
7. `SendToUser` a short pastoral digest **and** a chat copy (or attach the main `.md`) plus concrete paths.

## Notes

- Native skills and CLI fallback are complementary: native = Grok Bot tools + this Bot repo; CLI = Grok Build package in `biblemate-agentic-workspace` / `biblemate_studies`.
- One CLI per request unless the user asked to compare tools.
- Repo sync for **this** Bot pack: `/gbm-ecosystem-sync`. Build repo sync: that ecosystem's own `/sync`.
"""
    cli_content = (
        "---\n"
        f"name: {cli_name}\n"
        f"description: {yaml_quote(cli_desc)}\n"
        "ecosystem: biblemate\n"
        "port: grok-bot-native\n"
        "---\n"
        f"{cli_body}\n"
    )
    write_pkg(cli_slug, cli_content)
    write_catalog(cli_slug, build_catalog_loader(cli_slug, cli_name))
    extras.append({"id": cli_slug, "name": cli_name, "description": cli_desc, "kind": "skill"})

    sync_name = "GBM Ecosystem Sync"
    sync_slug = "gbm-ecosystem-sync"
    sync_desc = (
        "Commit and push the Grok Bot BibleMate ecosystem git repo to its remote. Use "
        "when the user runs /gbm-ecosystem-sync or /biblemate-ecosystem-sync or asks to "
        "sync, commit, or push grok-bot-biblemate (reports, skills, docs) — not a generic "
        "/sync for other repos. Use when the user runs /gbm-ecosystem-sync."
    )
    sync_body = f"""# {sync_name}

Stage, commit, and push **only** `{ARTIFACT_ROOT}` so the remote always has the latest skills, docs, and study reports. Counterpart to the Grok Build repo's `/sync`, with a scoped name so it does not collide with other systems.

> **Repo root (fixed):** `{ARTIFACT_ROOT}`
> Do **not** run this against `biblemate-agentic-workspace`, `biblemate_studies`, `grok-bot-trading-ecosystem`, or any other path.
> Slash names: **`/gbm-ecosystem-sync`** or **`/biblemate-ecosystem-sync`** (not `/sync`).

## Steps

### Phase 0: Safety

1. `cd {ARTIFACT_ROOT}` (confirm with `pwd` / `git rev-parse --show-toplevel`).
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

11. Check ahead of upstream, e.g. `git rev-list --count @{{upstream}}..HEAD` and/or `git log --oneline origin/main..HEAD`.
12. If there are unpushed commits, `git push`. If the remote rejected due to new commits, `git pull --rebase` then `git push` again (still no force-push).
13. If nothing to push, note that the branch is already up to date with the remote.

### Phase 3: Report

14. `SendToUser` the result: files changed (if any), commit hash (if any), push success/failure, and final `git status -sb`.
15. Sync is **not** complete until there are no unpushed commits on the tracking branch.

## CRITICAL

- **Never skip Phase 2.** Unpushed commits from earlier in the session still need a push.
- Scope is **only** `grok-bot-biblemate`. For the Grok Build BibleMate repo, use that ecosystem's own `/sync`.
- Slash name is **`/gbm-ecosystem-sync`** (alias `/biblemate-ecosystem-sync`) — not `/sync`.
"""
    sync_content = (
        "---\n"
        f"name: {sync_name}\n"
        f"description: {yaml_quote(sync_desc)}\n"
        "ecosystem: biblemate\n"
        "port: grok-bot-native\n"
        "---\n"
        f"{sync_body}\n"
    )
    write_pkg(sync_slug, sync_content)
    write_catalog(sync_slug, build_catalog_loader(sync_slug, sync_name))
    # Alias catalog for biblemate-ecosystem-sync → same playbook
    alias_slug = "biblemate-ecosystem-sync"
    alias_name = "BibleMate Ecosystem Sync"
    alias_loader = f"""---
name: {alias_name}
description: >-
  Use when the user runs /biblemate-ecosystem-sync or asks to sync grok-bot-biblemate
  (alias for /gbm-ecosystem-sync; native Grok Bot port).
---
# {alias_name}

Slash alias for **GBM Ecosystem Sync** (native Grok Bot port).

## Steps
1. Read and follow `{PLAYBOOK_ROOT}/{sync_slug}/SKILL.md`.
2. Pass through arguments after `/{alias_slug}`.
3. Execute with Grok Bot tools — do not call the `grok` CLI for the sync methodology itself (git via `Shell` is fine).
4. Scope is **only** `{ARTIFACT_ROOT}`.
5. `SendToUser` the sync result when finished.
"""
    # Thin alias playbook too
    alias_playbook = f"""---
name: {alias_name}
description: {yaml_quote("Slash alias for GBM Ecosystem Sync. Use when the user runs /biblemate-ecosystem-sync.")}
ecosystem: biblemate
port: grok-bot-native-alias
target: {sync_slug}
---
# {alias_name}

Native Grok Bot slash alias for **GBM Ecosystem Sync**.

## Steps
1. Open and follow `{PLAYBOOK_ROOT}/{sync_slug}/SKILL.md` exactly.
2. Pass through all arguments after `/{alias_slug}`.
3. Scope is **only** `{ARTIFACT_ROOT}` — never a generic `/sync`.
4. `SendToUser` the sync result when finished.
"""
    write_pkg(alias_slug, alias_playbook)
    write_catalog(alias_slug, alias_loader)
    extras.append({"id": sync_slug, "name": sync_name, "description": sync_desc, "kind": "skill"})
    extras.append({"id": alias_slug, "name": alias_name, "description": "alias", "kind": "alias", "target": sync_slug})
    return extras


def main() -> None:
    if not SRC.is_dir():
        raise SystemExit(
            f"Upstream .grok skills not found at {SRC}.\n"
            "Clone biblemate-agentic-workspace to /workspace/biblemate-agentic-workspace first."
        )

    manifest = []
    helpers_total = 0
    skills = sorted(p for p in SRC.iterdir() if p.is_dir() and (p / "SKILL.md").exists())
    for folder in skills:
        slug = folder.name
        name, desc, content = build_skill(slug, folder / "SKILL.md")
        path = write_pkg(slug, content)
        helpers_total += copy_helpers(folder, OUT / slug)
        write_catalog(slug, build_catalog_loader(slug, name))
        manifest.append({
            "id": slug,
            "name": name,
            "description": desc,
            "path": str(path),
            "kind": "skill",
            "bytes": len(content),
        })
        print(f"wrote skill {slug} ({len(content)} bytes)")

    for extra in write_special_skills():
        # Avoid duplicates if upstream somehow had them
        if any(m["id"] == extra["id"] for m in manifest):
            print(f"skip duplicate special {extra['id']}")
            continue
        manifest.append({
            "id": extra["id"],
            "name": extra["name"],
            "description": extra.get("description", ""),
            "path": str(OUT / extra["id"] / "SKILL.md"),
            "kind": extra["kind"],
            "bytes": (OUT / extra["id"] / "SKILL.md").stat().st_size,
            **({k: v for k, v in extra.items() if k == "target"}),
        })
        print(f"wrote special {extra['id']}")

    man_path = STAGING / "manifest.json"
    man_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    index_lines = ["# Grok Bot native BibleMate skills (ported)", "", f"Count: {len(manifest)}", ""]
    for m in manifest:
        index_lines.append(f"- `{m['id']}` — {m['name']} ({m['kind']})")
    (STAGING / "INDEX.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    # Also write to skill-port
    skill_port = Path("/workspace/grok-bot-skill-port")
    skill_port.mkdir(parents=True, exist_ok=True)
    (skill_port / "biblemate_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (skill_port / "biblemate_INDEX.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    readme = ["# Native Grok Bot BibleMate playbooks", "", f"Total: {len(manifest)}", ""]
    for m in sorted(manifest, key=lambda x: (0 if x["kind"] == "skill" else 1, x["id"].lower())):
        readme.append(f"- [{m['name']}]({m['id']}/SKILL.md) — `{m['id']}` ({m['kind']})")
    (OUT / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    print(f"DONE count={len(manifest)} helpers_copied≈{helpers_total} OUT={OUT} CATALOG={CATALOG_OUT}")


if __name__ == "__main__":
    main()
