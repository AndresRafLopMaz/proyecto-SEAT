"""FASE T1-B: evaluacion de las 30 muestras de T1 y generacion de resultados.

Ejecuta el instrumento congelado de T1 sobre las 30 muestras (10 por modelo),
produce:
- results/raw/T1/<modelo>/<sample_id>.json   (resultado individual)
- results/consolidated/T1_results.csv        (30 filas)
- results/reports/T1_analysis.md             (analisis descriptivo)

No modifica muestras, prompt.md, requirements.json, test_cases.md ni test_t1.py.
No genera datos ficticios: todo valor proviene de las herramientas.

Uso:
    .venv\\Scripts\\python.exe scripts\\evaluate_t1.py
"""

from __future__ import annotations

import csv
import json
import re
import statistics
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from evaluator.evaluator import evaluate_sample

MODELS = ("chatgpt", "deepseek", "opencode")
TASK = "T1"
TESTS_PATH = PROJECT_ROOT / "tasks" / TASK / "tests" / "test_t1.py"
SAMPLES_ROOT = PROJECT_ROOT / "samples"
RAW_DIR = PROJECT_ROOT / "results" / "raw" / TASK
CSV_PATH = PROJECT_ROOT / "results" / "consolidated" / f"{TASK}_results.csv"
REPORT_PATH = PROJECT_ROOT / "results" / "reports" / f"{TASK}_analysis.md"

CASE_IDS = [f"T1-C{i:02d}" for i in range(1, 11)]
REQUIREMENT_IDS = [f"T1-R{i}" for i in range(1, 6)]
DIMENSIONS = ("R", "F", "C", "M", "S", "ICC")

# Evidencia congelada requisito -> casos (ver tasks/T1/requirements.json).
CASE_REQUIREMENT_MAP = {
    "T1-R1": ["T1-C10"],
    "T1-R2": ["T1-C04", "T1-C05", "T1-C06", "T1-C07", "T1-C08"],
    "T1-R3": ["T1-C06", "T1-C07", "T1-C08"],
    "T1-R4": ["T1-C01", "T1-C02", "T1-C03", "T1-C04", "T1-C05"],
    "T1-R5": ["T1-C09"],
}


# ---------------------------------------------------------------------------
# Descubrimiento y evaluacion
# ---------------------------------------------------------------------------
def discover_samples():
    samples = []
    for model in MODELS:
        directory = SAMPLES_ROOT / model / TASK
        files = sorted(directory.glob("*.py")) if directory.is_dir() else []
        for path in files:
            match = re.search(r"R(\d+)", path.stem)
            samples.append(
                {
                    "model": model,
                    "repetition": int(match.group(1)) if match else None,
                    "path": path,
                    "sample_id": path.stem,
                }
            )
    return samples


def force_protocol_zeros(result):
    """Aplica el protocolo a muestras no evaluables por error de sintaxis/fuente.

    La muestra se conserva; se registra syntax_valid=False e incidencia, y se
    asignan ceros por protocolo (ICC=0). No son mediciones: quedan marcadas.
    """
    result["protocol_forced_zero"] = True
    result["tests_passed"] = 0
    result["requirements_satisfied"] = 0
    result["cases"] = {case_id: 0 for case_id in CASE_IDS}
    result["requirements"] = {req_id: 0 for req_id in REQUIREMENT_IDS}
    for case_id in CASE_IDS:
        result[case_id] = 0
    for req_id in REQUIREMENT_IDS:
        result[req_id] = 0
    result["R"] = 0.0
    result["F"] = 0.0
    result["C"] = 0.0
    result["M"] = 0.0
    result["S"] = 0.0
    result["ICC"] = 0.0
    result["incidents"].append(
        {
            "stage": "protocol",
            "status": "syntax_invalid",
            "message": (
                "Muestra no evaluable por error de sintaxis/fuente de codigo; "
                "por protocolo se asignan ceros e ICC=0 (dimensiones no medidas)."
            ),
        }
    )


