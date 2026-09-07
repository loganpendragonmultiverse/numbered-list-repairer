# Development contract

Repair skipped, duplicated, malformed, or mixed list numbering while preserving item text.

Preserve deterministic, source-safe behavior and the interpretation boundary documented in the README. Every feature release must update tests, version metadata, changelog, README claims, repository metadata, release assets, and the Forge catalog together.

## 1.1.0 improvement session

Add exact text diffs, nested numbering and explicit restarts while preserving fences, quotations, continuations and line endings.

`restart_lines` is an optional array of one-based source line numbers that restart numbering at the configured `start`. Indentation levels maintain separate counters; tabs use four-column expansion for that calculation. Fenced code and blockquotes are left unchanged, as are unrecognized continuation paragraphs and original line endings. The `diff` field shows the exact before/after text. This is a conservative text utility, not a complete CommonMark parser: use explicit fenced code for code preservation and inspect the diff before applying it elsewhere.

Local formatting, lint, strict types and regression tests pass. Public release completion requires the protected CI/CodeQL matrix, tagged artifacts and matching Forge catalog/detail deployment.
