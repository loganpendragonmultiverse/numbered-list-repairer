import hashlib
from pathlib import Path

import pytest

from numbered_list_repairer.cli import main
from numbered_list_repairer.core import analyze


def test_empty_item_between_filled_items_is_counted():
    result = analyze({"text": "7. One\n8. \n9. Three\n"})
    assert result["text"] == "1. One\n2. \n3. Three\n"
    assert result["items"] == 3
    assert len(result["changes"]) == 3


@pytest.mark.parametrize("separator", ["", " ", "\t", " \t  "])
def test_empty_separator_is_preserved(separator):
    result = analyze({"text": "8." + separator + "\r\n9. Filled\r\n"})
    assert result["text"] == "1." + separator + "\r\n2. Filled\r\n"
    assert result["items"] == 2


def test_empty_nested_restart_fence_and_quote_contract():
    source = "8. Parent\n\t8) \t\n\t9) Child\n9. \n```text\n9. \n```\n> 9. \n8.\n"
    result = analyze({"text": source, "restart_lines": [9]})
    assert result["text"] == "1. Parent\n\t1. \t\n\t2. Child\n2. \n```text\n9. \n```\n> 9. \n1.\n"
    assert result["items"] == 5


def test_attached_nonempty_text_is_not_newly_recognized():
    text = "7.word\n7. Word\n"
    assert analyze({"text": text})["text"] == "7.word\n1. Word\n"


def test_direct_empty_items_keep_source_and_crlf(tmp_path: Path):
    source = tmp_path / "draft.md"
    output = tmp_path / "fixed.md"
    original = b"\xef\xbb\xbf8. Filled\r\n9. \t\r\n10. End\r\n"
    source.write_bytes(original)
    digest = hashlib.sha256(original).hexdigest()
    assert main([str(source), "--format", "text", "--output", str(output)]) == 0
    expected = b"1. Filled\r\n2. \t\r\n3. End\r\n"
    assert output.read_bytes() == expected
    assert hashlib.sha256(source.read_bytes()).hexdigest() == digest
    assert main([str(source), "--format", "text", "--output", str(output)]) == 2
    assert output.read_bytes() == expected
