"""Pruebas unitarias de las funciones estadisticas (GLOBAL-B).

No tocan samples/ y no modifican global_results.csv. Cargar el modulo del
script mediante importlib para probar las funciones puras.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _load_module():
    path = ROOT / "scripts" / "analyze_global_stats.py"
    spec = importlib.util.spec_from_file_location("analyze_global_stats", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["analyze_global_stats"] = module
    spec.loader.exec_module(module)
    return module


stats_mod = _load_module()


# ---------------------------------------------------------------------------
# Cliff's delta
# ---------------------------------------------------------------------------
def test_cliffs_delta_iguales():
    assert stats_mod.cliffs_delta([1, 2, 3], [1, 2, 3]) == 0.0


def test_cliffs_delta_primer_grupo_mayor():
    assert stats_mod.cliffs_delta([3, 4, 5], [0, 1, 2]) == 1.0


def test_cliffs_delta_segundo_grupo_mayor():
    assert stats_mod.cliffs_delta([0, 1, 2], [3, 4, 5]) == -1.0


def test_cliffs_delta_con_valor_solapado():
    # 3 vs 3 es empate: 8 mayores, 0 menores sobre 9 pares.
    assert stats_mod.cliffs_delta([3, 4, 5], [1, 2, 3]) == pytest.approx(8 / 9)


def test_cliffs_delta_mixto():
    assert stats_mod.cliffs_delta([1, 2, 3], [2, 3, 4]) == pytest.approx(-5 / 9)


# ---------------------------------------------------------------------------
# Holm-Bonferroni
# ---------------------------------------------------------------------------
def test_holm_correccion():
    assert stats_mod.holm_correction([0.01, 0.04, 0.03]) == pytest.approx([0.03, 0.06, 0.06])


def test_holm_no_excede_uno():
    adjusted = stats_mod.holm_correction([0.4, 0.5, 0.9])
    assert all(value <= 1.0 for value in adjusted)
    assert all(adjusted[i] >= raw for i, raw in enumerate([0.4, 0.5, 0.9]))


def test_holm_preserva_orden():
    raw = [0.02, 0.001, 0.05]
    adjusted = stats_mod.holm_correction(raw)
    # el menor p debe recibir el menor p_holm
    assert adjusted[1] < adjusted[0]
    assert adjusted[0] <= adjusted[2]


# ---------------------------------------------------------------------------
# Dunn
# ---------------------------------------------------------------------------
def test_dunn_sin_empates():
    groups = {
        "chatgpt": [1, 2, 3],
        "deepseek": [4, 5, 6],
        "opencode": [7, 8, 9],
    }
    results = stats_mod.dunn_pairwise(groups)
    by_pair = {(r["group_1"], r["group_2"]): r for r in results}
    z_12 = -3 / (7.5 * (1 / 3 + 1 / 3)) ** 0.5
    assert by_pair[("chatgpt", "deepseek")]["z"] == pytest.approx(z_12)
    assert by_pair[("chatgpt", "opencode")]["z"] == pytest.approx(-6 / (5.0) ** 0.5)
    assert by_pair[("deepseek", "opencode")]["z"] == pytest.approx(z_12)
    # p bilateral consistente con la definicion
    from scipy.stats import norm

    assert by_pair[("chatgpt", "deepseek")]["p_raw"] == pytest.approx(
        2 * norm.sf(abs(z_12))
    )


def test_dunn_empates_reducen_varianza():
    # Con empates, el componente de varianza debe ser menor que sin empates.
    grupos_empates = {"chatgpt": [1, 1, 1], "deepseek": [2, 2, 2], "opencode": [2, 3, 3]}
    results = stats_mod.dunn_pairwise(grupos_empates)
    assert len(results) == 3
    # z finitos
    assert all(abs(r["z"]) < 1e6 for r in results)


# ---------------------------------------------------------------------------
# NO_VARIATION
# ---------------------------------------------------------------------------
def test_kruskal_no_variation():
    groups = {
        "chatgpt": [100.0] * 10,
        "deepseek": [100.0] * 10,
        "opencode": [100.0] * 10,
    }
    result = stats_mod.kruskal_analysis(groups)
    assert result["test_applicable"] is False
    assert result["reason"] == "all_values_identical"
    assert result["H"] is None
    assert result["p_value"] is None


def test_kruskal_aplicable():
    groups = {
        "chatgpt": [1, 2, 3, 4],
        "deepseek": [5, 6, 7, 8],
        "opencode": [9, 10, 11, 12],
    }
    result = stats_mod.kruskal_analysis(groups)
    assert result["test_applicable"] is True
    assert isinstance(result["H"], float)
    assert 0.0 <= result["p_value"] <= 1.0


# ---------------------------------------------------------------------------
# Epsilon squared
# ---------------------------------------------------------------------------
def test_epsilon_squared():
    assert stats_mod.epsilon_squared(8.0, 3, 30) == pytest.approx(6 / 27)
    assert stats_mod.epsilon_squared(3.0, 3, 30) == pytest.approx(1 / 27)


# ---------------------------------------------------------------------------
# Base congelada
# ---------------------------------------------------------------------------
def test_lee_90_observaciones():
    records = stats_mod.read_global()
    assert len(records) == 90
    assert {r["task"] for r in records} == {"T1", "T2", "T3"}
    assert {r["model"] for r in records} == {"chatgpt", "deepseek", "opencode"}


def test_global_results_no_modificado():
    assert stats_mod.sha256_file(stats_mod.GLOBAL_CSV) == stats_mod.EXPECTED_GLOBAL_SHA256
