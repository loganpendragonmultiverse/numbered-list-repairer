import pytest

from numbered_list_repairer.core import analyze


def test_nested_continuations_fences_quotes_and_restarts() -> None:
    text = "9. First\n   continued paragraph\n   8. Child\n   9. Child two\n9. Second\n\n```text\n9. Keep code\n```\n> 9. Keep quote\n9. Restart\n"
    report = analyze({"text": text, "restart_lines": [11]})
    assert (
        report["text"]
        == "1. First\n   continued paragraph\n   1. Child\n   2. Child two\n2. Second\n\n```text\n9. Keep code\n```\n> 9. Keep quote\n1. Restart\n"
    )
    assert report["items"] == 5
    assert "-9. First" in report["diff"] and "+1. First" in report["diff"]


def test_crlf_and_unclosed_fences_are_preserved() -> None:
    text = "2. A\r\n~~~\r\n9. Code\r\n"
    assert analyze({"text": text})["text"] == "1. A\r\n~~~\r\n9. Code\r\n"


@pytest.mark.parametrize(
    "extra", [{"text": []}, {"start": True}, {"restart_lines": [0]}, {"restart_lines": "1"}]
)
def test_bad_options(extra) -> None:
    with pytest.raises(ValueError):
        analyze({"text": "1. A", **extra})
