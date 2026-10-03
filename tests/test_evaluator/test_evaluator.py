"""Pruebas del instrumento: plantilla y coordinacion del evaluador."""

from pathlib import Path

from evaluator import evaluator

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TARGET = PROJECT_ROOT / "evaluator" / "scoring.py"


def test_result_template_has_all_fields():
    result = evaluator.create_result_template("s1", "chatgpt", "T1", 1)
    assert set(evaluator.RESULT_TEMPLATE_FIELDS).issubset(result.keys())
    assert result["ICC"] is None
    assert result["incidents"] == []


def test_evaluate_sample_with_syntax_error(tmp_path):
    broken = tmp_path / "broken.py"
    broken.write_text("def f(:\n", encoding="utf-8")
    result = evaluator.evaluate_sample(
        sample_id="s1",
        system="chatgpt",
        task="T1",
        repetition=1,
        code_path=broken,
    )
    assert result["syntax_valid"] is False
    assert result["ICC"] is None
    assert len(result["incidents"]) >= 1


def test_evaluate_sample_static_only():
    result = evaluator.evaluate_sample(
        sample_id="s1",
        system="deepseek",
        task="T1",
        repetition=1,
        code_path=TARGET,
    )
    assert result["syntax_valid"] is True
    assert result["C"] is not None
    assert result["M"] is not None
    assert result["S"] is not None
    assert result["R"] is None
    assert result["F"] is None
    assert result["ICC"] is None


def test_evaluate_sample_full_scoring():
    result = evaluator.evaluate_sample(
        sample_id="s1",
        system="opencode",
        task="T1",
        repetition=1,
        code_path=TARGET,
        requirements=[1, 1, 1, 1, 1],
    )
    assert result["R"] == 100.0
    assert result["C"] is not None
    assert result["M"] is not None
    assert result["S"] is not None
    # Sin pruebas funcionales no se calcula ICC.
    assert result["F"] is None
    assert result["ICC"] is None


def test_evaluate_sample_wrong_requirement_count():
    import pytest

    with pytest.raises(ValueError):
        evaluator.evaluate_sample(
            sample_id="s1",
            system="opencode",
            task="T1",
            repetition=1,
            code_path=TARGET,
            requirements=[1, 0],
        )


def test_apply_scoring_invalid_complexity_is_incident():
    result = evaluator.create_result_template("s1", "chatgpt", "T1", 1)
    result["cyclomatic_complexity"] = 0.5
    evaluator._apply_scoring(result)
    assert result["C"] is None
    assert any(incident["stage"] == "scoring" for incident in result["incidents"])
