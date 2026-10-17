from __future__ import annotations

import difflib
import json
import re
from typing import Any

PROJECT = "numbered-list-repairer"


def _require(data: dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None or value == "" or value == []:
        raise ValueError(f"{key} is required")
    return value


def _numbered_list(data: dict[str, Any]) -> dict[str, Any]:
    text = _require(data, "text")
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    start = data.get("start", 1)
    if not isinstance(start, int) or isinstance(start, bool) or start < 0:
        raise ValueError("start must be non-negative")
    restarts = data.get("restart_lines", [])
    if not isinstance(restarts, list) or not all(
        isinstance(n, int) and not isinstance(n, bool) and n > 0 for n in restarts
    ):
        raise ValueError("restart_lines must be an array of positive line numbers")
    pattern = re.compile(
        "^(?P<indent>\\s*)(?:(?:\\d+|[A-Za-z]|[ivxlcdmIVXLCDM]+)[.)]|[-*+])(?P<spacing>\\s+|$)(?P<body>.*)$"
    )
    repaired = []
    changes = []
    counters: dict[int, int] = {}
    count = 0
    fence: str | None = None
    for line_number, original in enumerate(text.splitlines(keepends=True), 1):
        line = original.rstrip("\r\n")
        ending = original[len(line) :]
        marker = re.match(r"^[ \t]*(`{3,}|~{3,})", line)
        if marker:
            if fence is None:
                fence = marker.group(1)
            elif (
                marker.group(1)[0] == fence[0]
                and len(marker.group(1)) >= len(fence)
                and not line[marker.end() :].strip()
            ):
                fence = None
            repaired.append(original)
            continue
        if fence or line.lstrip().startswith(">"):
            repaired.append(original)
            continue
        match = pattern.match(line)
        if not match:
            repaired.append(original)
            continue
        depth = len(match.group("indent").expandtabs(4))
        counters = {key: value for key, value in counters.items() if key <= depth}
        if line_number in restarts:
            counters[depth] = start
        number = counters.get(depth, start)
        body = match.group("body")
        spacing = " " if body else match.group("spacing")
        replacement = f"{match.group('indent')}{number}.{spacing}{body}"
        repaired.append(replacement + ending)
        if replacement != line:
            changes.append({"line": line_number, "before": line, "after": replacement})
        counters[depth] = number + 1
        count += 1
    result = "".join(repaired)
    return {
        "text": result,
        "changes": changes,
        "items": count,
        "diff": "".join(
            difflib.unified_diff(
                text.splitlines(keepends=True),
                result.splitlines(keepends=True),
                fromfile="original",
                tofile="repaired",
            )
        ),
    }


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise TypeError("input must be a JSON object")
    return {"version": 1, "project": PROJECT, **_numbered_list(data)}


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False, default=str) + "\n"


def render_markdown(report: dict[str, Any]) -> str:
    lines = [f"# {report['project'].replace('-', ' ').title()} report", ""]
    for key, value in report.items():
        if key not in {"version", "project"}:
            lines.extend(
                [
                    f"## {key.replace('_', ' ').title()}",
                    "",
                    f"```json\n{json.dumps(value, indent=2, ensure_ascii=False, default=str)}\n```",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"
