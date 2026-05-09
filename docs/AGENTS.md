# AGENTS.md

## Repository Overview

Minimal snippet repo for Google Sheets data fetching via the gviz JSONP API. No build system, package manager, or tests.

## Key Files

- `gsheet-code.md` — Main code snippet: `fetchSheet(gid)` uses JSONP to fetch a sheet tab by GID and returns an array of objects.
- `env.local` — Contains `google_id` (the Google Sheet ID). This value is referenced in the code as `SHEET_ID`.

## Runtime Notes

- This is browser-only code (uses `document.createElement('script')` and `window`).
- `SHEETS.sheet1` and `SHEETS.sheet2` are assumed to be defined externally (not in this repo).
- Requests timeout at 20 seconds.
- The gviz endpoint used: `https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?gid=${gid}&tqx=responseHandler:${cb}`

## No Tooling

- No `package.json`, no build step, no linter, no test runner.
- If you add a build/test setup, create the standard config files and update this file.
