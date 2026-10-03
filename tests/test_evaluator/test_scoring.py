"""Pruebas del instrumento: funciones puras de scoring."""

import pytest

from evaluator import scoring


# ---------------------------------------------------------------------------
# R: cumplimiento de requisitos
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "satisfied, expected",
    [(0, 0.0), (1, 20.0), (3, 60.0), (5, 100.0)],
)
def test_requirements_score(satisfied, expected):
    assert scoring.calculate_requirements_score(satisfied) == expected


@pytest.mark.parametrize("bad", [-1, 6, 10])
def test_requirements_score_invalid_satisfied(bad):
    with pytest.raises(ValueError):
        scoring.calculate_requirements_score(bad)


def test_requirements_score_invalid_total():
    with pytest.raises(ValueError):
        scoring.calculate_requirements_score(1, total=0)


def test_requirements_score_non_numeric():
    with pytest.raises(TypeError):
        scoring.calculate_requirements_score("tres")


# ---------------------------------------------------------------------------
# F: correccion funcional
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "passed, expected",
    [(0, 0.0), (5, 50.0), (10, 100.0)],
)
def test_functional_score(passed, expected):
    assert scoring.calculate_functional_score(passed) == expected


def test_functional_score_invalid():
    with pytest.raises(ValueError):
        scoring.calculate_functional_score(11)


# ---------------------------------------------------------------------------
# C: complejidad (los seis intervalos)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "complexity, expected",
    [
        (1, 100.0), (5, 100.0),        # 1 <= CC <= 5
        (5.0, 100.0),
        (6, 80.0), (10, 80.0),         # 5 < CC <= 10
        (10.0, 80.0),
        (11, 60.0), (20, 60.0),        # 10 < CC <= 20
        (20.0, 60.0),
        (21, 40.0), (30, 40.0),        # 20 < CC <= 30
        (30.0, 40.0),
        (31, 20.0), (40, 20.0),        # 30 < CC <= 40
        (40.0, 20.0),
        (41, 0.0), (100, 0.0),         # CC > 40
        (40.1, 0.0),
    ],
)
def test_complexity_score(complexity, expected):
    assert scoring.calculate_complexity_score(complexity) == expected


@pytest.mark.parametrize(
    "complexity, expected",
    [
        (5.4, 80.0),
        (10.4, 60.0),
        (20.4, 40.0),
        (30.4, 20.0),
        (40.4, 0.0),
    ],
)
def test_complexity_score_no_rounding(complexity, expected):
    # Con redondeo a entero estos valores caerian en un intervalo distinto.
    assert scoring.calculate_complexity_score(complexity) == expected


@pytest.mark.parametrize("bad", [0, 0.5, -1, -0.1])
def test_complexity_score_invalid(bad):
    with pytest.raises(ValueError):
        scoring.calculate_complexity_score(bad)


@pytest.mark.parametrize("bad", [True, False, "3", None])
def test_complexity_score_non_numeric(bad):
    with pytest.raises(TypeError):
        scoring.calculate_complexity_score(bad)


# ---------------------------------------------------------------------------
# IR: indice de riesgo
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "low, medium, high, expected",
    [
        (0, 0, 0, 0),
        (1, 0, 0, 1),
        (0, 1, 0, 3),
        (0, 0, 1, 5),
        (1, 1, 1, 9),
        (2, 3, 4, 2 + 9 + 20),
    ],
)
def test_risk_index(low, medium, high, expected):
    assert scoring.calculate_risk_index(low, medium, high) == expected


def test_risk_index_invalid():
    with pytest.raises(ValueError):
        scoring.calculate_risk_index(-1, 0, 0)


# ---------------------------------------------------------------------------
# S: seguridad
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "low, medium, high, expected",
    [
        (0, 0, 0, 100.0),
        (1, 0, 0, 95.0),
        (0, 0, 1, 75.0),
        (1, 1, 1, 55.0),
        (0, 0, 20, 0.0),
        (100, 100, 100, 0.0),
    ],
)
def test_security_score(low, medium, high, expected):
    assert scoring.calculate_security_score(low, medium, high) == expected


def test_security_score_never_negative():
    assert scoring.calculate_security_score(10, 10, 10) == 0.0


# ---------------------------------------------------------------------------
# ICC
# ---------------------------------------------------------------------------
def test_icc_all_100():
    assert scoring.calculate_icc(100, 100, 100, 100, 100) == 100.0


def test_icc_all_0():
    assert scoring.calculate_icc(0, 0, 0, 0, 0) == 0.0


def test_icc_mixed():
    result = scoring.calculate_icc(100, 80, 60, 40, 20)
    assert result == pytest.approx(60.0)


@pytest.mark.parametrize("bad", [-1, 101, 200])
def test_icc_out_of_range(bad):
    with pytest.raises(ValueError):
        scoring.calculate_icc(bad, 100, 100, 100, 100)


def test_icc_non_numeric():
    with pytest.raises(TypeError):
        scoring.calculate_icc("a", 100, 100, 100, 100)


def test_icc_weights_are_equal():
    assert scoring.WEIGHTS == {"R": 0.2, "F": 0.2, "C": 0.2, "M": 0.2, "S": 0.2}
