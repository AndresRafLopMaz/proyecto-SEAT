"""Instrumento de evaluacion de T1 (fase T1-A).

Contiene los 10 casos funcionales derivados exclusivamente de
tasks/T1/prompt.md. No incluye ni depende de ninguna muestra experimental.

Carga de la muestra
-------------------
La ruta del archivo Python a evaluar se recibe mediante la variable de
entorno SEAT_SAMPLE_PATH. El modulo se importa dinamicamente y debe exponer la
funcion `analizar_mediciones`. Si la variable no esta definida, los casos se
omiten (skip) para no romper la ejecucion del resto del instrumento.

Ejemplo de uso:
    $env:SEAT_SAMPLE_PATH = "ruta\\a\\la\\muestra.py"
    .venv\\Scripts\\python.exe -m pytest tasks\\T1\\tests\\test_t1.py -q

No se fija ninguna ruta hacia samples/chatgpt, samples/deepseek ni
samples/opencode.
"""

from __future__ import annotations

import copy
import importlib.util
import os
from pathlib import Path

import pytest

SAMPLE_ENV_VAR = "SEAT_SAMPLE_PATH"
SAMPLE_FUNCTION_NAME = "analizar_mediciones"

TOP_LEVEL_KEYS = {
    "validas",
    "invalidas",
    "promedio_general",
    "minimo_general",
    "maximo_general",
    "por_sensor",
}
SENSOR_KEYS = {"cantidad", "promedio", "minimo", "maximo"}

_SAMPLE_PATH = os.environ.get(SAMPLE_ENV_VAR)

pytestmark = pytest.mark.skipif(
    not _SAMPLE_PATH,
    reason=(
        f"Variable de entorno {SAMPLE_ENV_VAR} no definida: no hay muestra "
        "de T1 que cargar."
    ),
)


def _load_sample_function():
    """Importa la muestra indicada por SEAT_SAMPLE_PATH y devuelve la funcion."""
    path = Path(_SAMPLE_PATH)
    if not path.is_file():
        pytest.fail(f"La muestra indicada no existe: {path}", pytrace=False)
    spec = importlib.util.spec_from_file_location("seat_t1_sample", path)
    if spec is None or spec.loader is None:
        pytest.fail(f"No se pudo preparar la importacion de: {path}", pytrace=False)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    function = getattr(module, SAMPLE_FUNCTION_NAME, None)
    if not callable(function):
        pytest.fail(
            f"La muestra no define la funcion {SAMPLE_FUNCTION_NAME}()",
            pytrace=False,
        )
    return function


@pytest.fixture(scope="module")
def analizar_mediciones():
    return _load_sample_function()


def _assert_structure(result):
    """Verifica la estructura exacta exigida por prompt.md."""
    assert isinstance(result, dict)
    assert set(result.keys()) == TOP_LEVEL_KEYS
    assert isinstance(result["por_sensor"], dict)
    for sensor, stats in result["por_sensor"].items():
        assert isinstance(sensor, str)
        assert isinstance(stats, dict)
        assert set(stats.keys()) == SENSOR_KEYS


# ---------------------------------------------------------------------------
# T1-C01 - Funcionamiento normal (un sensor)
# ---------------------------------------------------------------------------
def test_t1_c01_funcionamiento_normal(analizar_mediciones):
    mediciones = [
        {"sensor": "S1", "valor": 10},
        {"sensor": "S1", "valor": 20},
        {"sensor": "S1", "valor": 32},
    ]

    resultado = analizar_mediciones(mediciones)

    _assert_structure(resultado)
    assert resultado["validas"] == 3
    assert resultado["invalidas"] == 0
    assert resultado["promedio_general"] == pytest.approx(62 / 3)
    assert resultado["minimo_general"] == 10
    assert resultado["maximo_general"] == 32

    assert set(resultado["por_sensor"].keys()) == {"S1"}
    sensor = resultado["por_sensor"]["S1"]
    assert sensor["cantidad"] == 3
    assert sensor["promedio"] == pytest.approx(62 / 3)
    assert sensor["minimo"] == 10
    assert sensor["maximo"] == 32


# ---------------------------------------------------------------------------
# T1-C02 - Agrupacion de varios sensores
# ---------------------------------------------------------------------------
def test_t1_c02_agrupacion_varios_sensores(analizar_mediciones):
    mediciones = [
        {"sensor": "S1", "valor": 10},
        {"sensor": "S1", "valor": 20},
        {"sensor": "S1", "valor": 32},
        {"sensor": "S2", "valor": 40},
        {"sensor": "S2", "valor": 50},
        {"sensor": "S2", "valor": 62},
    ]

    resultado = analizar_mediciones(mediciones)

    _assert_structure(resultado)
    assert resultado["validas"] == 6
    assert resultado["invalidas"] == 0
    assert resultado["promedio_general"] == pytest.approx(214 / 6)
    assert resultado["minimo_general"] == 10
    assert resultado["maximo_general"] == 62

    assert set(resultado["por_sensor"].keys()) == {"S1", "S2"}

    s1 = resultado["por_sensor"]["S1"]
    assert s1["cantidad"] == 3
    assert s1["promedio"] == pytest.approx(62 / 3)
    assert s1["minimo"] == 10
    assert s1["maximo"] == 32

    s2 = resultado["por_sensor"]["S2"]
    assert s2["cantidad"] == 3
    assert s2["promedio"] == pytest.approx(152 / 3)
    assert s2["minimo"] == 40
    assert s2["maximo"] == 62