def transcode_if_needed(sample, temp_dir):
    """Devuelve (ruta_a_evaluar, incidencia_encoding).

    Si la muestra no es UTF-8 valido, se decodifica como cp1252 (o latin-1) y se
    escribe una representacion temporal UTF-8 fuera de samples/. El archivo
    original nunca se modifica.
    """
    raw = sample["path"].read_bytes()
    try:
        raw.decode("utf-8")
        return sample["path"], None
    except UnicodeDecodeError:
        pass

    decoded = None
    used_encoding = None
    for encoding in ("cp1252", "latin-1"):
        try:
            decoded = raw.decode(encoding)
            used_encoding = encoding
            break
        except UnicodeDecodeError:
            continue

    if decoded is None:
        return sample["path"], {
            "stage": "encoding",
            "status": "undecodable",
            "message": (
                "El archivo no es UTF-8 valido ni decodificable en cp1252/latin-1; "
                f"no se pudo obtener una representacion medible. Original: {sample['path']}"
            ),
        }

    temp_path = Path(temp_dir) / f"{sample['sample_id']}__utf8.py"
    temp_path.write_text(decoded, encoding="utf-8")
    incident = {
        "stage": "encoding",
        "status": "transcoded_for_measurement",
        "message": (
            f"El archivo original no es UTF-8 valido; se decodifico como {used_encoding} "
            "y se midio sobre una representacion temporal UTF-8. "
            "El archivo original NO fue modificado."
        ),
        "original_path": str(sample["path"]),
        "source_encoding": used_encoding,
        "original_modified": False,
    }
    return temp_path, incident


def evaluate_samples(samples):
    results = []
    with tempfile.TemporaryDirectory(prefix="seat_t1_encoding_") as temp_dir:
        for sample in samples:
            eval_path, encoding_incident = transcode_if_needed(sample, temp_dir)
            result = evaluate_sample(
                sample_id=sample["sample_id"],
                system=sample["model"],
                task=TASK,
                repetition=sample["repetition"],
                code_path=eval_path,
                tests_path=TESTS_PATH,
                case_requirement_map=CASE_REQUIREMENT_MAP,
            )
            if encoding_incident is not None:
                result["encoding_incident"] = True
                result["original_path"] = str(sample["path"])
                result["original_modified"] = False
                result["incidents"].append(encoding_incident)
            if not result["syntax_valid"]:
                force_protocol_zeros(result)
            results.append(result)
    return results


