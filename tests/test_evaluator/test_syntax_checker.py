"""Pruebas del instrumento: comprobador de sintaxis."""

from pathlib import Path

from evaluator.syntax_checker import (
    FILE_NOT_FOUND,
    READ_ERROR,
    SYNTAX_ERROR,
    VALID,
    check_syntax,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_valid_file():
    target = PROJECT_ROOT / "evaluator" / "scoring.py"
    result = check_syntax(target)
    assert result.valid is True
    assert result.status == VALID
    assert result.exists is True
    assert result.to_dict()["status"] == VALID


def test_syntax_error_file(tmp_path):
    target = tmp_path / "broken.py"
    target.write_text("def f(:\n    return 1\n", encoding="utf-8")
    result = check_syntax(target)
    assert result.valid is False
    assert result.status == SYNTAX_ERROR
    assert result.error_type == "SyntaxError"
    assert result.line is not None


def test_file_not_found(tmp_path):
    target = tmp_path / "no_existe.py"
    result = check_syntax(target)
    assert result.valid is False
    assert result.status == FILE_NOT_FOUND
    assert result.exists is False


def test_read_error(tmp_path):
    target = tmp_path / "binario.py"
    target.write_bytes(b"\xff\xfe\x00\x01\x80")
    result = check_syntax(target)
    assert result.valid is False
    assert result.status == READ_ERROR


def test_does_not_modify_file(tmp_path):
    target = tmp_path / "estable.py"
    original = "x = 1\n"
    target.write_text(original, encoding="utf-8")
    check_syntax(target)
    assert target.read_text(encoding="utf-8") == original
