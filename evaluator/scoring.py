"""Funciones puras de puntuacion del instrumento de investigacion.

Este modulo no ejecuta herramientas externas ni depende de las tareas
experimentales T1/T2/T3. Implementa exclusivamente las formulas definidas en
el diseno metodologico:

    R = (requisitos satisfechos / 5) * 100
    F = (pruebas superadas / 10) * 100
    C = transformacion por intervalos de complejidad ciclomatica
    M = Indice de Mantenibilidad de Radon (0-100)
    IR = baja + (3 * media) + (5 * alta)
    S  = max(0, 100 - (5 * IR))
    ICC = (0.20 * R) + (0.20 * F) + (0.20 * C) + (0.20 * M) + (0.20 * S)
"""

from __future__ import annotations

DIMENSIONS = ("R", "F", "C", "M", "S")
WEIGHTS = {"R": 0.20, "F": 0.20, "C": 0.20, "M": 0.20, "S": 0.20}

# Intervalos de complejidad ciclomatica -> puntuacion.
# (limite_superior_inclusive, puntuacion)
COMPLEXITY_BANDS = (
    (5, 100),   # 1 - 5
    (10, 80),   # 6 - 10
    (20, 60),   # 11 - 20
    (30, 40),   # 21 - 30
    (40, 20),   # 31 - 40
)
COMPLEXITY_OVERFLOW_SCORE = 0  # >= 41


def _ensure_number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(
            f"{name} debe ser numerico, se recibio {type(value).__name__}"
        )
    return value


def _ensure_non_negative_int(value, name):
    _ensure_number(value, name)
    if float(value) != int(value):
        raise ValueError(f"{name} debe ser un entero")
    value = int(value)
    if value < 0:
        raise ValueError(f"{name} no puede ser negativo")
    return value


def _ensure_score(value, name):
    _ensure_number(value, name)
    if value < 0 or value > 100:
        raise ValueError(f"{name} debe estar en el rango [0, 100]")
    return float(value)


def calculate_requirements_score(satisfied, total=5):
    """R: porcentaje de requisitos satisfechos."""
    satisfied = _ensure_non_negative_int(satisfied, "satisfied")
    total = _ensure_number(total, "total")
    if total <= 0:
        raise ValueError("total debe ser mayor que cero")
    if satisfied > total:
        raise ValueError("satisfied no puede superar a total")
    return (satisfied / total) * 100.0


def calculate_functional_score(passed, total=10):
    """F: porcentaje de pruebas superadas."""
    passed = _ensure_non_negative_int(passed, "passed")
    total = _ensure_number(total, "total")
    if total <= 0:
        raise ValueError("total debe ser mayor que cero")
    if passed > total:
        raise ValueError("passed no puede superar a total")
    return (passed / total) * 100.0


def calculate_complexity_score(complexity):
    """C: transforma la complejidad ciclomatica media (numero real) segun los intervalos.

    No se redondea la complejidad: se aplican los intervalos directamente
    sobre el valor recibido.
    """
    complexity = _ensure_number(complexity, "complexity")
    if complexity < 1:
        raise ValueError("complexity debe ser mayor o igual a 1")
    for upper_bound, score in COMPLEXITY_BANDS:
        if complexity <= upper_bound:
            return float(score)
    return float(COMPLEXITY_OVERFLOW_SCORE)


def calculate_risk_index(low, medium, high):
    """IR: indice de riesgo combinado de Bandit."""
    low = _ensure_non_negative_int(low, "low")
    medium = _ensure_non_negative_int(medium, "medium")
    high = _ensure_non_negative_int(high, "high")
    return low + (3 * medium) + (5 * high)


def calculate_security_score(low, medium, high):
    """S: puntuacion de seguridad a partir del indice de riesgo."""
    risk_index = calculate_risk_index(low, medium, high)
    return max(0.0, 100.0 - (5 * risk_index))


def calculate_icc(r, f, c, m, s):
    """ICC: indice de calidad del codigo (media ponderada equidistante)."""
    r = _ensure_score(r, "R")
    f = _ensure_score(f, "F")
    c = _ensure_score(c, "C")
    m = _ensure_score(m, "M")
    s = _ensure_score(s, "S")
    values = {"R": r, "F": f, "C": c, "M": m, "S": s}
    return sum(WEIGHTS[key] * values[key] for key in DIMENSIONS)
