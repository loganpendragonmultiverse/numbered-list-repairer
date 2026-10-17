from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import analyze, render_json, render_markdown


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
    args = parser.parse_args(argv)
    try:
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
            sys.stdout.write(rendered)
    except (OSError, UnicodeError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0
