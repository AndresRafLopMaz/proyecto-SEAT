"""FASE GLOBAL-B: analisis estadistico formal de las 90 observaciones.

Fuente unica: results/consolidated/global_results.csv (congelado, READ-ONLY).
Verifica su SHA-256 antes y despues; nunca lo modifica.

Produce:
    results/statistics/descriptive_statistics.csv
    results/statistics/kruskal_wallis.csv
    results/statistics/posthoc_dunn_holm.csv
    results/statistics/statistical_manifest.json
    results/reports/global_statistical_analysis.md

Metodologia:
- contraste principal POR TAREA (no se combinan T1+T2+T3 en un unico omnibus);
- metrica principal: ICC; analisis secundarios: R, F, C, M, S;
- Kruskal-Wallis (alpha=0.05), nan_policy="raise";
- NO_VARIATION cuando todos los valores son identicos;
- post-hoc Dunn (con correccion por empates) solo tras omnibus significativo;
- correccion de Holm-Bonferroni;
- tamanos de efecto: epsilon squared (omnibus) y Cliff's delta (pares).

Uso:
    .venv\\Scripts\\python.exe scripts\\analyze_global_stats.py
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import statistics
from collections import Counter
from pathlib import Path

import scipy
from scipy import stats as scipy_stats
from scipy.stats import norm, rankdata

PROJECT_ROOT = Path(__file__).resolve().parents[1]
GLOBAL_CSV = PROJECT_ROOT / "results" / "consolidated" / "global_results.csv"
STATS_DIR = PROJECT_ROOT / "results" / "statistics"
REPORTS_DIR = PROJECT_ROOT / "results" / "reports"

DESCRIPTIVE_CSV = STATS_DIR / "descriptive_statistics.csv"
KRUSKAL_CSV = STATS_DIR / "kruskal_wallis.csv"
POSTHOC_CSV = STATS_DIR / "posthoc_dunn_holm.csv"
MANIFEST_JSON = STATS_DIR / "statistical_manifest.json"
REPORT_MD = REPORTS_DIR / "global_statistical_analysis.md"

EXPECTED_GLOBAL_SHA256 = (
    "ce2a48f8b513f60f908700f3ace8f593e4e7940562b0d6c0078c5778946f8671"
)

TASKS = ("T1", "T2", "T3")
MODELS = ("chatgpt", "deepseek", "opencode")
METRICS = ("R", "F", "C", "M", "S", "ICC")
PRIMARY_METRIC = "ICC"
ALPHA = 0.05
QUANTILE_METHOD = "statistics.quantiles(n=4, method='inclusive')"


# ---------------------------------------------------------------------------
# Utilidades estadisticas puras (testeables)
# ---------------------------------------------------------------------------
def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def descriptive(values):
    """Estadistica descriptiva. Cuartiles con metodos='inclusive'."""
    clean = [float(v) for v in values]
    n = len(clean)
    if n == 0:
        return None
    ordered = sorted(clean)
    if n >= 2:
        q1, _q2, q3 = statistics.quantiles(ordered, n=4, method="inclusive")
    else:
        q1 = q3 = ordered[0]
    return {
        "n": n,
        "mean": statistics.fmean(clean),
        "median": statistics.median(clean),
        "std": statistics.stdev(clean) if n > 1 else 0.0,
        "min": min(clean),
        "q1": q1,
        "q3": q3,
        "iqr": q3 - q1,
        "max": max(clean),
    }


def epsilon_squared(H, k, N):
    """Tamano de efecto omnibus epsilon^2 = (H - k + 1) / (N - k)."""
    return (H - k + 1) / (N - k)


def cliffs_delta(x, y):
    """Cliff's delta entre x (primer grupo) e y (segundo grupo)."""
    greater = 0
    lesser = 0
    for value_x in x:
        for value_y in y:
            if value_x > value_y:
                greater += 1
            elif value_x < value_y:
                lesser += 1
    total = len(x) * len(y)
    if total == 0:
        return 0.0
    return (greater - lesser) / total