# ---------------------------------------------------------------------------
# T1-C03 - Lista vacia
# ---------------------------------------------------------------------------
def test_t1_c03_lista_vacia(analizar_mediciones):
    resultado = analizar_mediciones([])

    assert resultado == {
        "validas": 0,
        "invalidas": 0,
        "promedio_general": None,
        "minimo_general": None,
        "maximo_general": None,
        "por_sensor": {},
    }


# ---------------------------------------------------------------------------
# T1-C04 - Limites validos (0 y 100)
# ---------------------------------------------------------------------------
def test_t1_c04_limites_validos(analizar_mediciones):
    mediciones = [
        {"sensor": "S1", "valor": 0},
        {"sensor": "S1", "valor": 100},
    ]

    resultado = analizar_mediciones(mediciones)

    _assert_structure(resultado)
    assert resultado["validas"] == 2
    assert resultado["invalidas"] == 0
    assert resultado["promedio_general"] == pytest.approx(50.0)
    assert resultado["minimo_general"] == 0
    assert resultado["maximo_general"] == 100

    sensor = resultado["por_sensor"]["S1"]
    assert sensor["cantidad"] == 2
    assert sensor["promedio"] == pytest.approx(50.0)
    assert sensor["minimo"] == 0
    assert sensor["maximo"] == 100


# ---------------------------------------------------------------------------
# T1-C05 - Normalizacion del nombre de sensor
# ---------------------------------------------------------------------------
def test_t1_c05_normalizacion_sensor(analizar_mediciones):
    mediciones = [
        {"sensor": "S1", "valor": 10},
        {"sensor": " S1 ", "valor": 20},
        {"sensor": "S1  ", "valor": 32},
    ]

    resultado = analizar_mediciones(mediciones)

    _assert_structure(resultado)
    assert resultado["validas"] == 3
    assert resultado["invalidas"] == 0
    assert set(resultado["por_sensor"].keys()) == {"S1"}
    assert resultado["promedio_general"] == pytest.approx(62 / 3)

    sensor = resultado["por_sensor"]["S1"]
    assert sensor["cantidad"] == 3
    assert sensor["promedio"] == pytest.approx(62 / 3)
    assert sensor["minimo"] == 10
    assert sensor["maximo"] == 32


# ---------------------------------------------------------------------------
# T1-C06 - Campos faltantes y registros invalidos
# ---------------------------------------------------------------------------
def test_t1_c06_campos_faltantes(analizar_mediciones):
    mediciones = [
        {},
        {"sensor": "S1"},
        {"valor": 10},
        {"sensor": "S1", "valor": 50},
    ]

    resultado = analizar_mediciones(mediciones)

    _assert_structure(resultado)
    assert resultado["validas"] == 1
    assert resultado["invalidas"] == 3
    assert resultado["promedio_general"] == pytest.approx(50.0)
    assert resultado["minimo_general"] == 50
    assert resultado["maximo_general"] == 50

    assert set(resultado["por_sensor"].keys()) == {"S1"}
    assert resultado["por_sensor"]["S1"]["cantidad"] == 1


# ---------------------------------------------------------------------------
# T1-C07 - Valores numericos fuera de rango
# ---------------------------------------------------------------------------
def test_t1_c07_fuera_de_rango(analizar_mediciones):
    mediciones = [
        {"sensor": "S1", "valor": -1},
        {"sensor": "S1", "valor": 100.1},
    ]

    resultado = analizar_mediciones(mediciones)

    _assert_structure(resultado)
    assert resultado["validas"] == 0
    assert resultado["invalidas"] == 2
    assert resultado["promedio_general"] is None
    assert resultado["minimo_general"] is None
    assert resultado["maximo_general"] is None
    assert resultado["por_sensor"] == {}


# ---------------------------------------------------------------------------
# T1-C08 - Tipos invalidos
# ---------------------------------------------------------------------------
def test_t1_c08_tipos_invalidos(analizar_mediciones):
    mediciones = [
        {"sensor": "S1", "valor": True},
        {"sensor": "S1", "valor": False},
        {"sensor": "S1", "valor": "50"},
        {"sensor": "S1", "valor": None},
        {"sensor": 123, "valor": 50},
        {"sensor": "   ", "valor": 50},
        "registro",
    ]

    resultado = analizar_mediciones(mediciones)

    _assert_structure(resultado)
    assert resultado["validas"] == 0
    assert resultado["invalidas"] == 7
    assert resultado["promedio_general"] is None
    assert resultado["minimo_general"] is None
    assert resultado["maximo_general"] is None
    assert resultado["por_sensor"] == {}


# ---------------------------------------------------------------------------
# T1-C09 - Inmutabilidad
# ---------------------------------------------------------------------------
def test_t1_c09_inmutabilidad(analizar_mediciones):
    mediciones = [
        {"sensor": "S1", "valor": 10},
        {"sensor": " S1 ", "valor": 20},
        {"sensor": "S2", "valor": 30},
    ]
    copia = copy.deepcopy(mediciones)

    analizar_mediciones(mediciones)

    assert mediciones == copia


# ---------------------------------------------------------------------------
# T1-C10 - Tipo de entrada principal incorrecto
# ---------------------------------------------------------------------------
def test_t1_c10_tipo_principal_incorrecto(analizar_mediciones):
    for entrada in ("no es lista", {"sensor": "S1"}, 42, None, ("S1", 10)):
        with pytest.raises(TypeError):
            analizar_mediciones(entrada)