def write_individual_results(results):
    written = []
    for result in results:
        model_dir = RAW_DIR / result["model"]
        model_dir.mkdir(parents=True, exist_ok=True)
        path = model_dir / f"{result['sample_id']}.json"
        path.write_text(
            json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        written.append(path)
    return written


# ---------------------------------------------------------------------------
# Consolidado CSV
# ---------------------------------------------------------------------------
CSV_COLUMNS = (
    ["sample_id", "model", "repetition"]
    + CASE_IDS
    + REQUIREMENT_IDS
    + [
        "tests_passed",
        "requirements_satisfied",
        "R",
        "F",
        "cyclomatic_complexity",
        "C",
        "maintainability_index",
        "M",
        "security_low",
        "security_medium",
        "security_high",
        "S",
        "ICC",
        "syntax_valid",
    ]
)


def write_csv(results):
    rows = []
    for result in results:
        row = {"sample_id": result["sample_id"], "model": result["model"], "repetition": result["repetition"]}
        for case_id in CASE_IDS:
            row[case_id] = result.get(case_id, 0)
        for req_id in REQUIREMENT_IDS:
            row[req_id] = result.get(req_id, 0)
        row["tests_passed"] = result.get("tests_passed")
        row["requirements_satisfied"] = result.get("requirements_satisfied")
        row["R"] = result.get("R")
        row["F"] = result.get("F")
        row["cyclomatic_complexity"] = result.get("cyclomatic_complexity")
        row["C"] = result.get("C")
        row["maintainability_index"] = result.get("maintainability_index")
        row["M"] = result.get("M")
        row["security_low"] = result.get("security_low")
        row["security_medium"] = result.get("security_medium")
        row["security_high"] = result.get("security_high")
        row["S"] = result.get("S")
        row["ICC"] = result.get("ICC")
        row["syntax_valid"] = result.get("syntax_valid")
        rows.append(row)

    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    return rows


# ---------------------------------------------------------------------------
# Estadistica descriptiva
# ---------------------------------------------------------------------------
def describe(values):
    clean = [float(v) for v in values if v is not None]
    if not clean:
        return None
    summary = {
        "n": len(clean),
        "mean": statistics.fmean(clean),
        "median": statistics.median(clean),
        "stdev": statistics.stdev(clean) if len(clean) > 1 else 0.0,
        "min": min(clean),
        "max": max(clean),
    }
    if len(clean) >= 2:
        q = statistics.quantiles(sorted(clean), n=4, method="inclusive")
        summary["iqr"] = q[2] - q[0]
    else:
        summary["iqr"] = 0.0
    return summary


def stats_by_model(results):
    stats = {}
    for model in MODELS:
        subset = [r for r in results if r["model"] == model]
        stats[model] = {dim: describe([r.get(dim) for r in subset]) for dim in DIMENSIONS}
    return stats


def ratio_matrix(results, ids):
    """{id: {model: (aprobados, total)}} para casos o requisitos."""
    matrix = {}
    for item_id in ids:
        matrix[item_id] = {}
        for model in MODELS:
            subset = [r for r in results if r["model"] == model]
            passed = sum(1 for r in subset if r.get(item_id) == 1)
            matrix[item_id][model] = (passed, len(subset))
    return matrix


# ---------------------------------------------------------------------------
# Reporte markdown
# ---------------------------------------------------------------------------
def fmt(value, digits=2):
    if value is None:
        return "N/A"
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, int):
        return str(value)
    return f"{value:.{digits}f}"


