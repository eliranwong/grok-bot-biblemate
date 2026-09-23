---
name: BibleMate Ecosystem Sync
description: >-
  Use when the user runs /biblemate-ecosystem-sync or asks to sync grok-bot-biblemate
  (alias for /gbm-ecosystem-sync; native Grok Bot port).
---
# BibleMate Ecosystem Sync

Slash alias for **GBM Ecosystem Sync** (native Grok Bot port).

## Steps
1. Read and follow `/home/box/agent-data/biblemate-native-skills/gbm-ecosystem-sync/SKILL.md`.
2. Pass through arguments after `/biblemate-ecosystem-sync`.
3. Execute with Grok Bot tools — do not call the `grok` CLI for the sync methodology itself (git via `Shell` is fine).
4. Scope is **only** `/workspace/grok-bot-biblemate`.
5. `SendToUser` the sync result when finished.
