# Development contract

Repair skipped, duplicated, malformed, or mixed list numbering while preserving item text.

Preserve deterministic, source-safe behavior and the interpretation boundary documented in the README. Every feature release must update tests, version metadata, changelog, README claims, repository metadata, release assets, and the Forge catalog together.

## 1.1.0 improvement session

Add exact text diffs, nested numbering and explicit restarts while preserving fences, quotations, continuations and line endings.

`restart_lines` is an optional array of one-based source line numbers that restart numbering at the configured `start`. Indentation levels maintain separate counters; tabs use four-column expansion for that calculation. Fenced code and blockquotes are left unchanged, as are unrecognized continuation paragraphs and original line endings. The `diff` field shows the exact before/after text. This is a conservative text utility, not a complete CommonMark parser: use explicit fenced code for code preservation and inspect the diff before applying it elsewhere.

Local formatting, lint, strict types and regression tests pass. Public release completion requires the protected CI/CodeQL matrix, tagged artifacts and matching Forge catalog/detail deployment.

## 1.2.0 acceptance

Repair UTF-8 text and Markdown files directly while preserving their line endings and original source.

Use `repair-numbering draft.md --format json` to inspect text changes, then `repair-numbering draft.md --format text --output repaired.md` for a new document. .txt, .md and .markdown are direct text; .json remains the existing specification format. --input-format overrides unknown extensions. --start and repeated --restart-line override corresponding JSON options when supplied. UTF-8 BOM input is accepted, original line endings are preserved, and existing outputs or the source are never replaced. This remains a conservative marker utility, not a complete CommonMark parser.

## Prior Gold Star review — October 17, 2026

Previously reviewed release: v1.2.1.
Fix numbered lists in text, Markdown or JSON without changing the original file.

Logan considers this project complete. Continue fixes and maintenance, and consider good new ideas. The catalog records the reviewed release.

Definition: https://www.loganpendragonforge.com/open-source/?gold=1

## 1.2.1 empty outline items

Recognize and count common empty marker bodies, including a bare marker at end of line, without accepting attached nonempty text such as `1.word`. Preserve empty-item separator whitespace, indentation and original line endings; retain existing normalization for filled items. Verify an empty item between filled ones, mixed trailing spaces/tabs, nested/restarted lists, fenced-code/quote exclusion, direct UTF-8/BOM/CRLF CLI output, source hashes and existing text/JSON root contracts. No new CommonMark parser or continuation semantics are introduced.

## 1.3.0 report controls

Use `--check` (or `--fail-on-change`) to print the selected report and exit 1 when repairs are needed, 0 when unchanged, or 2 on an input/output error. Check mode rejects `--output` and leaves the source unchanged.

## 1.3.1 stdout regression acceptance

Exercise real closed stdout pipes with small and large reports, complete normal output, partial and zero descriptor writes, and in-memory streams. Verify status 2 without an ignored shutdown exception, unchanged source files, and existing report and output-file contracts.
