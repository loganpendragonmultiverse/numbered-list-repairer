import io
import json
import os
import subprocess
import sys

import pytest

from numbered_list_repairer.cli import _write_stdout


def invocation(tmp_path, large, format_name="json"):
    source = tmp_path / "outline.md"
    source.write_bytes(("9. Ω item\r\n" * (1000 if large else 1)).encode())
    args = [source, "--format", format_name]
    return source, args


@pytest.mark.parametrize("large", [False, True])
@pytest.mark.parametrize("format_name", ["json", "text"])
def test_normal_stdout_is_complete_and_preserves_input(tmp_path, large, format_name):
    source, args = invocation(tmp_path, large, format_name)
    before = source.read_bytes()
    result = subprocess.run(
        [sys.executable, "-m", "numbered_list_repairer", *map(str, args)],
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert not result.stderr
    assert source.read_bytes() == before
    assert len(result.stdout) > 8192 if large else len(result.stdout) < 8192
    if format_name == "text":
        expected = "".join(f"{i}. Ω item\r\n" for i in range(1, 1001 if large else 2)).encode(
            "utf-8"
        )
        assert result.stdout == expected
    else:
        assert json.loads(result.stdout)


@pytest.mark.parametrize("large", [False, True])
@pytest.mark.parametrize("format_name", ["json", "text"])
def test_closed_stdout_pipe_returns_two_without_shutdown_warning(tmp_path, large, format_name):
    source, args = invocation(tmp_path, large, format_name)
    before = source.read_bytes()
    reader, writer = os.pipe()
    os.close(reader)
    try:
        result = subprocess.run(
            [sys.executable, "-m", "numbered_list_repairer", *map(str, args)],
            stdout=writer,
            stderr=subprocess.PIPE,
            check=False,
        )
    finally:
        os.close(writer)
    assert result.returncode == 2, result.stderr
    assert b"error:" in result.stderr
    assert b"Exception ignored" not in result.stderr
    assert b"Traceback" not in result.stderr
    assert source.read_bytes() == before
    assert not list(tmp_path.glob("*.report"))


def test_in_memory_stdout_is_not_replaced_or_closed(monkeypatch):
    stream = io.StringIO()
    monkeypatch.setattr(sys, "stdout", stream)
    _write_stdout("Complete Ω report\n")
    assert sys.stdout is stream and not stream.closed
    assert stream.getvalue() == "Complete Ω report\n"
    stream.write("still open")


@pytest.mark.parametrize("zero", [False, True])
def test_descriptor_short_and_zero_writes(monkeypatch, zero):
    class Output:
        encoding = "utf-8"
        errors = "strict"

        def fileno(self):
            return 123

    stream = Output()
    received = bytearray()

    def write(descriptor, remaining):
        assert descriptor == 123
        if zero:
            return 0
        received.extend(remaining[:7])
        return min(7, len(remaining))

    monkeypatch.setattr(sys, "stdout", stream)
    monkeypatch.setattr(os, "write", write)
    if zero:
        with pytest.raises(OSError, match="no report bytes"):
            _write_stdout("Complete Ω report\n")
    else:
        _write_stdout("Complete Ω report\n")
        assert received == "Complete Ω report\n".encode()
    assert sys.stdout is stream


def test_raw_text_stdout_keeps_utf8_with_non_utf8_terminal(monkeypatch):
    class Output:
        encoding = "ascii"
        errors = "strict"

        def fileno(self):
            return 123

    received = bytearray()

    def write(descriptor, remaining):
        received.extend(remaining)
        return len(remaining)

    monkeypatch.setattr(sys, "stdout", Output())
    monkeypatch.setattr(os, "write", write)
    _write_stdout("1. Ω\r\n", raw_text=True)
    assert received == "1. Ω\r\n".encode()
