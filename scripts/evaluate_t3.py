"""FASE T3-B: evaluacion de las 30 muestras de T3 y generacion de resultados.

Ejecuta el instrumento congelado de T3 sobre las 30 muestras (10 por modelo),
produce:
- results/raw/T3/<modelo>/<sample_id>.json   (resultado individual)
- results/consolidated/T3_results.csv        (30 filas)
- results/reports/T3_analysis.md             (analisis descriptivo)

No modifica muestras, prompt.md, requirements.json, test_cases.md,
test_t3.py ni restrictions_check.py. No genera datos ficticios.

T3-R5 tiene evidencia funcional (T3-C09, T3-C10) y estatica
(tasks/T3/restrictions_check.py). R5 = 1 solo si ambas partes pasan.
Las comprobaciones estatica y de Bandit son independientes: Bandit no decide
R5 y restrictions_check no calcula S.

Uso:
    .venv\\Scripts\\python.exe scripts\\evaluate_t3.py
"""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import re
import statistics
import sys
import tempfile
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "tasks" / "T3"))

from evaluator.evaluator import evaluate_sample
from evaluator import scoring
import restrictions_check

MODELS = ("chatgpt", "deepseek", "opencode")
TASK = "T3"
TESTS_PATH = PROJECT_ROOT / "tasks" / TASK / "tests" / "test_t3.py"
SAMPLES_ROOT = PROJECT_ROOT / "samples"
RAW_DIR = PROJECT_ROOT / "results" / "raw" / TASK
CSV_PATH = PROJECT_ROOT / "results" / "consolidated" / f"{TASK}_results.csv"
REPORT_PATH = PROJECT_ROOT / "results" / "reports" / f"{TASK}_analysis.md"

CASE_IDS = [f"T3-C{i:02d}" for i in range(1, 11)]
REQUIREMENT_IDS = [f"T3-R{i}" for i in range(1, 6)]
DIMENSIONS = ("R", "F", "C", "M", "S", "ICC")

# Evidencia congelada requisito -> casos (T3-R5 se refina con la parte estatica).
CASE_REQUIREMENT_MAP = {
    "T3-R1": ["T3-C10"],
    "T3-R2": ["T3-C01", "T3-C02", "T3-C03"],
    "T3-R3": ["T3-C04", "T3-C05"],
    "T3-R4": ["T3-C06", "T3-C07", "T3-C08"],
    "T3-R5": ["T3-C09", "T3-C10"],
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
    """Aplica el protocolo a muestras no evaluables (sintaxis/fuente)."""
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
            "status": "not_evaluable",
            "message": (
                "Muestra no evaluable (error de sintaxis real o codificacion no "
                "recuperable); por protocolo se asignan ceros e ICC=0 "
                "(dimensiones no medidas)."
            ),
        }
    )


def apply_r5_rule(result, static_passed):
    """Aplica T3-R5 = C09 AND C10 AND restricciones estaticas, y recalcula R."""
    detail = dict(result.get("requirements") or {})
    for req_id in REQUIREMENT_IDS:
        detail.setdefault(req_id, result.get(req_id, 0))
    r5 = 1 if (
        result.get("T3-C09") == 1
        and result.get("T3-C10") == 1
        and bool(static_passed)
    ) else 0
    detail["T3-R5"] = r5
    result["requirements"] = detail
    for req_id in REQUIREMENT_IDS:
        result[req_id] = detail.get(req_id, 0)
    satisfied = sum(detail.get(req_id, 0) for req_id in REQUIREMENT_IDS)
    result["requirements_satisfied"] = satisfied
    result["R"] = scoring.calculate_requirements_score(satisfied, 5)