def build_markdown(results, rows, stats, cases_matrix, req_matrix):
    total = len(results)
    models_present = sorted({r["model"] for r in results})
    syntax_invalid = [r for r in results if not r.get("syntax_valid")]
    methodological = [
        r for r in results
        for incident in r.get("incidents", [])
        if incident.get("stage") in ("radon", "bandit", "pytest")
    ]
    encoding_incidents = [r for r in results if r.get("encoding_incident")]
    valid = [r for r in results if r.get("syntax_valid")]

    lines = []
    lines.append("# Análisis de resultados — T1")
    lines.append("")
    lines.append("## 1. Descripción de la ejecución")
    lines.append("")
    lines.append(f"- Muestras procesadas: {total}")
    lines.append(f"- Modelos: {', '.join(models_present)}")
    counts = {m: sum(1 for r in results if r["model"] == m) for m in models_present}
    lines.append(f"- Muestras por modelo: {counts}")
    lines.append("- Instrumentos utilizados:")
    lines.append("  - `tasks/T1/prompt.md` (especificación congelada)")
    lines.append("  - `tasks/T1/tests/test_t1.py` (10 casos funcionales) vía pytest")
    lines.append("  - Radon (complejidad ciclomática promedio e índice de mantenibilidad)")
    lines.append("  - Bandit (hallazgos de seguridad por severidad)")
    lines.append("  - Fórmulas de `evaluator/scoring.py` (R, F, C, M, S, ICC)")
    lines.append("")

    lines.append("## 2. Integridad de los datos")
    lines.append("")
    lines.append(f"- Muestras procesadas: {total}/30")
    lines.append(f"- Mediciones válidas (sintaxis correcta): {len(valid)}")
    lines.append(f"- Muestras con error de sintaxis/fuente: {len(syntax_invalid)}")
    for r in syntax_invalid:
        detail = next(
            (i for i in r.get("incidents", []) if i.get("stage") == "syntax"), {}
        )
        lines.append(
            f"  - {r['sample_id']} ({r['model']}): "
            f"{detail.get('status', 'n/a')} — {detail.get('message', '')}"
        )
    lines.append(f"- Muestras con incidencia metodológica de herramienta: {len(methodological)}")
    lines.append(f"- Muestras con incidencia de encoding (medición sobre representación temporal UTF-8): {len(encoding_incidents)}")
    for r in encoding_incidents:
        lines.append(
            f"  - {r['sample_id']} ({r['model']}): original no UTF-8 "
            f"({r['original_path']}); archivo original NO modificado"
        )
    lines.append("- Las muestras con error de sintaxis/fuente se conservaron y se les aplicó el protocolo (ceros e ICC=0); no son mediciones de C/M/S.")
    lines.append("")

    # 3. Requisitos
    lines.append("## 3. Cumplimiento de requisitos — R")
    lines.append("")
    lines.append("| Requisito | " + " | ".join(models_present) + " |")
    lines.append("|---|" + "|".join(["---"] * len(models_present)) + "|")
    for req_id in REQUIREMENT_IDS:
        cells = []
        for m in models_present:
            passed, tot = req_matrix[req_id][m]
            pct = (passed / tot * 100) if tot else 0
            cells.append(f"{passed}/{tot} ({pct:.0f}%)")
        lines.append(f"| {req_id} | " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("Media de R por modelo:")
    for m in models_present:
        lines.append(f"- {m}: {fmt(stats[m]['R']['mean'])} (mediana {fmt(stats[m]['R']['median'])})")
    lines.append("")

    # 4. F
    lines.append("## 4. Corrección funcional — F")
    lines.append("")
    lines.append("| Modelo | tests aprobados (media/10) | F media | F mediana | F mín | F máx |")
    lines.append("|---|---|---|---|---|---|")
    for m in models_present:
        subset = [r for r in results if r["model"] == m]
        mean_passed = statistics.fmean([r.get("tests_passed") or 0 for r in subset])
        s = stats[m]["F"]
        lines.append(
            f"| {m} | {mean_passed:.1f}/10 | {fmt(s['mean'])} | {fmt(s['median'])} | "
            f"{fmt(s['min'])} | {fmt(s['max'])} |"
        )
    lines.append("")

    # 5. Casos
    lines.append("## 5. Análisis por caso de prueba")
    lines.append("")
    lines.append("| Caso | " + " | ".join(models_present) + " |")
    lines.append("|---|" + "|".join(["---"] * len(models_present)) + "|")
    for case_id in CASE_IDS:
        cells = []
        for m in models_present:
            passed, tot = cases_matrix[case_id][m]
            pct = (passed / tot * 100) if tot else 0
            cells.append(f"{passed}/{tot} ({pct:.0f}%)")
        lines.append(f"| {case_id} | " + " | ".join(cells) + " |")
    lines.append("")
    lines.extend(_case_observations(cases_matrix, models_present))
    lines.append("")

    # 6. C
    lines.append("## 6. Complejidad — C")
    lines.append("")
    lines.append("| Modelo | CC media | CC mediana | C media | C mediana | C mín | C máx |")
    lines.append("|---|---|---|---|---|---|---|")
    for m in models_present:
        subset = [r for r in results if r["model"] == m]
        cc_vals = [r.get("cyclomatic_complexity") for r in subset if r.get("cyclomatic_complexity") is not None]
        cc_mean = statistics.fmean(cc_vals) if cc_vals else None
        cc_med = statistics.median(cc_vals) if cc_vals else None
        s = stats[m]["C"]
        lines.append(
            f"| {m} | {fmt(cc_mean)} | {fmt(cc_med)} | {fmt(s['mean'])} | {fmt(s['median'])} | "
            f"{fmt(s['min'])} | {fmt(s['max'])} |"
        )
    lines.append("")

    # 7. M
    lines.append("## 7. Mantenibilidad — M")
    lines.append("")
    lines.append("| Modelo | MI media | M media | M mediana | M mín | M máx |")
    lines.append("|---|---|---|---|---|---|")
    for m in models_present:
        subset = [r for r in results if r["model"] == m]
        mi_vals = [r.get("maintainability_index") for r in subset if r.get("maintainability_index") is not None]
        mi_mean = statistics.fmean(mi_vals) if mi_vals else None
        s = stats[m]["M"]
        lines.append(
            f"| {m} | {fmt(mi_mean)} | {fmt(s['mean'])} | {fmt(s['median'])} | "
            f"{fmt(s['min'])} | {fmt(s['max'])} |"
        )
    lines.append("")

    # 8. S
    lines.append("## 8. Seguridad — S")
    lines.append("")
    lines.append("| Modelo | low (total) | medium (total) | high (total) | S media | S mín | S máx |")
    lines.append("|---|---|---|---|---|---|---|")
    for m in models_present:
        subset = [r for r in results if r["model"] == m]
        low = sum(r.get("security_low") or 0 for r in subset)
        med = sum(r.get("security_medium") or 0 for r in subset)
        high = sum(r.get("security_high") or 0 for r in subset)
        s = stats[m]["S"]
        lines.append(
            f"| {m} | {low} | {med} | {high} | {fmt(s['mean'])} | {fmt(s['min'])} | {fmt(s['max'])} |"
        )
    lines.append("")

    # 9. ICC
    lines.append("## 9. Índice de Calidad del Código — ICC")
    lines.append("")
    lines.append("| Modelo | ICC media | ICC mediana | ICC mín | ICC máx |")
    lines.append("|---|---|---|---|---|")
    for m in models_present:
        s = stats[m]["ICC"]
        lines.append(
            f"| {m} | {fmt(s['mean'])} | {fmt(s['median'])} | {fmt(s['min'])} | {fmt(s['max'])} |"
        )
    lines.append("")

    # 10. Variabilidad
    lines.append("## 10. Variabilidad")
    lines.append("")
    lines.append("| Modelo | Dimensión | media | mediana | desv. est. | mín | máx | IQR |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for m in models_present:
        for dim in DIMENSIONS:
            s = stats[m][dim]
            if s is None:
                continue
            lines.append(
                f"| {m} | {dim} | {fmt(s['mean'])} | {fmt(s['median'])} | {fmt(s['stdev'])} | "
                f"{fmt(s['min'])} | {fmt(s['max'])} | {fmt(s['iqr'])} |"
            )
    lines.append("")

    # 11. Observaciones
    lines.append("## 11. Observaciones técnicas")
    lines.append("")
    lines.extend(_technical_observations(results, stats, cases_matrix, req_matrix, models_present))
    lines.append("")

    # 12. Datos para el informe
    lines.append("## 12. Datos relevantes para el informe")
    lines.append("")
    lines.append("- Los datos anteriores provienen exclusivamente de la ejecución de T1 sobre 10 muestras por modelo.")
    lines.append("- R y F se derivan del instrumento congelado; C, M y S de Radon y Bandit; ICC de la fórmula del protocolo.")
    lines.append("- Las diferencias aquí descritas son observadas en esta ejecución; no implican relaciones causales.")
    lines.append("- No debe inferirse superioridad universal de ningún modelo a partir de estos datos.")
    lines.append("")
    return "\n".join(lines)


def _case_observations(cases_matrix, models):
    lines = []
    ratios = {}
    for case_id in CASE_IDS:
        values = []
        for m in models:
            passed, tot = cases_matrix[case_id][m]
            values.append(passed / tot if tot else 0)
        ratios[case_id] = values
    all_pass = [
        c for c in CASE_IDS
        if all(cases_matrix[c][m][0] == cases_matrix[c][m][1] for m in models)
    ]
    global_ratio = {c: sum(ratios[c]) / len(models) for c in CASE_IDS}
    min_v = min(global_ratio.values())
    max_v = max(global_ratio.values())
    worst = [c for c in CASE_IDS if global_ratio[c] == min_v]
    best = [c for c in CASE_IDS if global_ratio[c] == max_v]

    lines.append(
        "DATO: casos en los que los modelos aprobaron el 100% de sus muestras: "
        + (", ".join(all_pass) if all_pass else "ninguno") + "."
    )
    lines.append("")
    if min_v == max_v:
        lines.append(
            "OBSERVACIÓN: en esta ejecución todos los casos presentaron la misma "
            f"proporción global de aprobación ({min_v*100:.0f}%); no hubo casos con "
            "mayor o menor porcentaje de fallos entre sí."
        )
    else:
        lines.append(
            "OBSERVACIÓN: casos con menor proporción global de aprobación: "
            + ", ".join(f"{c} ({global_ratio[c]*100:.0f}%)" for c in worst) + "."
        )
        lines.append("")
        lines.append(
            "OBSERVACIÓN: casos con mayor proporción global de aprobación: "
            + ", ".join(f"{c} ({global_ratio[c]*100:.0f}%)" for c in best) + "."
        )
    return lines


def _technical_observations(results, stats, cases_matrix, req_matrix, models):
    lines = []
    # Diferencias por caso.
    spreads = []
    for case_id in CASE_IDS:
        passed_counts = [cases_matrix[case_id][m][0] for m in models]
        spreads.append((case_id, max(passed_counts) - min(passed_counts)))
    spread_sorted = sorted(spreads, key=lambda item: item[1], reverse=True)
    lines.append("DATO: mayor diferencia de aprobaciones entre modelos por caso: "
                 + ", ".join(f"{c} (Δ={d} muestras)" for c, d in spread_sorted[:3]) + ".")
    lines.append("")
    # Requisitos no cumplidos.
    failed_reqs = []
    for req_id in REQUIREMENT_IDS:
        for m in models:
            passed, tot = req_matrix[req_id][m]
            if passed < tot:
                failed_reqs.append(f"{req_id}/{m} ({passed}/{tot})")
    lines.append("DATO: requisitos no cumplidos por algún modelo: "
                 + (", ".join(failed_reqs) if failed_reqs else "ninguno") + ".")
    lines.append("")
    # Bandit hallazgos.
    for m in models:
        subset = [r for r in results if r["model"] == m]
        high = sum(r.get("security_high") or 0 for r in subset)
        med = sum(r.get("security_medium") or 0 for r in subset)
        lines.append(f"DATO: {m} — hallazgos Bandit: {med} de severidad media, {high} de severidad alta.")
    lines.append("")
    lines.append("OBSERVACIÓN: las cifras reflejan únicamente las 10 muestras de T1 y las herramientas empleadas; no permiten atribuir causas ni generalizar a otros contextos.")
    return lines


def main():
    samples = discover_samples()
    print(f"Muestras encontradas: {len(samples)}")
    per_model = {m: sum(1 for s in samples if s["model"] == m) for m in MODELS}
    print(f"Por modelo: {per_model}")

    results = evaluate_samples(samples)
    processed = len(results)
    print(f"Muestras procesadas: {processed}")

    write_individual_results(results)
    rows = write_csv(results)
    stats = stats_by_model(results)
    cases_matrix = ratio_matrix(results, CASE_IDS)
    req_matrix = ratio_matrix(results, REQUIREMENT_IDS)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        build_markdown(results, rows, stats, cases_matrix, req_matrix), encoding="utf-8"
    )
    print(f"JSON individuales en: {RAW_DIR}")
    print(f"CSV en: {CSV_PATH}")
    print(f"Reporte en: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
