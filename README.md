# Numbered List Repairer

> ⭐ **Gold Star Project**
> I consider this project complete. Fixes, maintenance and good new ideas are still welcome.
> [About Gold Stars](https://www.loganpendragonforge.com/open-source/?gold=1)
>
> Fix numbered lists in text, Markdown or JSON without changing the original file.

## What you can do

- Choose a starting number and when numbering should restart.
- Keep item text, line endings and fenced code intact.
- Save the repaired list as a new file or print it to the terminal.


## Current release 1.3.0

Add `--check` / `--fail-on-change`: print the report and return 1 when repairs are needed, without creating an output file.
Explicit backtick and tilde fences are preserved at any indentation, including fences nested under list items. List-like code inside those fences stays unchanged while surrounding list numbers are repaired. This does not add general Markdown interpretation.

## Updates in 1.2.1

Renumber empty outline items along with filled items. For example, `7. One`, `8. ` and `9. Three` become `1. One`, `2. ` and `3. Three`. Empty markers retain their original following spaces or tabs, including a bare marker with no following space. Indentation, line endings, fenced code, quotations and source-file preservation keep their existing behavior. Filled items retain the existing normalized marker spacing.

## Previous release 1.2.0

Repair UTF-8 text and Markdown files directly while preserving their line endings and original source.

Use `repair-numbering draft.md --format json` to inspect text changes, then `repair-numbering draft.md --format text --output repaired.md` for a new document. .txt, .md and .markdown are direct text; .json remains the existing specification format. --input-format overrides unknown extensions. --start and repeated --restart-line override corresponding JSON options when supplied. UTF-8 BOM input is accepted, original line endings are preserved, and existing outputs or the source are never replaced. This remains a conservative marker utility, not a complete CommonMark parser.

[![CI](https://github.com/loganpendragonmultiverse/numbered-list-repairer/actions/workflows/ci.yml/badge.svg)](https://github.com/loganpendragonmultiverse/numbered-list-repairer/actions/workflows/ci.yml)

Repair skipped, duplicated, malformed, or mixed list numbering while preserving item text. The command uses explicit UTF-8 JSON input and produces reviewable JSON or Markdown output.

## Three-minute start

```bash
python -m pip install .
repair-numbering examples/sample.json
repair-numbering examples/sample.json --format json --output report.json
```

The example documents the v1 input shape. Existing report files are never overwritten. Source inputs are read-only except where the documented purpose explicitly creates a new output artifact.

## Privacy and platforms

The tool runs locally and does not upload input or include telemetry. Python 3.10 or newer is supported on Windows, macOS, and Linux.

## Interpretation boundary

The repairer recognizes common one-line markers. Nested semantics, continuation paragraphs, and intentional numbering require review.

## Development

```bash
python -m pip install -e ".[dev]"
ruff format --check .
ruff check .
mypy src
pytest
python -m build
```

The project is feature-complete for its documented v1 scope. Maintenance focuses on correctness, security, compatibility, and well-supported input improvements.

Part of the [Logan Pendragon Forge open-source collection](https://www.loganpendragonforge.com/open-source/). Licensed under the [MIT License](LICENSE).

## Updates in 1.1.0

Add exact text diffs, nested numbering and explicit restarts while preserving fences, quotations, continuations and line endings.

```bash
repair-numbering examples/sample.json --format json
```

`restart_lines` is an optional array of one-based source line numbers that restart numbering at the configured `start`. Indentation levels maintain separate counters; tabs use four-column expansion for that calculation. Fenced code and blockquotes are left unchanged, as are unrecognized continuation paragraphs and original line endings. The `diff` field shows the exact before/after text. This is a conservative text utility, not a complete CommonMark parser: use explicit fenced code for code preservation and inspect the diff before applying it elsewhere.

## 1.3.0 report controls

Use `--check` (or `--fail-on-change`) to print the selected report and exit 1 when repairs are needed, 0 when unchanged, or 2 on an input/output error. Check mode rejects `--output` and leaves the source unchanged.

## Changes prepared for 1.3.1

Failed stdout writes, including a closed pipe, return exit status 2 with an error diagnostic. Normal report contents and existing file-preservation behavior are unchanged.
