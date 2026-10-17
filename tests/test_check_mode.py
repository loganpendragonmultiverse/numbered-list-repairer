import json

import pytest

from numbered_list_repairer.cli import main


@pytest.mark.parametrize("flag", ["--check", "--fail-on-change"])
def test_check_reports_change_without_writing(tmp_path, capsys, flag):
    source = tmp_path / "list.md"
    source.write_bytes(b"9. one\r\n8. two\r\n")
    before = source.read_bytes()
    assert main([str(source), flag, "--format", "json"]) == 1
    report = json.loads(capsys.readouterr().out)
    assert len(report["changes"]) == 2
    assert source.read_bytes() == before
    source.write_text("1. one\n2. two\n", encoding="utf-8")
    assert main([str(source), flag]) == 0
    capsys.readouterr()
    output = tmp_path / "out.md"
    assert main([str(source), flag, "--output", str(output)]) == 2
    assert "--check" in capsys.readouterr().err
    assert not output.exists()