def holm_correction(p_values):
    """Holm-Bonferroni. Devuelve p_holm en el mismo orden que la entrada."""
    m = len(p_values)
    order = sorted(range(m), key=lambda i: p_values[i])
    adjusted = [0.0] * m
    running = 0.0
    for position, index in enumerate(order):
        value = (m - position) * p_values[index]
        running = max(running, value)
        adjusted[index] = min(running, 1.0)
    return adjusted


def _mean_ranks(groups, labels):
    elements = []
    for label in labels:
        for value in groups[label]:
            elements.append((value, label))
    values = [value for value, _ in elements]
    ranks = rankdata(values)
    accum = {label: [] for label in labels}
    for (_value, label), rank in zip(elements, ranks):
        accum[label].append(float(rank))
    return {label: sum(ranks_) / len(ranks_) for label, ranks_ in accum.items()}


def dunn_pairwise(groups, labels=MODELS, pairs=((0, 1), (0, 2), (1, 2))):
    """Dunn por pares con correccion por empates.

    z = (mean_rank_i - mean_rank_j) / sqrt(VC * (1/n_i + 1/n_j))
    VC = N(N+1)/12 - sum(t^3 - t) / (12 (N-1))
    p bilateral = 2 * norm.sf(|z|)
    """
    all_values = [value for label in labels for value in groups[label]]
    N = len(all_values)
    if N < 2:
        raise ValueError("Dunn requiere al menos 2 observaciones")
    mean_ranks = _mean_ranks(groups, labels)
    counts = Counter(all_values)
    tie_sum = sum(t ** 3 - t for t in counts.values() if t > 1)
    variance_component = N * (N + 1) / 12 - tie_sum / (12 * (N - 1))

    results = []
    for i, j in pairs:
        label_i, label_j = labels[i], labels[j]
        n_i, n_j = len(groups[label_i]), len(groups[label_j])
        denominator = math.sqrt(variance_component * (1 / n_i + 1 / n_j))
        z = (mean_ranks[label_i] - mean_ranks[label_j]) / denominator
        p_raw = 2 * norm.sf(abs(z))
        results.append(
            {
                "group_1": label_i,
                "group_2": label_j,
                "z": z,
                "p_raw": p_raw,
            }
        )
    return results


def kruskal_analysis(groups, labels=MODELS):
    """Kruskal-Wallis con deteccion explicita de NO_VARIATION."""
    combined = [value for label in labels for value in groups[label]]
    if len(set(combined)) <= 1:
        return {
            "test_applicable": False,
            "reason": "all_values_identical",
            "H": None,
            "p_value": None,
        }
    result = scipy_stats.kruskal(*(groups[label] for label in labels), nan_policy="raise")
    return {
        "test_applicable": True,
        "reason": "",
        "H": float(result.statistic),
        "p_value": float(result.pvalue),
    }


# ---------------------------------------------------------------------------
# Lectura de la base congelada
# ---------------------------------------------------------------------------
def read_global(path=GLOBAL_CSV):
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    records = []
    for row in rows:
        record = {
            "task": row["task"].strip(),
            "model": row["model"].strip(),
            "repetition": int(str(row["repetition"]).strip()),
            "sample_id": row["sample_id"].strip(),
        }
        for metric in METRICS:
            record[metric] = float(row[metric])
        records.append(record)
    return records


def groups_for(records, task, metric):
    return {
        model: [r[metric] for r in records if r["task"] == task and r["model"] == model]
        for model in MODELS
    }


# ---------------------------------------------------------------------------
# Generacion de artefactos
# ---------------------------------------------------------------------------
def build_descriptive_rows(records):
    rows = []
    for task in TASKS:
        for model in MODELS:
            for metric in METRICS:
                values = [r[metric] for r in records if r["task"] == task and r["model"] == model]
                summary = descriptive(values)
                rows.append({"scope": "task", "task": task, "model": model, "metric": metric, **summary})
    for model in MODELS:
        for metric in METRICS:
            values = [r[metric] for r in records if r["model"] == model]
            summary = descriptive(values)
            rows.append({"scope": "global_descriptive", "task": "ALL", "model": model, "metric": metric, **summary})
    return rows


