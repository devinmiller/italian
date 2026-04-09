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

## Language

- **Italian study content** (notes, examples, glosses): standard Italian; voice per existing notes.
- **Technical artifacts** (schemas, tooling docs, engineering notes, code comments for scripts): **English**, unless the user asks otherwise.

## Editing principles

- Prefer **minimal, focused edits**: 
  - Change only what the task requires; do not reorganize unrelated files.
  - Do not simply replace unless explicitly ask or information is incorrect, invalid, or violates other explicit rules.
  - Strive to integrate new information into existing information where possible and where it makes sense.
  - Keep related information together, if there are exceptions DO NOT create a seperate section for exceptions, put it inline with the relavent information.
- **Preserve voice, tone, style**: 
  - Unless asked to rewrite for clarity or the voice is not natural for a native Italian speaker, preserve the voice.
  - Keep a consistent style and tone a cross pages and sections within a page.
- For **Italian**: 
  - Use standard Italian spelling and terminology.
  - When grammar is ambiguous, prefer natural, spoken Italian.
  - Note briefly any difference in register and formality.
- For **formatting**: 
  - Prefer tables, lists, bullet points, etc. over blocks of text unless necessary to explain a concept.
  - Do not list all conjugations or ending for words that follow standard patterns.
    - For example, for **ajectives** like *molto* it isn't necessary to list all endings like *molto*/*molta*/*molti*/*molte*.  Simply, *molto/a* will suffice.
  - Do list conjugations and endings for words that are irregular, invariable, or do not follow standard patterns. Deviations from patterns must be noted for clarity.  Do not make assumptions.
    - For example, for **adjectives** like *poco*, list the difference in the endings, like *poco/a (-chi/-che)*
- For **page structure**: 
  - The content of level 1 headings should only be links to lower level headings, but only in scenarios where there is more than 1 lower level heading, or unless explicitly asked.
  - The content of level 1 headings should also include a brief, concise description of page contents.
  - Keep related information together under the same heading.  
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
