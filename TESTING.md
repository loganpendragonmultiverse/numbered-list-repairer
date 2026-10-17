# Testing

Run `ruff format --check .`, `ruff check .`, `mypy src`, `pytest`, and `python -m build`. CI also audits dependencies and runs the supported OS/Python matrix.

## 1.1.0 regression acceptance

Run the complete existing suite plus the new regression fixtures. Confirm the documented command produces the selected output, malformed input remains actionable, and source files remain unchanged. Add exact text diffs, nested numbering and explicit restarts while preserving fences, quotations, continuations and line endings.

## 1.2.0 acceptance

Repair UTF-8 text and Markdown files directly while preserving their line endings and original source.

Verify Auto-detect JSON specifications or text/Markdown input by extension with an explicit override; Support explicit starting numbers and restart lines for direct text input; Export repaired plain text to a new file in addition to reviewable JSON/Markdown reports. Run the full existing quality and build gates; release only through protected PR checks and verified tag artifacts.

## 1.2.1 empty outline items

Recognize and count common empty marker bodies, including a bare marker at end of line, without accepting attached nonempty text such as `1.word`. Preserve empty-item separator whitespace, indentation and original line endings; retain existing normalization for filled items. Verify an empty item between filled ones, mixed trailing spaces/tabs, nested/restarted lists, fenced-code/quote exclusion, direct UTF-8/BOM/CRLF CLI output, source hashes and existing text/JSON root contracts. No new CommonMark parser or continuation semantics are introduced.
