import json
from pathlib import Path

from numbered_list_repairer.cli import main


def test_direct_markdown_preserves_bytes_and_writes_new_text(tmp_path: Path, capsys):
    source = tmp_path / "draft.md"
    output = tmp_path / "repaired.md"
    original = "8. One Ω\r\n9. Two\r\n```\r\n7. Code\r\n```\r\n"
    source.write_bytes(original.encode())
    assert main([str(source), "--format", "json"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["text"] == original.replace("8. One", "1. One").replace("9. Two", "2. Two")
    assert main([str(source), "--format", "text", "--output", str(output)]) == 0
    assert output.read_bytes() == report["text"].encode()
    assert source.read_bytes() == original.encode()
    assert main([str(source), "--format", "text", "--output", str(output)]) == 2


def test_explicit_mode_start_restart_and_invalid_options(tmp_path: Path, capsys):
    path = tmp_path / "input.custom"
    path.write_text("7. One\n8. Two\n9. Three")
    assert main([str(path)]) == 2
    assert (
        main(
            [
                str(path),
                "--input-format",
                "text",
                "--start",
                "3",
                "--restart-line",
                "3",
                "--format",
                "text",
            ]
        )
        == 0
    )
    assert capsys.readouterr().out == "3. One\n4. Two\n3. Three"
    assert main([str(path), "--input-format", "text", "--start", "-1"]) == 2
    assert main([str(path), "--input-format", "text", "--restart-line", "0"]) == 2
    path.write_text("")
    assert main([str(path), "--input-format", "text"]) == 2