def transcode_if_needed(sample, temp_dir, sha_before):
    """Devuelve (ruta_a_evaluar, incidencia_encoding) segun el protocolo T2/T3."""
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
            candidate = raw.decode(encoding)
        except UnicodeDecodeError:
            continue
        try:
            ast.parse(candidate)
        except SyntaxError:
            continue
        decoded = candidate
        used_encoding = encoding
        break

    if decoded is None:
        return sample["path"], {
            "stage": "encoding",
            "status": "undecodable",
            "message": (
                "El archivo no es UTF-8 valido y ninguna decodificacion "
                "(cp1252/latin-1) produce contenido sintacticamente valido; no se "
                "pudo obtener una representacion medible de forma objetiva. "
                f"Original: {sample['path']}"
            ),
            "original_path": str(sample["path"]),
            "sha256_before": sha_before,
            "original_modified": False,
        }

    temp_path = Path(temp_dir) / f"{sample['sample_id']}__utf8.py"
    temp_path.write_text(decoded, encoding="utf-8")
    incident = {
        "stage": "encoding",
        "status": "transcoded_for_measurement",
        "message": (
            f"El archivo original no es UTF-8 valido; se decodifico como {used_encoding} "
            "y se midio sobre una representacion temporal UTF-8 (misma representacion "
            "para pytest, restrictions_check, Radon y Bandit). El archivo original NO "
            "fue modificado."
        ),
        "original_path": str(sample["path"]),
        "source_encoding": used_encoding,
        "sha256_before": sha_before,
        "original_modified": False,
    }
    return temp_path, incident


def evaluate_samples(samples):
    results = []
    hashes = {}
    with tempfile.TemporaryDirectory(prefix="seat_t3_encoding_") as temp_dir:
        for sample in samples:
            sha_before = hashlib.sha256(sample["path"].read_bytes()).hexdigest()
            hashes[sample["sample_id"]] = (sample["path"], sha_before)

            eval_path, encoding_incident = transcode_if_needed(
                sample, temp_dir, sha_before
            )

            result = evaluate_sample(
                sample_id=sample["sample_id"],
                system=sample["model"],
                task=TASK,
                repetition=sample["repetition"],
                code_path=eval_path,
                tests_path=TESTS_PATH,
                case_requirement_map=CASE_REQUIREMENT_MAP,
            )

            result["encoding_incident"] = encoding_incident is not None
            if encoding_incident is not None:
                result["original_path"] = str(sample["path"])
                result["original_modified"] = False
                result["incidents"].append(encoding_incident)

            # Comprobacion estatica sobre LA MISMA representacion usada para medir.
            restriction = restrictions_check.check_external_restrictions(eval_path)
            result["external_restrictions_passed"] = restriction["passed"]
            result["external_restrictions_violations"] = restriction["violations"]
            result["non_stdlib_imports"] = restriction["non_stdlib_imports"]

            if not result["syntax_valid"]:
                force_protocol_zeros(result)
            else:
                apply_r5_rule(result, restriction["passed"])

            results.append(result)

    # Verificacion de integridad del original.
    for result in results:
        path, sha_before = hashes[result["sample_id"]]
        sha_after = hashlib.sha256(path.read_bytes()).hexdigest()
        result["original_sha256"] = sha_before
        result["original_hash_unchanged"] = sha_after == sha_before
        if result.get("encoding_incident"):
            for incident in result["incidents"]:
                if incident.get("stage") == "encoding":
                    incident["sha256_after"] = sha_after
                    incident["hash_unchanged"] = sha_after == sha_before
    return results


def write_individual_results(results):
    for result in results:
        model_dir = RAW_DIR / result["model"]
        model_dir.mkdir(parents=True, exist_ok=True)
        path = model_dir / f"{result['sample_id']}.json"
        path.write_text(
            json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
        )


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
        "external_restrictions_passed",
        "R",
        "F",
        "cyclomatic_complexity",
        "max_complexity",
        "C",
        "maintainability_index",
        "M",
        "security_low",
        "security_medium",
        "security_high",
        "S",
        "ICC",
        "syntax_valid",
        "encoding_incident",
    ]
)


