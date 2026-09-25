# BibleMate orchestrators (`/biblemate`, `/biblemate-super`)

These two enrolled skills are the **front door** for deep BibleMate study under Grok Bot’s enrollment cap. They do **not** replace leaf skills by collapsing a study into one recipe. Each run **composes many** playbooks from the unenrolled library.

## Why only two enrolled?

Market / trading skills already occupy most of the ~100 enrollment slots. Leaf BibleMate playbooks (~130) stay on disk and are opened **by path** when an orchestrator plans them.

| Enrolled (`workflows/`) | Unenrolled library |
|-------------------------|--------------------|
| `/biblemate`, `/biblemate-super` (+ staples like `/promise-prayer`, `/gbm-ecosystem-sync`) | `/home/box/agent-data/biblemate-native-skills/<id>/SKILL.md` |

## Hard rule

**Multi-skill only.** A valid study always includes multiple leaves (at least retrieval + analysis + theology + application for standard runs). Routing to a single leaf is a failure mode.

## Paths

```text
PLAYBOOK_ROOT = /home/box/agent-data/biblemate-native-skills
ARTIFACT_ROOT = /workspace/grok-bot-biblemate
STUDIES_DIR   = /workspace/grok-bot-biblemate/biblemate
PERSONAS      = /workspace/biblemate-agentic-workspace/.grok/agents.md
```

Repo mirrors: `skills/biblemate/`, `skills/biblemate-super/` (full playbooks + Python helpers).

## `/biblemate` — fixed multi-phase pipeline

Use for standard **passage / book / topical / sermon_devotion** studies.

1. Classify study type.
2. Plan **many** leaf ids per phase (see playbook routing tables).
3. For each leaf: `Read PLAYBOOK_ROOT/<id>/SKILL.md` → execute → save step.
4. Pre-final overview → iterative final manuscript → optional sync.

### Phase → leaves (summary)

| Phase | Multiple leaves (examples) |
|-------|----------------------------|
| 1 Data | `bible` + (`original`\|`interlinear`) + `morphology`, `xrefs`, `commentary`, … |
| 2 Analysis | `keywords`, `outline`, `flow`, context/highlights, … |
| 3 Theology | `themes`, `theology`, `meaning`, `insights`, `canon`, … |
| 4 Application | `application` + (`sermon`\|`devotion`) + `prayer`, … |
| 5–7 | Overview, final response, `sync` / GBM |

Helpers: `skills/biblemate/biblemate_orchestrator.py`  
`--list-skills` discovers `PLAYBOOK_ROOT` (not `.grok/skills`).

## `/biblemate-super` — dynamic multi-phase + audits

Use for custom phase design, deep/contested research, multi-book synthesis, or audit-until-solid.

1. Assess request; invent N phases with clear goals.
2. Assign **multiple** steps (skill + persona) per phase.
3. Execute each leaf playbook; **audit**; append more leaves if goals unmet.
4. Overview → iterative final response → sync.

Study folders are prefixed `super_`.

Helpers: `skills/biblemate-super/biblemate_super_orchestrator.py`

## Intent → which orchestrator

| Ask | Skill |
|-----|--------|
| Ordinary passage/book/topical/sermon study | `/biblemate` |
| “Super”, custom phases, deep audit, course-length | `/biblemate-super` |
| Ambiguous “study X” | `/biblemate` |
| Bilingual promise + daily news prayer | `/promise-prayer` (separate) |
| Push this Bot pack | `/gbm-ecosystem-sync` |

## Enrollment

```text
update_state → skill write (omit id on create; id becomes biblemate / biblemate-super)
```

Do **not** Shell-overwrite `~/agent-data/workflows/*/SKILL.md` (catalog glitch risk). Edit playbooks under `biblemate-native-skills/` or this repo, then re-save enrolled wrappers via `update_state`.

Thin enrolled wrappers point at the full native playbooks.

## Leaf library notes

- ~131 folders under `PLAYBOOK_ROOT` (book abbrevs + analytical/pastoral utilities).
- Prefer `Luke` over legacy `gospel-of-luke` / `third-gospel`.
- Prefer `ot-highlights` over typo folder `ot-highligths`.
- Leaves are **not** required in `workflows/` for orchestration to work.

## Related docs

- [Promise Prayer](promise-prayer.md)
- Repo `skills/README.md` index
- `AGENTS.md` / setup guides in this repo
