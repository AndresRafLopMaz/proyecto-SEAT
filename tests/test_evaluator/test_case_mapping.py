"""Pruebas del instrumento: reconocimiento generico de casos T1/T2."""

import pytest

from evaluator.evaluator import (
    _case_id_from_test_name,
    collect_case_results,
    derive_requirements,
)


@pytest.mark.parametrize(
    "test_name, expected",
    [
        ("test_t1_c01_funcionamiento_normal", "T1-C01"),
        ("test_t1_c10_tipo_principal_incorrecto", "T1-C10"),
        ("test_t2_c01_agregar_existente", "T2-C01"),
        ("test_t2_c08_transferencia_invalida_atomica", "T2-C08"),
        ("test_t2_c10_tipos_e_inmutabilidad", "T2-C10"),
        ("test_t3_c05_algo", "T3-C05"),
    ],
)
def test_reconoce_casos_de_tarea(test_name, expected):
    assert _case_id_from_test_name(test_name) == expected


@pytest.mark.parametrize(
    "test_name",
    [
        "",
        None,
        "test_t1_c1_x",          # un solo digito de caso
        "test_t1_x01_y",         # falta la 'c'
        "test_c01_x",            # falta la tarea
        "foo_t1_c01_bar",        # no empieza con test_
        "test_t1_c01foo",        # sin separador despues del caso
    ],
)
def test_rechaza_nombres_invalidos(test_name):
    assert _case_id_from_test_name(test_name) is None


def test_t1_sigue_mapeando_igual():
    resultado = collect_case_results(
        {
            "cases": {
                "test_t1_c01_funcionamiento_normal": "pass",
                "test_t1_c02_agrupacion_varios_sensores": "fail",
            }
        }
    )
    assert resultado == {"T1-C01": 1, "T1-C02": 0}


def test_t2_mapea_casos_y_estados():
    resultado = collect_case_results(
        {
            "cases": {
                "test_t2_c07_transferencia_valida": "pass",
                "test_t2_c08_transferencia_invalida_atomica": "fail",
                "test_t2_c10_tipos_e_inmutabilidad": "pass",
                "nombre_irrelevante": "pass",
            }
        }
    )
    assert resultado == {"T2-C07": 1, "T2-C08": 0, "T2-C10": 1}


def test_derive_requirements_t2():
    mapping = {
        "T2-R1": ["T2-C10"],
        "T2-R3": ["T2-C07", "T2-C08"],
    }
    assert derive_requirements({"T2-C10": 1, "T2-C07": 1, "T2-C08": 1}, mapping) == {
        "T2-R1": 1,
        "T2-R3": 1,
    }
    assert derive_requirements({"T2-C10": 1, "T2-C07": 1, "T2-C08": 0}, mapping) == {
        "T2-R1": 1,
        "T2-R3": 0,
    }
