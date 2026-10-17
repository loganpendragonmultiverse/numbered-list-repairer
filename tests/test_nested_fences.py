from pathlib import Path

import pytest

from numbered_list_repairer.cli import main
from numbered_list_repairer.core import analyze


@pytest.mark.parametrize("indent", ["    ", "        ", "\t"])
@pytest.mark.parametrize("fence", ["```", "~~~~"])
def test_indented_explicit_fences_preserve_literal_markers(indent: str, fence: str) -> None:
    text = f"9. Parent\n{indent}{fence}text\n{indent}9. Keep literal\n{indent}8. \n{indent}{fence}\n9. Next\n"
    result = analyze({"text": text})
    assert result["text"] == text.replace("9. Parent", "1. Parent").replace("9. Next", "2. Next")
    assert result["items"] == 2
    assert [change["line"] for change in result["changes"]] == [1, 6]


def test_nested_fence_cli_preserves_crlf_and_source(tmp_path: Path) -> None:
    source = tmp_path / "nested.md"
    original = b"\xef\xbb\xbf9. Parent\r\n    ```\r\n    9. Literal code\r\n    ```\r\n9. Next\r\n"
    source.write_bytes(original)
    target = tmp_path / "repaired.md"
    assert main([str(source), "--format", "text", "--output", str(target)]) == 0
    assert target.read_bytes() == original.removeprefix(b"\xef\xbb\xbf").replace(
        b"9. Parent", b"1. Parent"
    ).replace(b"9. Next", b"2. Next")
    assert source.read_bytes() == original
