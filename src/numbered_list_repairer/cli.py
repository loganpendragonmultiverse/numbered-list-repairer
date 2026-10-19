from __future__ import annotations

import argparse
import io
import json
import os
import sys
from pathlib import Path

from .core import analyze, render_json, render_markdown


def _write_stdout(rendered: str, *, raw_text: bool = False) -> None:
    """Deliver report bytes without leaving a failed buffered write for shutdown."""
    try:
        descriptor = sys.stdout.fileno()
    except (AttributeError, io.UnsupportedOperation):
        stream = getattr(sys.stdout, "buffer", None) if raw_text else None
        if stream is not None:
            stream.write(rendered.encode("utf-8"))
            stream.flush()
        else:
            sys.stdout.write(rendered)
            sys.stdout.flush()
        return
    encoding = "utf-8" if raw_text else sys.stdout.encoding or "utf-8"
    pending = memoryview(rendered.encode(encoding, sys.stdout.errors or "strict"))
    while pending:
        written = os.write(descriptor, pending)
        if written <= 0:
            raise OSError("stdout accepted no report bytes")
        pending = pending[written:]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Repair numbered text from a JSON specification or UTF-8 text/Markdown file."
    )
    parser.add_argument("input", type=Path, help="UTF-8 JSON, text or Markdown input file")
    parser.add_argument("--input-format", choices=("auto", "json", "text"), default="auto")
    parser.add_argument("--start", type=int, help="Override initial numbering")
    parser.add_argument(
        "--restart-line",
        type=int,
        action="append",
        help="One-based line to restart; repeat as needed",
    )
    parser.add_argument("--format", choices=("markdown", "json", "text"), default="markdown")
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--check",
        "--fail-on-change",
        action="store_true",
        help="Report repairs without writing a file; exit 1 when changes are needed",
    )
    args = parser.parse_args(argv)
    try:
        if args.check and args.output:
            raise ValueError("--check cannot be combined with --output")
        mode = args.input_format
        if mode == "auto":
            if args.input.suffix.lower() == ".json":
                mode = "json"
            elif args.input.suffix.lower() in {".txt", ".md", ".markdown"}:
                mode = "text"
            else:
                raise ValueError("choose --input-format json or text for this file extension")
        with args.input.open(encoding="utf-8-sig", newline="") as source:
            text = source.read()
        data = json.loads(text) if mode == "json" else {"text": text}
        if not isinstance(data, dict):
            raise TypeError("input must be a JSON object")
        if args.start is not None:
            data["start"] = args.start
        if args.restart_line is not None:
            data["restart_lines"] = args.restart_line
        report = analyze(data)
        rendered = (
            report["text"]
            if args.format == "text"
            else render_json(report)
            if args.format == "json"
            else render_markdown(report)
        )
        if args.output:
            if args.output.exists():
                raise ValueError(f"output already exists: {args.output}")
            with args.output.open("x", encoding="utf-8", newline="") as output_file:
                output_file.write(rendered)
        else:
            _write_stdout(rendered, raw_text=args.format == "text")
    except (OSError, UnicodeError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 1 if args.check and report["changes"] else 0