def write_csv(results):
    rows = []
    for result in results:
        row = {
            "sample_id": result["sample_id"],
            "model": result["model"],
            "repetition": result["repetition"],
        }
        for case_id in CASE_IDS:
            row[case_id] = result.get(case_id, 0)
        for req_id in REQUIREMENT_IDS:
            row[req_id] = result.get(req_id, 0)
        row["tests_passed"] = result.get("tests_passed")
        row["requirements_satisfied"] = result.get("requirements_satisfied")
        row["external_restrictions_passed"] = result.get("external_restrictions_passed")
        row["R"] = result.get("R")
        row["F"] = result.get("F")
        row["cyclomatic_complexity"] = result.get("cyclomatic_complexity")
        row["max_complexity"] = result.get("max_complexity")
        row["C"] = result.get("C")
        row["maintainability_index"] = result.get("maintainability_index")
        row["M"] = result.get("M")
        row["security_low"] = result.get("security_low")
        row["security_medium"] = result.get("security_medium")
        row["security_high"] = result.get("security_high")
        row["S"] = result.get("S")
        row["ICC"] = result.get("ICC")
        row["syntax_valid"] = result.get("syntax_valid")
        row["encoding_incident"] = result.get("encoding_incident")
        rows.append(row)

    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    return rows


# ---------------------------------------------------------------------------
# Estadistica descriptiva y matrices
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
    matrix = {}
    for item_id in ids:
        matrix[item_id] = {}
        for model in MODELS:
            subset = [r for r in results if r["model"] == model]
            passed = sum(1 for r in subset if r.get(item_id) == 1)
            matrix[item_id][model] = (passed, len(subset))
    return matrix


def bandit_findings(result):
    """Devuelve la lista de hallazgos Bandit desde la salida cruda."""
    raw = (result.get("bandit") or {}).get("stdout") or ""
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return []
    return data.get("results", []) or []


def security_summary(results):
    summary = {}
    for model in MODELS:
        subset = [r for r in results if r["model"] == model]
        low = sum(r.get("security_low") or 0 for r in subset)
        med = sum(r.get("security_medium") or 0 for r in subset)
        high = sum(r.get("security_high") or 0 for r in subset)
        affected = sum(1 for r in subset if (r.get("security_low") or 0) + (r.get("security_medium") or 0) + (r.get("security_high") or 0) > 0)
        test_ids = Counter()
        eval_samples = 0
        for r in subset:
            findings = bandit_findings(r)
            if findings:
                pass
            uses_eval = False
            for finding in findings:
                test_ids[finding.get("test_id", "?")] += 1
                text = str(finding.get("issue_text", "")).lower()
                if finding.get("test_id") == "B307" or "eval" in text:
                    uses_eval = True
            if uses_eval:
                eval_samples += 1
        summary[model] = {
            "low": low,
            "medium": med,
            "high": high,
            "affected_samples": affected,
            "test_ids": test_ids,
            "eval_samples": eval_samples,
        }
    return summary


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


