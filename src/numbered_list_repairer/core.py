from __future__ import annotations

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
    text = str(_require(data, "text"))
    start = int(data.get("start", 1))
    if start < 0:
        raise ValueError("start must be non-negative")
    pattern = re.compile(
        "^(?P<indent>\\s*)(?:(?:\\d+|[A-Za-z]|[ivxlcdmIVXLCDM]+)[.)]|[-*+])\\s+(?P<body>.+)$"
    )
    repaired = []
    changes = []
    number = start
    for line_number, line in enumerate(text.splitlines(), 1):
        match = pattern.match(line)
        if not match:
            repaired.append(line)
            continue
        replacement = f"{match.group('indent')}{number}. {match.group('body')}"
        repaired.append(replacement)
        if replacement != line:
            changes.append({"line": line_number, "before": line, "after": replacement})
        number += 1
    return {"text": "\n".join(repaired), "changes": changes, "items": number - start}


def analyze(data: dict[str, Any]) -> dict[str, Any]:
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
