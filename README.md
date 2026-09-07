# Numbered List Repairer

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

## Version 1.1.0: reviewed improvements

Add exact text diffs, nested numbering and explicit restarts while preserving fences, quotations, continuations and line endings.

```bash
repair-numbering examples/sample.json --format json
```

`restart_lines` is an optional array of one-based source line numbers that restart numbering at the configured `start`. Indentation levels maintain separate counters; tabs use four-column expansion for that calculation. Fenced code and blockquotes are left unchanged, as are unrecognized continuation paragraphs and original line endings. The `diff` field shows the exact before/after text. This is a conservative text utility, not a complete CommonMark parser: use explicit fenced code for code preservation and inspect the diff before applying it elsewhere.
