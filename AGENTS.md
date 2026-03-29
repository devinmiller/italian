# Agent Instructions

This file gives coding and editing agents context for working in this repository. it will be updated as conventions and needs evolve.

## Project Overview

- **Purpose**: Italian study materials, particularly grammar, notes, vocabulary.
- **Stack**: Content should be entirely Markdown and any CSV should be ignored.  This is meant to be an Obsidian (the markdown note taking app) library  

## Layout

| Path | Role | 
|------|------|
| Repository root | Topic notes (e.g. verbs, tenses, pronouns, articles). |
| `inclasse/` | In-class notes, stories, and course-specific CSV/JSON. |
| `flashcards/` | Flashcard exports and vocabulary lists (often CSV). |
| `archive/` | Older or superseded notes and helper scripts. |

## Editing principles

- Prefer **minimal, focused edits**: change only what the task requires; do not reorganize unrelated files.
- **Preserve the learner’s voice** unless asked to rewrite for clarity or the voice is not naturally for a native Italian speaker.
- For **Italian**: use standard Italian spelling and terminology; when grammar is ambiguous, prefer widely taught textbook patterns and note uncertainty briefly if relevant.
- **CSV files**: keep consistent column order within a file; avoid breaking importers (assume comma-separated unless the file clearly uses another delimiter).
- **Markdown**: match existing heading levels and list style in nearby sections.

## What to avoid

- Do not delete or rewrite large bodies of notes without explicit instruction.
- Do not add dependencies, frameworks, or tooling unless the user asks.
- Avoid committing editor-only folders (e.g. local Obsidian config) unless the user wants them tracked.

## Cursor-specific

- Project rules may live under `.cursor/rules/`; prefer those for file-specific or always-on guidance.
- If this file conflicts with a user message, **follow the user message** for that task.

## Checklist before finishing substantive edits

- [ ] Paths and cross-references in edited files still make sense.
- [ ] Italian examples remain accurate for the stated rule or topic.