DESCRIPTIVE_COLUMNS = ["scope", "task", "model", "metric", "n", "mean", "median", "std", "min", "q1", "q3", "iqr", "max"]


def write_descriptive(rows):
    STATS_DIR.mkdir(parents=True, exist_ok=True)
    with DESCRIPTIVE_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=DESCRIPTIVE_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def build_kruskal(records):
    results = []
    for task in TASKS:
        for metric in METRICS:
            groups = groups_for(records, task, metric)
            analysis = kruskal_analysis(groups)
            row = {
                "task": task,
                "metric": metric,
                "test_applicable": analysis["test_applicable"],
                "reason": analysis["reason"],
                "n_chatgpt": len(groups["chatgpt"]),
                "n_deepseek": len(groups["deepseek"]),
                "n_opencode": len(groups["opencode"]),
                "H": "" if analysis["H"] is None else analysis["H"],
                "p_value": "" if analysis["p_value"] is None else analysis["p_value"],
                "alpha": ALPHA,
                "significant": (
                    "" if analysis["p_value"] is None else (analysis["p_value"] < ALPHA)
                ),
                "epsilon_squared": (
                    "" if analysis["H"] is None
                    else epsilon_squared(analysis["H"], len(MODELS), len(MODELS) * 10)
                ),
            }
            results.append(row)
    return results


KRUSKAL_COLUMNS = [
    "task", "metric", "test_applicable", "reason",
    "n_chatgpt", "n_deepseek", "n_opencode",
    "H", "p_value", "alpha", "significant", "epsilon_squared",
]


def write_kruskal(rows):
    with KRUSKAL_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=KRUSKAL_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def build_posthoc(records, kruskal_rows):
    rows = []
    for krow in kruskal_rows:
        if not krow["significant"]:
            continue
        task, metric = krow["task"], krow["metric"]
        groups = groups_for(records, task, metric)
        pairwise = dunn_pairwise(groups)
        p_holms = holm_correction([p["p_raw"] for p in pairwise])
        for pair, p_holm in zip(pairwise, p_holms):
            rows.append(
                {
                    "task": task,
                    "metric": metric,
                    "group_1": pair["group_1"],
                    "group_2": pair["group_2"],
                    "z": pair["z"],
                    "p_raw": pair["p_raw"],
                    "p_holm": p_holm,
                    "significant_holm": p_holm < ALPHA,
                    "cliffs_delta": cliffs_delta(
                        groups[pair["group_1"]], groups[pair["group_2"]]
                    ),
                }
            )
    return rows


POSTHOC_COLUMNS = [
    "task", "metric", "group_1", "group_2", "z", "p_raw", "p_holm",
    "significant_holm", "cliffs_delta",
]


def write_posthoc(rows):
    with POSTHOC_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=POSTHOC_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def build_manifest(global_hash_before, global_hash_after, hashes):
    return {
        "phase": "GLOBAL-B (analisis estadistico formal)",
        "global_results_sha256": global_hash_before,
        "global_results_sha256_after": global_hash_after,
        "global_results_unchanged": global_hash_before == global_hash_after,
        "python_version": platform.python_version(),
        "scipy_version": scipy.__version__,
        "alpha": ALPHA,
        "primary_metric": PRIMARY_METRIC,
        "omnibus_test": "Kruskal-Wallis",
        "posthoc_test": "Dunn (con correccion por empates)",
        "multiple_comparison_correction": "Holm-Bonferroni",
        "omnibus_effect_size": "epsilon_squared",
        "pairwise_effect_size": "cliffs_delta",
        "quantile_method": QUANTILE_METHOD,
        "total_observations": 90,
        "task_group_sizes": {task: {model: 10 for model in MODELS} for task in TASKS},
        "generated_files": {
            "descriptive_statistics.csv": hashes.get("descriptive_statistics.csv"),
            "kruskal_wallis.csv": hashes.get("kruskal_wallis.csv"),
            "posthoc_dunn_holm.csv": hashes.get("posthoc_dunn_holm.csv"),
        },
    }