def build_markdown(results, stats, cases_matrix, req_matrix, sec_summary):
    total = len(results)
    models_present = sorted({r["model"] for r in results})
    syntax_invalid = [r for r in results if not r.get("syntax_valid")]
    encoding_incidents = [r for r in results if r.get("encoding_incident")]
    restriction_failures = [r for r in results if not r.get("external_restrictions_passed")]
    valid = [r for r in results if r.get("syntax_valid")]

    lines = []
    lines.append("# Análisis de resultados — T3")
    lines.append("")
    lines.append("## 1. Descripción de la ejecución")
    lines.append("")
    lines.append(f"- Muestras procesadas: {total}")
    lines.append(f"- Modelos: {', '.join(models_present)}")
    counts = {m: sum(1 for r in results if r["model"] == m) for m in models_present}
    lines.append(f"- Muestras por modelo: {counts}")
    lines.append("- Instrumentos utilizados:")
    lines.append("  - `tasks/T3/prompt.md` (especificación congelada)")
    lines.append("  - `tasks/T3/tests/test_t3.py` (10 casos funcionales) vía pytest")
    lines.append("  - `tasks/T3/restrictions_check.py` (restricciones externas, T3-R5)")
    lines.append("  - Radon (complejidad media/máxima y mantenibilidad)")
    lines.append("  - Bandit (seguridad estática, dimensión S)")
    lines.append("  - Fórmulas de `evaluator/scoring.py` (R, F, C, M, S, ICC)")
    lines.append("")

    lines.append("## 2. Integridad de los datos")
    lines.append("")
    lines.append(f"- Muestras procesadas: {total}/30")
    lines.append(f"- Mediciones válidas (sintaxis correcta): {len(valid)}")
    lines.append(f"- Muestras con error de sintaxis real: {len(syntax_invalid)}")
    for r in syntax_invalid:
        detail = next((i for i in r.get("incidents", []) if i.get("stage") == "syntax"), {})
        lines.append(f"  - {r['sample_id']} ({r['model']}): {detail.get('status','n/a')} — {detail.get('message','')}")
    lines.append(f"- Muestras con incidencia de encoding (representación temporal UTF-8): {len(encoding_incidents)}")
    for r in encoding_incidents:
        detail = next((i for i in r.get("incidents", []) if i.get("stage") == "encoding"), {})
        lines.append(
            f"  - {r['sample_id']} ({r['model']}): {detail.get('status')}, "
            f"source_encoding={detail.get('source_encoding')}, hash_unchanged={detail.get('hash_unchanged')}; original NO modificado"
        )
    lines.append(f"- Muestras que no cumplen restricciones externas: {len(restriction_failures)}")
    lines.append("")

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

    lines.append("## 6. Restricciones externas — T3-R5")
    lines.append("")
    lines.append("| Modelo | restrictions_check passed | muestras con incumplimiento |")
    lines.append("|---|---|---|")
    for m in models_present:
        subset = [r for r in results if r["model"] == m]
        passed = sum(1 for r in subset if r.get("external_restrictions_passed"))
        failed = len(subset) - passed
        lines.append(f"| {m} | {passed}/{len(subset)} | {failed} |")
    lines.append("")
    for r in restriction_failures:
        cats = Counter(v.get("category") for v in r.get("external_restrictions_violations", []))
        lines.append(
            f"- {r['sample_id']} ({r['model']}): no pasa restrictions_check "
            f"({dict(cats)}); no_stdlib={r.get('non_stdlib_imports')}"
        )
    lines.append("")
    lines.append("Nota: T3-R5 = 1 solo si T3-C09 pasa, T3-C10 pasa y restrictions_check pasa. Bandit es independiente (dimensión S).")
    lines.append("")

    lines.append("## 7. Complejidad — C")
    lines.append("")
    lines.append("| Modelo | CC media | CC mediana | CC máx (media) | C media | C mediana | C mín | C máx |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for m in models_present:
        subset = [r for r in results if r["model"] == m]
        cc_vals = [r.get("cyclomatic_complexity") for r in subset if r.get("cyclomatic_complexity") is not None]
        mx_vals = [r.get("max_complexity") for r in subset if r.get("max_complexity") is not None]
        s = stats[m]["C"]
        lines.append(
            f"| {m} | {fmt(statistics.fmean(cc_vals) if cc_vals else None)} | "
            f"{fmt(statistics.median(cc_vals) if cc_vals else None)} | "
            f"{fmt(statistics.fmean(mx_vals) if mx_vals else None)} | "
            f"{fmt(s['mean'])} | {fmt(s['median'])} | {fmt(s['min'])} | {fmt(s['max'])} |"
        )
    lines.append("")

    lines.append("## 8. Mantenibilidad — M")
    lines.append("")
    lines.append("| Modelo | MI media | M media | M mediana | M mín | M máx |")
    lines.append("|---|---|---|---|---|---|")
    for m in models_present:
        subset = [r for r in results if r["model"] == m]
        mi_vals = [r.get("maintainability_index") for r in subset if r.get("maintainability_index") is not None]
        s = stats[m]["M"]
        lines.append(
            f"| {m} | {fmt(statistics.fmean(mi_vals) if mi_vals else None)} | {fmt(s['mean'])} | "
            f"{fmt(s['median'])} | {fmt(s['min'])} | {fmt(s['max'])} |"
        )
    lines.append("")

    lines.append("## 9. Seguridad — S")
    lines.append("")
    lines.append("### 9.1 Hallazgos por severidad")
    lines.append("")
    lines.append("| Modelo | low | medium | high | muestras con ≥1 hallazgo |")
    lines.append("|---|---|---|---|---|")
    for m in models_present:
        s = sec_summary[m]
        lines.append(f"| {m} | {s['low']} | {s['medium']} | {s['high']} | {s['affected_samples']}/10 |")
    lines.append("")
    lines.append("### 9.2 Tipos de hallazgo")
    lines.append("")
    for m in models_present:
        s = sec_summary[m]
        if s["test_ids"]:
            detail = ", ".join(f"{tid}={n}" for tid, n in sorted(s["test_ids"].items()))
        else:
            detail = "ninguno"
        lines.append(f"- {m}: {detail}")
    lines.append("")
    lines.append("### 9.3 Uso de eval u otros patrones relevantes")
    lines.append("")
    for m in models_present:
        lines.append(f"- {m}: Bandit identificó eval/B307 en {sec_summary[m]['eval_samples']}/10 muestras.")
    lines.append("")
    lines.append("### 9.4 Puntuación S por modelo")
    lines.append("")
    lines.append("| Modelo | S media | S mediana | S mín | S máx |")
    lines.append("|---|---|---|---|---|")
    for m in models_present:
        s = stats[m]["S"]
        lines.append(f"| {m} | {fmt(s['mean'])} | {fmt(s['median'])} | {fmt(s['min'])} | {fmt(s['max'])} |")
    lines.append("")

    lines.append("## 10. Índice de Calidad del Código — ICC")
    lines.append("")
    lines.append("| Modelo | ICC media | ICC mediana | ICC mín | ICC máx |")
    lines.append("|---|---|---|---|---|")
    for m in models_present:
        s = stats[m]["ICC"]
        lines.append(f"| {m} | {fmt(s['mean'])} | {fmt(s['median'])} | {fmt(s['min'])} | {fmt(s['max'])} |")
    lines.append("")

    lines.append("## 11. Variabilidad")
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

    lines.append("## 12. Incidencias metodológicas")
    lines.append("")
    if not syntax_invalid and not encoding_incidents and not restriction_failures:
        lines.append("- No se registraron incidencias metodológicas en esta ejecución.")
    for r in encoding_incidents:
        detail = next((i for i in r.get("incidents", []) if i.get("stage") == "encoding"), {})
        lines.append(
            f"- {r['sample_id']} ({r['model']}): encoding ({detail.get('status')}, "
            f"source_encoding={detail.get('source_encoding')}, hash_unchanged={detail.get('hash_unchanged')}); original NO modificado."
        )
    for r in syntax_invalid:
        lines.append(f"- {r['sample_id']} ({r['model']}): error de sintaxis del código generado (syntax_valid=false, ICC=0).")
    lines.append("")

    lines.append("## 13. Observaciones técnicas")
    lines.append("")
    lines.extend(_technical_observations(results, cases_matrix, req_matrix, models_present))
    lines.append("")

    lines.append("## 14. Datos relevantes para el informe académico")
    lines.append("")
    lines.append("- Los datos provienen exclusivamente de la ejecución de T3 sobre 10 muestras por modelo.")
    lines.append("- R y F se derivan del instrumento congelado de T3 (R5 incluye evidencia estática); C, M y S de Radon y Bandit; ICC de la fórmula del protocolo.")
    lines.append("- Bandit y restrictions_check son independientes: Bandit alimenta S, restrictions_check alimenta R5.")
    lines.append("- Las diferencias descritas son observadas en esta ejecución; no implican relaciones causales.")
    lines.append("- No debe inferirse superioridad de ningún modelo a partir de estos datos.")
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
    all_pass = [c for c in CASE_IDS if all(cases_matrix[c][m][0] == cases_matrix[c][m][1] for m in models)]
    global_ratio = {c: sum(ratios[c]) / len(models) for c in CASE_IDS}
    min_v = min(global_ratio.values())
    max_v = max(global_ratio.values())
    worst = [c for c in CASE_IDS if global_ratio[c] == min_v]
    best = [c for c in CASE_IDS if global_ratio[c] == max_v]
    lines.append(
        "DATO: casos en los que los tres modelos aprobaron el 100% de sus muestras: "
        + (", ".join(all_pass) if all_pass else "ninguno") + "."
    )
    lines.append("")
    if min_v == max_v:
        lines.append(
            "OBSERVACIÓN: en esta ejecución todos los casos presentaron la misma "
            f"proporción global de aprobación ({min_v*100:.0f}%)."
        )
    else:
        lines.append("OBSERVACIÓN: casos con menor proporción global de aprobación: " + ", ".join(f"{c} ({global_ratio[c]*100:.0f}%)" for c in worst) + ".")
        lines.append("")
        lines.append("OBSERVACIÓN: casos con mayor proporción global de aprobación: " + ", ".join(f"{c} ({global_ratio[c]*100:.0f}%)" for c in best) + ".")
    return lines


def _technical_observations(results, cases_matrix, req_matrix, models):
    lines = []
    spreads = []
    for case_id in CASE_IDS:
        passed_counts = [cases_matrix[case_id][m][0] for m in models]
        spreads.append((case_id, max(passed_counts) - min(passed_counts)))
    max_spread = max((d for _, d in spreads), default=0)
    if max_spread == 0:
        lines.append("DATO: no se observaron diferencias de aprobación entre modelos en ningún caso.")
    else:
        top = sorted((x for x in spreads if x[1] > 0), key=lambda x: x[1], reverse=True)[:3]
        lines.append("DATO: mayor diferencia de aprobaciones entre modelos por caso: " + ", ".join(f"{c} (Δ={d} muestras)" for c, d in top) + ".")
    lines.append("")
    failed_reqs = []
    for req_id in REQUIREMENT_IDS:
        for m in models:
            passed, tot = req_matrix[req_id][m]
            if passed < tot:
                failed_reqs.append(f"{req_id}/{m} ({passed}/{tot})")
    lines.append("DATO: requisitos no cumplidos por algún modelo: " + (", ".join(failed_reqs) if failed_reqs else "ninguno") + ".")
    lines.append("")
    lines.append("OBSERVACIÓN: las cifras reflejan únicamente las 10 muestras de T3 por modelo y las herramientas empleadas; no permiten atribuir causas ni generalizar a otros contextos.")
    return lines


def main():
    samples = discover_samples()
    print(f"Muestras encontradas: {len(samples)}")
    per_model = {m: sum(1 for s in samples if s["model"] == m) for m in MODELS}
    print(f"Por modelo: {per_model}")

    results = evaluate_samples(samples)
    print(f"Muestras procesadas: {len(results)}")

    write_individual_results(results)
    write_csv(results)
    stats = stats_by_model(results)
    cases_matrix = ratio_matrix(results, CASE_IDS)
    req_matrix = ratio_matrix(results, REQUIREMENT_IDS)
    sec_summary = security_summary(results)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        build_markdown(results, stats, cases_matrix, req_matrix, sec_summary),
        encoding="utf-8",
    )
    print(f"JSON individuales en: {RAW_DIR}")
    print(f"CSV en: {CSV_PATH}")
    print(f"Reporte en: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
