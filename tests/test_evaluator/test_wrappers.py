"""Pruebas del instrumento: wrappers de herramientas y captura de salida."""

from pathlib import Path

from evaluator import bandit_runner, pytest_runner, radon_runner

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TARGET = PROJECT_ROOT / "evaluator" / "scoring.py"
REQUIRED_KEYS = {"tool", "command", "exit_code", "stdout", "stderr", "status", "error"}


def test_radon_on_real_file():
    result = radon_runner.run_radon(TARGET)
    assert result["status"] == "ok"
    assert isinstance(result["average_complexity"], (int, float))
    assert isinstance(result["maintainability_index"], (int, float))
    assert REQUIRED_KEYS.issubset(result["cc"].keys())
    assert REQUIRED_KEYS.issubset(result["mi"].keys())


def test_radon_missing_file_records_error(tmp_path):
    result = radon_runner.run_radon(tmp_path / "no_existe.py")
    assert result["status"] == "error"
    assert result["cc"]["exit_code"] is not None
    assert result["cc"]["error"] is not None


def test_bandit_on_real_file():
    result = bandit_runner.run_bandit(TARGET)
    assert result["status"] in ("clean", "issues_found")
    assert REQUIRED_KEYS.issubset(result.keys())
    assert isinstance(result["security_low"], int)
    assert isinstance(result["security_medium"], int)
    assert isinstance(result["security_high"], int)


def test_bandit_missing_file_records_error(tmp_path):
    result = bandit_runner.run_bandit(tmp_path / "no_existe.py")
    assert result["status"] == "error"
    assert result["error"] is not None


def test_parse_pytest_summary():
    output = "3 passed, 2 failed, 1 error in 0.12s"
    summary = pytest_runner.parse_pytest_summary(output)
    assert summary["passed"] == 3
    assert summary["failed"] == 2
    assert summary["errors"] == 1


def test_parse_pytest_summary_empty():
    summary = pytest_runner.parse_pytest_summary("")
    assert summary["passed"] == 0
    assert summary["failed"] == 0


def test_pytest_missing_target_records_exit_code(tmp_path):
    result = pytest_runner.run_pytest(tmp_path / "no_existe.py")
    assert result["status"] == "error"
    assert result["exit_code"] is not None
    assert REQUIRED_KEYS.issubset(result.keys())


def test_wrapper_command_uses_current_interpreter():
    result = radon_runner.run_radon(TARGET)
    assert result["cc"]["command"][1:] == ["-m", "radon", "cc", str(TARGET), "-j"]
