"""Instrumento de evaluacion de T3 (fase T3-A).

Contiene los 10 casos funcionales derivados exclusivamente de
tasks/T3/prompt.md. No incluye ni depende de ninguna muestra experimental.

Carga de la muestra
-------------------
La ruta del archivo Python a evaluar se recibe mediante la variable de
entorno SEAT_SAMPLE_PATH. El modulo se importa dinamicamente y debe exponer la
funcion `evaluar_expresion`. Si la variable no esta definida, los casos se
omiten (skip) para no romper la ejecucion del resto del instrumento.

Ejemplo de uso:
    $env:SEAT_SAMPLE_PATH = "ruta\\a\\la\\muestra.py"
    .venv\\Scripts\\python.exe -m pytest tasks\\T3\\tests\\test_t3.py -q

No se fija ninguna ruta hacia samples/chatgpt, samples/deepseek ni
samples/opencode.

Nota: estos tests miden el cumplimiento funcional. No penalizan estrategias
internas (eval, ast, operadores, etc.); la seguridad se mide con Bandit en T3-B.
"""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path

import pytest

SAMPLE_ENV_VAR = "SEAT_SAMPLE_PATH"
SAMPLE_FUNCTION_NAME = "evaluar_expresion"

_SAMPLE_PATH = os.environ.get(SAMPLE_ENV_VAR)

pytestmark = pytest.mark.skipif(
    not _SAMPLE_PATH,
    reason=(
        f"Variable de entorno {SAMPLE_ENV_VAR} no definida: no hay muestra "
        "de T3 que cargar."
    ),
)


def _load_sample_function():
    """Importa la muestra indicada por SEAT_SAMPLE_PATH y devuelve la funcion."""
    path = Path(_SAMPLE_PATH)
    if not path.is_file():
        pytest.fail(f"La muestra indicada no existe: {path}", pytrace=False)
    try:
        spec = importlib.util.spec_from_file_location("seat_t3_sample", path)
    except Exception as exc:  # noqa: BLE001 - reportar fallo claro de carga
        pytest.fail(f"No se pudo preparar la importacion de {path}: {exc}", pytrace=False)
    if spec is None or spec.loader is None:
        pytest.fail(f"No se pudo preparar la importacion de: {path}", pytrace=False)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:  # noqa: BLE001
        pytest.fail(f"El modulo de la muestra no pudo cargarse: {exc}", pytrace=False)
    function = getattr(module, SAMPLE_FUNCTION_NAME, None)
    if not callable(function):
        pytest.fail(
            f"La muestra no define la funcion {SAMPLE_FUNCTION_NAME}()",
            pytrace=False,
        )
    return function


@pytest.fixture(scope="module")
def evaluar_expresion():
    return _load_sample_function()


# ---------------------------------------------------------------------------
# T3-C01 - Precedencia basica
# ---------------------------------------------------------------------------
def test_t3_c01_precedencia_basica(evaluar_expresion):
    resultado = evaluar_expresion("2 + 3 * 4")
    assert resultado == pytest.approx(14)


# ---------------------------------------------------------------------------
# T3-C02 - Parentesis
# ---------------------------------------------------------------------------
def test_t3_c02_parentesis(evaluar_expresion):
    resultado = evaluar_expresion("(2 + 3) * 4")
    assert resultado == pytest.approx(20)


# ---------------------------------------------------------------------------
# T3-C03 - Division y resultado decimal
# ---------------------------------------------------------------------------
def test_t3_c03_division_decimal(evaluar_expresion):
    assert evaluar_expresion("10 / 4") == pytest.approx(2.5)
    assert evaluar_expresion("2.5 + 1.25") == pytest.approx(3.75)


# ---------------------------------------------------------------------------
# T3-C04 - Operador unario simple
# ---------------------------------------------------------------------------
def test_t3_c04_unario_simple(evaluar_expresion):
    assert evaluar_expresion("-5 + 2") == pytest.approx(-3)
    assert evaluar_expresion("+5 - 2") == pytest.approx(3)


# ---------------------------------------------------------------------------
# T3-C05 - Unarios, parentesis y expresion compuesta
# ---------------------------------------------------------------------------
def test_t3_c05_unario_parentesis_compuesto(evaluar_expresion):
    assert evaluar_expresion("-(3 + 2) * 4") == pytest.approx(-20)
    assert evaluar_expresion("-  ( 3 + 2 )  *  4") == pytest.approx(-20)


# ---------------------------------------------------------------------------
# T3-C06 - Variables, llamadas y atributos
# ---------------------------------------------------------------------------
def test_t3_c06_variables_llamadas_atributos(evaluar_expresion):
    for expresion in ("x + 1", "abs(5)", "obj.valor", "(1).__class__"):
        with pytest.raises(ValueError):
            evaluar_expresion(expresion)


# ---------------------------------------------------------------------------
# T3-C07 - Colecciones, lambda y comprensiones
# ---------------------------------------------------------------------------
def test_t3_c07_colecciones_lambda_comprensiones(evaluar_expresion):
    for expresion in (
        "[1, 2]",
        "(1, 2)",
        "{'a': 1}",
        "{1, 2}",
        "lambda x: x",
        "[x for x in [1,2]]",
    ):
        with pytest.raises(ValueError):
            evaluar_expresion(expresion)


# ---------------------------------------------------------------------------
# T3-C08 - Operadores y construcciones no permitidas
# ---------------------------------------------------------------------------
def test_t3_c08_operadores_prohibidos(evaluar_expresion):
    for expresion in (
        "2 ** 3",
        "5 // 2",
        "5 % 2",
        "1 < 2",
        "True and False",
        "x = 1",
        "import os",
    ):
        with pytest.raises(ValueError):
            evaluar_expresion(expresion)


# ---------------------------------------------------------------------------
# T3-C09 - Sintaxis invalida
# ---------------------------------------------------------------------------
def test_t3_c09_sintaxis_invalida(evaluar_expresion):
    for expresion in ("2 +", "(3 * 4", ""):
        with pytest.raises(ValueError):
            evaluar_expresion(expresion)


# ---------------------------------------------------------------------------
# T3-C10 - Division por cero, tipo principal y determinismo
# ---------------------------------------------------------------------------
def test_t3_c10_errores_tipo_determinismo(evaluar_expresion):
    # A) division por cero
    with pytest.raises(ZeroDivisionError):
        evaluar_expresion("10 / 0")

    # B) tipo principal incorrecto
    for argumento in (123, None):
        with pytest.raises(TypeError):
            evaluar_expresion(argumento)

    # C) determinismo
    expresion = "((10 - 2) / 4) + 3 * 2"
    resultados = [evaluar_expresion(expresion) for _ in range(5)]
    assert isinstance(resultados[0], (int, float))
    assert all(resultado == resultados[0] for resultado in resultados)
