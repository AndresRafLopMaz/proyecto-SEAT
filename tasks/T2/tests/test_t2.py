"""Instrumento de evaluacion de T2 (fase T2-A).

Contiene los 10 casos funcionales derivados exclusivamente de
tasks/T2/prompt.md. No incluye ni depende de ninguna muestra experimental.

Carga de la muestra
-------------------
La ruta del archivo Python a evaluar se recibe mediante la variable de
entorno SEAT_SAMPLE_PATH. El modulo se importa dinamicamente y debe exponer la
funcion `procesar_inventario`. Si la variable no esta definida, los casos se
omiten (skip) para no romper la ejecucion del resto del instrumento.

Ejemplo de uso:
    $env:SEAT_SAMPLE_PATH = "ruta\\a\\la\\muestra.py"
    .venv\\Scripts\\python.exe -m pytest tasks\\T2\\tests\\test_t2.py -q

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
SAMPLE_FUNCTION_NAME = "procesar_inventario"

TOP_LEVEL_KEYS = {"inventario", "aplicadas", "rechazadas"}

_SAMPLE_PATH = os.environ.get(SAMPLE_ENV_VAR)

pytestmark = pytest.mark.skipif(
    not _SAMPLE_PATH,
    reason=(
        f"Variable de entorno {SAMPLE_ENV_VAR} no definida: no hay muestra "
        "de T2 que cargar."
    ),
)


def _load_sample_function():
    """Importa la muestra indicada por SEAT_SAMPLE_PATH y devuelve la funcion."""
    path = Path(_SAMPLE_PATH)
    if not path.is_file():
        pytest.fail(f"La muestra indicada no existe: {path}", pytrace=False)
    try:
        spec = importlib.util.spec_from_file_location("seat_t2_sample", path)
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
def procesar_inventario():
    return _load_sample_function()


def _assert_structure(result):
    """Verifica la estructura exacta exigida por prompt.md."""
    assert isinstance(result, dict)
    assert set(result.keys()) == TOP_LEVEL_KEYS
    assert isinstance(result["inventario"], dict)
    assert isinstance(result["aplicadas"], int)
    assert isinstance(result["rechazadas"], int)


# ---------------------------------------------------------------------------
# T2-C01 - Agregar a producto existente
# ---------------------------------------------------------------------------
def test_t2_c01_agregar_existente(procesar_inventario):
    inventario = {"A": 5}
    operaciones = [{"accion": "agregar", "codigo": "A", "cantidad": 3}]

    resultado = procesar_inventario(inventario, operaciones)

    _assert_structure(resultado)
    assert resultado["inventario"] == {"A": 8}
    assert resultado["aplicadas"] == 1
    assert resultado["rechazadas"] == 0


# ---------------------------------------------------------------------------
# T2-C02 - Agregar producto nuevo
# ---------------------------------------------------------------------------
def test_t2_c02_agregar_nuevo(procesar_inventario):
    inventario = {}
    operaciones = [{"accion": "agregar", "codigo": "B", "cantidad": 7}]

    resultado = procesar_inventario(inventario, operaciones)

    _assert_structure(resultado)
    assert resultado["inventario"] == {"B": 7}
    assert resultado["aplicadas"] == 1
    assert resultado["rechazadas"] == 0


# ---------------------------------------------------------------------------
# T2-C03 - Retiro parcial
# ---------------------------------------------------------------------------
def test_t2_c03_retiro_parcial(procesar_inventario):
    inventario = {"A": 10}
    operaciones = [{"accion": "retirar", "codigo": "A", "cantidad": 4}]

    resultado = procesar_inventario(inventario, operaciones)

    _assert_structure(resultado)
    assert resultado["inventario"] == {"A": 6}
    assert resultado["aplicadas"] == 1
    assert resultado["rechazadas"] == 0


# ---------------------------------------------------------------------------
# T2-C04 - Retiro total (permanece con 0)
# ---------------------------------------------------------------------------
def test_t2_c04_retiro_total(procesar_inventario):
    inventario = {"A": 10}
    operaciones = [{"accion": "retirar", "codigo": "A", "cantidad": 10}]

    resultado = procesar_inventario(inventario, operaciones)

    _assert_structure(resultado)
    assert resultado["inventario"] == {"A": 0}
    assert resultado["aplicadas"] == 1
    assert resultado["rechazadas"] == 0


# ---------------------------------------------------------------------------
# T2-C05 - Retiro rechazado por stock insuficiente
# ---------------------------------------------------------------------------
def test_t2_c05_retiro_rechazado(procesar_inventario):
    inventario = {"A": 3}
    operaciones = [{"accion": "retirar", "codigo": "A", "cantidad": 5}]

    resultado = procesar_inventario(inventario, operaciones)

    _assert_structure(resultado)
    assert resultado["inventario"] == {"A": 3}
    assert resultado["aplicadas"] == 0
    assert resultado["rechazadas"] == 1


# ---------------------------------------------------------------------------
# T2-C06 - Eliminacion (valida e invalida)
# ---------------------------------------------------------------------------
def test_t2_c06_eliminacion(procesar_inventario):
    resultado_valido = procesar_inventario(
        {"A": 5, "B": 2},
        [{"accion": "eliminar", "codigo": "A"}],
    )
    _assert_structure(resultado_valido)
    assert resultado_valido["inventario"] == {"B": 2}
    assert resultado_valido["aplicadas"] == 1
    assert resultado_valido["rechazadas"] == 0

    resultado_invalido = procesar_inventario(
        {"A": 5},
        [{"accion": "eliminar", "codigo": "Z"}],
    )
    _assert_structure(resultado_invalido)
    assert resultado_invalido["inventario"] == {"A": 5}
    assert resultado_invalido["aplicadas"] == 0
    assert resultado_invalido["rechazadas"] == 1


# ---------------------------------------------------------------------------
# T2-C07 - Transferencia valida
# ---------------------------------------------------------------------------
def test_t2_c07_transferencia_valida(procesar_inventario):
    inventario = {"A": 10, "B": 2}
    operaciones = [
        {"accion": "transferir", "origen": "A", "destino": "B", "cantidad": 4}
    ]

    resultado = procesar_inventario(inventario, operaciones)

    _assert_structure(resultado)
    assert resultado["inventario"] == {"A": 6, "B": 6}
    assert resultado["aplicadas"] == 1
    assert resultado["rechazadas"] == 0


# ---------------------------------------------------------------------------
# T2-C08 - Transferencia invalida y atomicidad
# ---------------------------------------------------------------------------
def test_t2_c08_transferencia_invalida_atomica(procesar_inventario):
    subcasos = [
        ({"A": 2, "B": 5}, {"accion": "transferir", "origen": "A", "destino": "B", "cantidad": 3}),
        ({"A": 5}, {"accion": "transferir", "origen": "A", "destino": "A", "cantidad": 1}),
        ({"A": 5}, {"accion": "transferir", "origen": "X", "destino": "A", "cantidad": 1}),
        ({"A": 5}, {"accion": "transferir", "origen": "A", "destino": "Y", "cantidad": 1}),
    ]

    for inventario, operacion in subcasos:
        estado_antes = copy.deepcopy(inventario)
        resultado = procesar_inventario(inventario, [operacion])
        _assert_structure(resultado)
        assert resultado["inventario"] == estado_antes, (
            f"Transferencia invalida con {operacion} produjo cambio parcial"
        )
        assert resultado["aplicadas"] == 0, operacion
        assert resultado["rechazadas"] == 1, operacion
        # El inventario de entrada tampoco debe haberse alterado.
        assert inventario == estado_antes


# ---------------------------------------------------------------------------
# T2-C09 - Operaciones invalidas y continuidad
# ---------------------------------------------------------------------------
def test_t2_c09_invalidas_y_continuidad(procesar_inventario):
    inventario = {"A": 10}
    operaciones = [
        {"accion": "agregar", "codigo": "A", "cantidad": True},
        {"accion": "agregar", "codigo": "A", "cantidad": False},
        {"accion": "agregar", "codigo": "A", "cantidad": 0},
        {"accion": "agregar", "codigo": "A", "cantidad": -3},
        {"accion": "agregar", "codigo": "A", "cantidad": "5"},
        {"accion": "accion_desconocida", "codigo": "A", "cantidad": 1},
        {"accion": "agregar", "codigo": "A"},
        {"accion": "agregar", "codigo": "A", "cantidad": 2},
    ]

    resultado = procesar_inventario(inventario, operaciones)

    _assert_structure(resultado)
    assert resultado["inventario"] == {"A": 12}
    assert resultado["aplicadas"] == 1
    assert resultado["rechazadas"] == 7


# ---------------------------------------------------------------------------
# T2-C10 - Tipos principales e inmutabilidad
# ---------------------------------------------------------------------------
def test_t2_c10_tipos_e_inmutabilidad(procesar_inventario):
    # A) inventario no dict -> TypeError
    for inventario_invalido in ("texto", [], None, 5):
        with pytest.raises(TypeError):
            procesar_inventario(inventario_invalido, [])

    # B) operaciones no list -> TypeError
    for operaciones_invalidas in ("texto", {}, None, 5):
        with pytest.raises(TypeError):
            procesar_inventario({}, operaciones_invalidas)

    # C) inmutable
    inventario = {"A": 5, "B": 3}
    operaciones = [
        {"accion": "agregar", "codigo": "A", "cantidad": 2},
        {"accion": "transferir", "origen": "A", "destino": "B", "cantidad": 1},
        {"accion": "eliminar", "codigo": "B"},
    ]
    inventario_original = copy.deepcopy(inventario)
    operaciones_original = copy.deepcopy(operaciones)

    resultado = procesar_inventario(inventario, operaciones)

    _assert_structure(resultado)
    assert inventario == inventario_original
    assert operaciones == operaciones_original