def _fmt(value, digits=4):
    if value is None or value == "":
        return "N/A"
    if isinstance(value, bool):
        return str(value)
    return f"{float(value):.{digits}f}"


def build_report(records, descriptive_rows, kruskal_rows, posthoc_rows, global_hash):
    def desc(task, model, metric):
        for row in descriptive_rows:
            if row["scope"] == "task" and row["task"] == task and row["model"] == model and row["metric"] == metric:
                return row
        return None

    def krow(task, metric):
        for row in kruskal_rows:
            if row["task"] == task and row["metric"] == metric:
                return row
        return None

    lines = []
    lines.append("# Análisis estadístico global")
    lines.append("")
    lines.append("## 1. Objetivo")
    lines.append("")
    lines.append(
        "Comparar las categorías experimentales (chatgpt, deepseek, opencode) sin mezclar "
        "las tareas en el contraste principal. El contraste inferencial se realiza por "
        "separado para T1, T2 y T3, porque las tareas tienen características diferentes."
    )
    lines.append("")

    lines.append("## 2. Base analizada")
    lines.append("")
    lines.append("- 90 observaciones (3 tareas × 3 modelos × 10 repeticiones).")
    lines.append("- 3 tareas: T1, T2, T3.")
    lines.append("- 3 modelos: chatgpt, deepseek, opencode.")
    lines.append("- 10 observaciones por tarea/modelo.")
    lines.append(f"- Fuente única: `results/consolidated/global_results.csv`.")
    lines.append(f"- SHA-256: `{global_hash}`")
    lines.append("")

    lines.append("## 3. Método estadístico")
    lines.append("")
    lines.append("- Estadística descriptiva (n, media, mediana, desviación estándar, mín, máx, Q1, Q3, IQR).")
    lines.append(f"- Cuantiles: `{QUANTILE_METHOD}` (mismo método en todos los grupos).")
    lines.append(f"- Kruskal-Wallis H con alpha = {ALPHA} y nan_policy='raise'.")
    lines.append("- Si el omnibus es significativo: post-hoc de Dunn por pares con corrección por empates.")
    lines.append("- Corrección de comparaciones múltiples: Holm-Bonferroni (decisión con p_holm).")
    lines.append("- Tamaños de efecto: epsilon squared (omnibus) y Cliff's delta (pares).")
    lines.append("- NO_VARIATION: si todos los valores son idénticos, el test no se aplica y no se inventa estadístico.")
    lines.append("- n = 10 por grupo: limita la potencia estadística; los resultados no se generalizan más allá de las tareas, versiones y generaciones evaluadas.")
    lines.append("")

    lines.append("## 4. Análisis primario del ICC")
    lines.append("")
    for task in TASKS:
        lines.append(f"### 4.{TASKS.index(task) + 1} {task}")
        lines.append("")
        lines.append("| Modelo | n | media | mediana | std | mín | Q1 | Q3 | IQR | máx |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|")
        for model in MODELS:
            d = desc(task, model, "ICC")
            lines.append(
                f"| {model} | {d['n']} | {_fmt(d['mean'])} | {_fmt(d['median'])} | {_fmt(d['std'])} | "
                f"{_fmt(d['min'])} | {_fmt(d['q1'])} | {_fmt(d['q3'])} | {_fmt(d['iqr'])} | {_fmt(d['max'])} |"
            )
        k = krow(task, "ICC")
        lines.append("")
        if not k["test_applicable"]:
            lines.append(f"- NO_VARIATION ({k['reason']}): no existe variación observada en el ICC dentro de {task}.")
        else:
            lines.append(f"- H = {_fmt(k['H'])}; p = {_fmt(k['p_value'], 6)}; epsilon squared = {_fmt(k['epsilon_squared'])}.")
            if k["significant"]:
                lines.append("- Decisión: p < 0.05 → se rechaza H0; hay evidencia de que al menos una distribución del ICC difiere entre modelos.")
            else:
                lines.append("- Decisión: p ≥ 0.05 → no se rechaza H0.")
        lines.append("")

    lines.append("## 5. Análisis secundario por dimensiones")
    lines.append("")
    for index, metric in enumerate(("R", "F", "C", "M", "S"), start=1):
        lines.append(f"### 5.{index} {metric}")
        lines.append("")
        lines.append("| Tarea | test aplicable | H | p | epsilon² | decisión |")
        lines.append("|---|---|---|---|---|---|")
        for task in TASKS:
            k = krow(task, metric)
            if not k["test_applicable"]:
                lines.append(f"| {task} | NO_VARIATION | N/A | N/A | N/A | {k['reason']} |")
            else:
                decision = "se rechaza H0" if k["significant"] else "no se rechaza H0"
                lines.append(
                    f"| {task} | sí | {_fmt(k['H'])} | {_fmt(k['p_value'], 6)} | "
                    f"{_fmt(k['epsilon_squared'])} | {decision} |"
                )
        lines.append("")

    lines.append("## 6. Comparaciones post-hoc")
    lines.append("")
    if not posthoc_rows:
        lines.append("- No hubo omnibus significativos; no se ejecutaron comparaciones post-hoc.")
    else:
        lines.append("| Tarea | Métrica | Grupo 1 | Grupo 2 | z | p crudo | p Holm | significativo (Holm) | Cliff's delta |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for row in posthoc_rows:
            lines.append(
                f"| {row['task']} | {row['metric']} | {row['group_1']} | {row['group_2']} | "
                f"{_fmt(row['z'])} | {_fmt(row['p_raw'], 6)} | {_fmt(row['p_holm'], 6)} | "
                f"{row['significant_holm']} | {_fmt(row['cliffs_delta'])} |"
            )
    lines.append("")

    lines.append("## 7. Variabilidad")
    lines.append("")
    lines.append("Descripción de la estabilidad del ICC por tarea y modelo (std, IQR, mín-máx).")
    lines.append("")
    lines.append("| Tarea | Modelo | std | IQR | mín | máx |")
    lines.append("|---|---|---|---|---|---|")
    for task in TASKS:
        for model in MODELS:
            d = desc(task, model, "ICC")
            lines.append(f"| {task} | {model} | {_fmt(d['std'])} | {_fmt(d['iqr'])} | {_fmt(d['min'])} | {_fmt(d['max'])} |")
    lines.append("")
    lines.append("Menor desviación indica mayor estabilidad observada, no superioridad.")
    lines.append("")

    lines.append("## 8. Resumen descriptivo global")
    lines.append("")
    lines.append("Resumen descriptivo de las 30 observaciones por modelo (T1+T2+T3 combinadas). Es únicamente descriptivo y no constituye un contraste inferencial agrupado.")
    lines.append("")
    lines.append("| Modelo | Métrica | n | media | mediana | std | mín | Q1 | Q3 | IQR | máx |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for model in MODELS:
        for metric in METRICS:
            row = next(r for r in descriptive_rows if r["scope"] == "global_descriptive" and r["model"] == model and r["metric"] == metric)
            lines.append(
                f"| {model} | {metric} | {row['n']} | {_fmt(row['mean'])} | {_fmt(row['median'])} | "
                f"{_fmt(row['std'])} | {_fmt(row['min'])} | {_fmt(row['q1'])} | {_fmt(row['q3'])} | "
                f"{_fmt(row['iqr'])} | {_fmt(row['max'])} |"
            )
    lines.append("")

    lines.append("## 9. Hallazgos estadísticos principales")
    lines.append("")
    applicable = [k for k in kruskal_rows if k["test_applicable"]]
    no_variation = [k for k in kruskal_rows if not k["test_applicable"]]
    significant = [k for k in applicable if k["significant"]]
    lines.append(f"- Pruebas omnibus aplicables: {len(applicable)}; no aplicables (NO_VARIATION): {len(no_variation)}.")
    lines.append(f"- Omnibus significativos (p < {ALPHA}): {len(significant)}.")
    for k in significant:
        lines.append(f"  - {k['task']} / {k['metric']}: H={_fmt(k['H'])}, p={_fmt(k['p_value'], 6)}, epsilon²={_fmt(k['epsilon_squared'])}.")
    sig_pairs = [r for r in posthoc_rows if r["significant_holm"]]
    lines.append(f"- Pares post-hoc significativos tras Holm: {len(sig_pairs)}.")
    for r in sig_pairs:
        lines.append(
            f"  - {r['task']}/{r['metric']} {r['group_1']} vs {r['group_2']}: "
            f"p_holm={_fmt(r['p_holm'], 6)}, Cliff's delta={_fmt(r['cliffs_delta'])}."
        )
    lines.append("- Los resultados no significativos se reportan como ausencia de evidencia bajo esta prueba y esta muestra, no como equivalencia.")
    lines.append("")

    lines.append("## 10. Estado para contraste final de hipótesis")
    lines.append("")
    lines.append("Los resultados anteriores (ICC por tarea, dimensiones secundarias, post-hoc y tamaños de efecto) se llevarán a GLOBAL-C para el contraste final de hipótesis. Esta fase no redacta las conclusiones finales del proyecto.")
    lines.append("")
    return "\n".join(lines)


def main():
    if not GLOBAL_CSV.is_file():
        print(f"ERROR: no existe {GLOBAL_CSV}")
        return 1
    global_hash_before = sha256_file(GLOBAL_CSV)
    if global_hash_before != EXPECTED_GLOBAL_SHA256:
        print("ERROR: el SHA-256 de global_results.csv no coincide con el esperado. DETENCION.")
        print(f"  esperado: {EXPECTED_GLOBAL_SHA256}")
        print(f"  actual:   {global_hash_before}")
        return 1

    records = read_global()
    if len(records) != 90:
        print(f"ERROR: se esperaban 90 observaciones, se leyeron {len(records)}")
        return 1

    descriptive_rows = build_descriptive_rows(records)
    write_descriptive(descriptive_rows)

    kruskal_rows = build_kruskal(records)
    write_kruskal(kruskal_rows)

    posthoc_rows = build_posthoc(records, kruskal_rows)
    write_posthoc(posthoc_rows)

    report = build_report(records, descriptive_rows, kruskal_rows, posthoc_rows, global_hash_before)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_MD.write_text(report, encoding="utf-8")

    global_hash_after = sha256_file(GLOBAL_CSV)
    hashes = {
        "descriptive_statistics.csv": sha256_file(DESCRIPTIVE_CSV),
        "kruskal_wallis.csv": sha256_file(KRUSKAL_CSV),
        "posthoc_dunn_holm.csv": sha256_file(POSTHOC_CSV),
    }
    manifest = build_manifest(global_hash_before, global_hash_after, hashes)
    MANIFEST_JSON.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Observaciones: {len(records)}")
    print(f"global sha256 before: {global_hash_before}")
    print(f"global sha256 after:  {global_hash_after} (unchanged={global_hash_before == global_hash_after})")
    print(f"descriptive: {DESCRIPTIVE_CSV}")
    print(f"kruskal: {KRUSKAL_CSV}")
    print(f"posthoc: {POSTHOC_CSV}")
    print(f"manifest: {MANIFEST_JSON}")
    print(f"report: {REPORT_MD}")
    if global_hash_before != global_hash_after:
        print("ERROR: global_results.csv cambio. Fase fallida.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
