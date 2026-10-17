# Changelog

## 1.2.1

- Count and renumber empty outline items while preserving their trailing whitespace, indentation and line endings.
- Preserve existing fence/quote exclusions, filled-item behavior and read-only source/new-output guarantees.


## 1.2.0 - 2026-10-17

- Auto-detect JSON specifications or text/Markdown input by extension with an explicit override
- Support explicit starting numbers and restart lines for direct text input
- Export repaired plain text to a new file in addition to reviewable JSON/Markdown reports

## 1.1.0 - 2026-09-07

- Add exact text diffs, nested numbering and explicit restarts while preserving fences, quotations, continuations and line endings.
- Added regression coverage for the audited behavior and invalid inputs.

## 1.0.0 - 2026-07-26

- Released the first complete Numbered List Repairer command-line workflow.
- Added deterministic reporting, representative examples, cross-platform tests, and explicit limitations.

Raw text written to stdout preserves LF or CRLF bytes on Windows as well as Unix; subprocess regressions exercise both line endings.
