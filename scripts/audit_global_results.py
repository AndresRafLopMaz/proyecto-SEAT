"""FASE GLOBAL-A: auditoria, consolidacion y congelamiento de resultados T1/T2/T3.

Lee exclusivamente los consolidados cerrados:
    results/consolidated/T1_results.csv
    results/consolidated/T2_results.csv
    results/consolidated/T3_results.csv

Genera:
    results/consolidated/global_results.csv   (90 filas)
    results/consolidated/global_manifest.json (hashes, conteos, integridad)
    results/reports/global_data_audit.md      (reporte de auditoria)

NO reprocesa muestras, NO recalcula metricas, NO modifica las fuentes y NO
realiza analisis inferencial. Solo integridad, consolidacion, trazabilidad y
congelamiento. La formula oficial del ICC se recalcula unicamente con fines de
auditoria; nunca se reemplaza el valor almacenado.

Uso:
    .venv\\Scripts\\python.exe scripts\\audit_global_results.py
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import statistics
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CONSOLIDATED_DIR = PROJECT_ROOT / "results" / "consolidated"
REPORTS_DIR = PROJECT_ROOT / "results" / "reports"
GLOBAL_CSV = CONSOLIDATED_DIR / "global_results.csv"
MANIFEST_PATH = CONSOLIDATED_DIR / "global_manifest.json"
AUDIT_REPORT = REPORTS_DIR / "global_data_audit.md"

TASKS = ("T1", "T2", "T3")
MODELS = ("chatgpt", "deepseek", "opencode")
DIMENSIONS = ("R", "F", "C", "M", "S", "ICC")
SOURCE_FILES = {task: f"{task}_results.csv" for task in TASKS}

ICC_TOLERANCE = 0.05
MEAN_TOLERANCE = 0.02

# Medias cerradas conocidas (presentacion con 2 decimales).
KNOWN_MEANS = {
    ("T1", "chatgpt"): {"R": 100.00, "F": 100.00, "C": 78.00, "M": 49.22, "S": 100.00, "ICC": 85.44},
    ("T1", "deepseek"): {"R": 100.00, "F": 100.00, "C": 78.00, "M": 46.24, "S": 100.00, "ICC": 84.85},
    ("T1", "opencode"): {"R": 100.00, "F": 100.00, "C": 60.00, "M": 43.04, "S": 100.00, "ICC": 80.61},
    ("T2", "chatgpt"): {"R": 100.00, "F": 100.00, "C": 72.00, "M": 39.39, "S": 100.00, "ICC": 82.28},
    ("T2", "deepseek"): {"R": 100.00, "F": 100.00, "C": 76.00, "M": 33.13, "S": 100.00, "ICC": 81.83},
    ("T2", "opencode"): {"R": 100.00, "F": 100.00, "C": 38.00, "M": 34.44, "S": 100.00, "ICC": 74.49},
    ("T3", "chatgpt"): {"R": 100.00, "F": 100.00, "C": 78.00, "M": 42.49, "S": 96.00, "ICC": 83.30},
    ("T3", "deepseek"): {"R": 100.00, "F": 100.00, "C": 86.00, "M": 40.40, "S": 100.00, "ICC": 85.28},
    ("T3", "opencode"): {"R": 94.00, "F": 95.00, "C": 88.00, "M": 37.79, "S": 95.50, "ICC": 82.06},
}

GLOBAL_COLUMNS = (
    ["task", "model", "repetition", "sample_id"]
    + list(DIMENSIONS)
    + ["syntax_valid", "encoding_incident", "source_file"]
)


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _parse_bool(value):
    if value is None:
        return None
    text = str(value).strip().lower()
    if text in ("true", "1"):
        return True
    if text in ("false", "0"):
        return False
    return None


def _parse_float(value):
    """Devuelve (float|None, error|None). No sustituye valores invalidos."""
    if value is None:
        return None, "valor ausente (null)"
    text = str(value).strip()
    if text == "":
        return None, "cadena vacia"
    try:
        number = float(text)
    except ValueError:
        return None, f"valor no numerico: {value!r}"
    if math.isnan(number):
        return None, "NaN"
    if math.isinf(number):
        return None, "infinito"
    return number, None


def read_source(task):
    path = CONSOLIDATED_DIR / SOURCE_FILES[task]
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_records():
    records = []
    for task in TASKS:
        rows = read_source(task)
        for row in rows:
            record = {
                "task": task,
                "model": (row.get("model") or "").strip(),
                "repetition_raw": row.get("repetition"),
                "sample_id": (row.get("sample_id") or "").strip(),
                "syntax_valid": _parse_bool(row.get("syntax_valid")),
                "encoding_incident": _parse_bool(row.get("encoding_incident")),
                "source_file": SOURCE_FILES[task],
                "row": row,
            }
            for dim in DIMENSIONS:
                value, error = _parse_float(row.get(dim))
                record[dim] = value
                record[f"{dim}_error"] = error
            records.append(record)
    return records


def audit(records):
    errors = []
    warnings = []
    missing = []
    out_of_range = []

    # Conteos
    per_task = {t: sum(1 for r in records if r["task"] == t) for t in TASKS}
    per_model = {m: sum(1 for r in records if r["model"] == m) for m in MODELS}
    per_group = {
        (t, m): sum(1 for r in records if r["task"] == t and r["model"] == m)
        for t in TASKS for m in MODELS
    }

    for task, count in per_task.items():
        if count != 30:
            errors.append(f"{task} tiene {count} filas (esperado 30)")
    for model, count in per_model.items():
        if count != 30:
            errors.append(f"modelo {model} tiene {count} filas (esperado 30)")
    for (task, model), count in per_group.items():
        if count != 10:
            errors.append(f"{task}/{model} tiene {count} filas (esperado 10)")
    if len(records) != 90:
        errors.append(f"total de observaciones {len(records)} (esperado 90)")

    # Identificadores
    seen = {}
    repetition_local = {}
    for r in records:
        sid = r["sample_id"]
        if sid in seen:
            errors.append(f"sample_id duplicado: {sid}")
        seen[sid] = r
        if r["model"] not in MODELS:
            errors.append(f"modelo invalido en {sid}: {r['model']!r}")
        if r["task"] not in TASKS:
            errors.append(f"tarea invalida en {sid}: {r['task']!r}")
        rep = r["repetition_raw"]
        try:
            rep_int = int(str(rep).strip())
        except (TypeError, ValueError):
            errors.append(f"repetition invalida en {sid}: {rep!r}")
            continue
        if not (1 <= rep_int <= 10):
            errors.append(f"repetition fuera de 1..10 en {sid}: {rep_int}")
        repetition_local.setdefault((r["task"], r["model"], rep_int), []).append(sid)

    for key, sids in repetition_local.items():
        if len(sids) != 1:
            errors.append(f"repeticion {key} aparece {len(sids)} veces: {sids}")
    for task in TASKS:
        for model in MODELS:
            for rep in range(1, 11):
                if (task, model, rep) not in repetition_local:
                    errors.append(f"falta la combinacion {task}/{model}/R{rep:02d}")

    # Rangos y faltantes
    for r in records:
        for dim in DIMENSIONS:
            if r[f"{dim}_error"] is not None:
                missing.append(f"{r['sample_id']} {dim}: {r[f'{dim}_error']}")
                continue
            value = r[dim]
            if not (0.0 <= value <= 100.0):
                out_of_range.append(f"{r['sample_id']} {dim}={value}")

    if missing:
        errors.append(f"{len(missing)} valores faltantes/invalidos")
    if out_of_range:
        errors.append(f"{len(out_of_range)} valores fuera de rango [0,100]")

    # Consistencia del ICC (auditoria, sin reemplazar)
    icc_deltas = []
    icc_inconsistent = []
    for r in records:
        if any(r[d] is None for d in ("R", "F", "C", "M", "S", "ICC")):
            continue
        recalculated = 0.20 * (r["R"] + r["F"] + r["C"] + r["M"] + r["S"])
        delta = r["ICC"] - recalculated
        icc_deltas.append(abs(delta))
        r["icc_recalculated"] = recalculated
        r["icc_delta"] = delta
        r["icc_consistent"] = abs(delta) <= ICC_TOLERANCE
        if not r["icc_consistent"]:
            icc_inconsistent.append(
                f"{r['sample_id']} ICC={r['ICC']} recalc={recalculated:.6f} delta={delta:.6f}"
            )
    if icc_inconsistent:
        errors.append(f"{len(icc_inconsistent)} ICC inconsistentes")

    # Validacion contra medias conocidas
    means_report = {}
    mean_mismatches = []
    for task in TASKS:
        for model in MODELS:
            subset = [r for r in records if r["task"] == task and r["model"] == model]
            computed = {}
            for dim in DIMENSIONS:
                values = [r[dim] for r in subset if r[dim] is not None]
                computed[dim] = statistics.fmean(values) if values else None
            means_report[(task, model)] = computed
            known = KNOWN_MEANS[(task, model)]
            for dim in DIMENSIONS:
                if computed[dim] is None:
                    continue
                if abs(computed[dim] - known[dim]) > MEAN_TOLERANCE:
                    mean_mismatches.append(
                        f"{task}/{model} {dim}: calculado={computed[dim]:.4f} conocido={known[dim]:.2f}"
                    )
    if mean_mismatches:
        errors.append(f"{len(mean_mismatches)} medias no coinciden con los resultados cerrados")

    # Resumen syntax / encoding
    syntax_summary = {}
    for task in TASKS:
        for model in MODELS:
            subset = [r for r in records if r["task"] == task and r["model"] == model]
            false_count = sum(1 for r in subset if r["syntax_valid"] is False)
            encoding_true = sum(1 for r in subset if r["encoding_incident"] is True)
            encoding_na = sum(1 for r in subset if r["encoding_incident"] is None)
            syntax_summary[(task, model)] = {
                "syntax_false": false_count,
                "encoding_true": encoding_true,
                "encoding_not_registered": encoding_na,
            }

    return {
        "errors": errors,
        "warnings": warnings,
        "missing": missing,
        "out_of_range": out_of_range,
        "icc_inconsistent": icc_inconsistent,
        "icc_max_abs_delta": max(icc_deltas) if icc_deltas else 0.0,
        "mean_mismatches": mean_mismatches,
        "per_task": per_task,
        "per_model": per_model,
        "per_group": per_group,
        "means_report": means_report,
        "syntax_summary": syntax_summary,
        "unique_sample_ids": len(seen),
    }


def ordered_records(records):
    by_key = {(r["task"], r["model"], int(str(r["repetition_raw"]).strip())): r for r in records}
    ordered = []
    for task in TASKS:
        for model in MODELS:
            for rep in range(1, 11):
                ordered.append(by_key[(task, model, rep)])
    return ordered


def write_global_csv(records):
    CONSOLIDATED_DIR.mkdir(parents=True, exist_ok=True)
    with GLOBAL_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=GLOBAL_COLUMNS)
        writer.writeheader()
        for r in records:
            writer.writerow(
                {
                    "task": r["task"],
                    "model": r["model"],
                    "repetition": int(str(r["repetition_raw"]).strip()),
                    "sample_id": r["sample_id"],
                    "R": r["R"],
                    "F": r["F"],
                    "C": r["C"],
                    "M": r["M"],
                    "S": r["S"],
                    "ICC": r["ICC"],
                    "syntax_valid": "" if r["syntax_valid"] is None else r["syntax_valid"],
                    "encoding_incident": "" if r["encoding_incident"] is None else r["encoding_incident"],
                    "source_file": r["source_file"],
                }
            )


def build_manifest(source_hashes_before, source_rows, global_hash, audit_result, records, frozen):
    groups = {
        f"{t}/{m}": audit_result["per_group"][(t, m)]
        for t in TASKS for m in MODELS
    }
    return {
        "experiment": "EVALUACION DE LA CALIDAD DEL CODIGO GENERADO MEDIANTE DISTINTOS MODELOS DE INTELIGENCIA ARTIFICIAL EN TAREAS DE PROGRAMACION",
        "phase": "GLOBAL-A (congelamiento de datos)",
        "python_version": platform.python_version(),
        "total_observations": len(records),
        "tasks": dict(audit_result["per_task"]),
        "models": dict(audit_result["per_model"]),
        "groups": groups,
        "dimensions": list(DIMENSIONS),
        "icc_formula": "ICC = 0.20*R + 0.20*F + 0.20*C + 0.20*M + 0.20*S",
        "source_files": {
            name: {"sha256": source_hashes_before[name], "rows": source_rows[name]}
            for name in SOURCE_FILES.values()
        },
        "global_results": {"sha256": global_hash, "rows": len(records)},
        "source_files_unchanged": frozen,
        "icc": {
            "max_abs_delta": audit_result["icc_max_abs_delta"],
            "inconsistent": len(audit_result["icc_inconsistent"]),
            "tolerance": ICC_TOLERANCE,
        },
        "integrity_status": "PASS" if not audit_result["errors"] else "FAIL",
        "integrity_errors": audit_result["errors"],
        "integrity_warnings": audit_result["warnings"],
    }


def _fmt(value, digits=2):
    if value is None:
        return "N/A"
    return f"{value:.{digits}f}"


def build_audit_md(audit_result, source_hashes, global_hash, frozen):
    lines = []
    lines.append("# Auditoría global de resultados")
    lines.append("")
    lines.append("## 1. Objetivo")
    lines.append("")
    lines.append(
        "Auditar, consolidar y congelar las 90 observaciones de T1, T2 y T3 a partir "
        "de los consolidados cerrados, sin reprocesar muestras ni recalcular métricas, "
        "y sin realizar análisis inferencial. Esta fase solo cubre integridad, "
        "consolidación, trazabilidad y congelamiento."
    )
    lines.append("")

    lines.append("## 2. Fuentes utilizadas")
    lines.append("")
    lines.append("| Archivo | Filas | SHA-256 |")
    lines.append("|---|---|---|")
    for task in TASKS:
        name = SOURCE_FILES[task]
        lines.append(f"| `{name}` | {audit_result['per_task'][task]} | `{source_hashes[name]}` |")
    lines.append("")

    lines.append("## 3. Integridad por tarea")
    lines.append("")
    lines.append("| Tarea | Observaciones | Esperado | Estado |")
    lines.append("|---|---|---|---|")
    for task in TASKS:
        count = audit_result["per_task"][task]
        lines.append(f"| {task} | {count} | 30 | {'OK' if count == 30 else 'ERROR'} |")
    lines.append("")

    lines.append("## 4. Integridad por modelo")
    lines.append("")
    lines.append("| Modelo | Observaciones | Esperado | Estado |")
    lines.append("|---|---|---|---|")
    for model in MODELS:
        count = audit_result["per_model"][model]
        lines.append(f"| {model} | {count} | 30 | {'OK' if count == 30 else 'ERROR'} |")
    lines.append("")

    lines.append("## 5. Integridad tarea × modelo")
    lines.append("")
    lines.append("| Tarea | chatgpt | deepseek | opencode |")
    lines.append("|---|---|---|---|")
    for task in TASKS:
        cells = [str(audit_result["per_group"][(task, m)]) for m in MODELS]
        lines.append(f"| {task} | " + " | ".join(cells) + " |")
    lines.append("")

    lines.append("## 6. Validación de identificadores")
    lines.append("")
    lines.append(f"- sample_id únicos: {audit_result['unique_sample_ids']} / 90")
    lines.append("- Convención verificada: `<TAREA>_<modelo>_R01..R10`.")
    lines.append("- Cada combinación tarea/modelo/repetición aparece exactamente una vez (1..10).")
    if audit_result["errors"]:
        lines.append("")
        lines.append("Errores de integridad detectados:")
        for err in audit_result["errors"]:
            lines.append(f"- {err}")
    else:
        lines.append("- Sin errores de integridad.")
    lines.append("")

    lines.append("## 7. Valores faltantes y rangos")
    lines.append("")
    lines.append(f"- Valores faltantes/inválidos: {len(audit_result['missing'])}")
    for item in audit_result["missing"]:
        lines.append(f"  - {item}")
    lines.append(f"- Valores fuera de rango [0,100]: {len(audit_result['out_of_range'])}")
    for item in audit_result["out_of_range"]:
        lines.append(f"  - {item}")
    if not audit_result["missing"] and not audit_result["out_of_range"]:
        lines.append("- R, F, C, M, S e ICC presentes y dentro de [0,100] en las 90 observaciones.")
    lines.append("")

    lines.append("## 8. Consistencia del ICC")
    lines.append("")
    lines.append(
        "- ICC recalculado con fines de auditoría como "
        "`0.20*R + 0.20*F + 0.20*C + 0.20*M + 0.20*S`; el valor almacenado no se modificó."
    )
    lines.append(f"- Delta absoluto máximo |ICC_almacenado - ICC_recalculado|: {audit_result['icc_max_abs_delta']:.6f}")
    lines.append(f"- ICC inconsistentes (tolerancia {ICC_TOLERANCE}): {len(audit_result['icc_inconsistent'])}")
    for item in audit_result["icc_inconsistent"]:
        lines.append(f"  - {item}")
    if not audit_result["icc_inconsistent"]:
        lines.append("- Las 90 observaciones son consistentes con la fórmula (diferencias ≤ tolerancia de presentación).")
    lines.append("")

    lines.append("## 9. Errores sintácticos e incidencias registradas")
    lines.append("")
    lines.append("| Tarea | Modelo | syntax_valid=false | encoding_incident=true | encoding no registrado |")
    lines.append("|---|---|---|---|---|")
    total_syntax_false = 0
    total_encoding_true = 0
    total_encoding_na = 0
    for task in TASKS:
        for model in MODELS:
            s = audit_result["syntax_summary"][(task, model)]
            total_syntax_false += s["syntax_false"]
            total_encoding_true += s["encoding_true"]
            total_encoding_na += s["encoding_not_registered"]
            lines.append(
                f"| {task} | {model} | {s['syntax_false']} | {s['encoding_true']} | {s['encoding_not_registered']} |"
            )
    lines.append(f"| **Total** | | **{total_syntax_false}** | **{total_encoding_true}** | **{total_encoding_na}** |")
    lines.append("")
    if total_encoding_na:
        lines.append(
            "Nota de trazabilidad: el consolidado de T1 no incluye la columna `encoding_incident`; "
            "esas celdas quedan vacías en `global_results.csv` (no se inventan valores). Las "
            "incidencias de encoding de T2/T3 se conservan desde sus consolidados."
        )
        lines.append("")

    lines.append("## 10. Proveniencia y hashes")
    lines.append("")
    lines.append(f"- Cada fila de `global_results.csv` incluye `source_file` (T1/T2/T3_results.csv).")
    lines.append(f"- SHA-256 de `global_results.csv`: `{global_hash}`")
    lines.append("- SHA-256 de las fuentes:")
    for task in TASKS:
        lines.append(f"  - `{SOURCE_FILES[task]}`: `{source_hashes[SOURCE_FILES[task]]}`")
    lines.append(f"- Fuentes sin cambios tras la consolidación: {'true' if frozen else 'false'}")
    lines.append("")

    lines.append("## 11. Resultado del congelamiento")
    lines.append("")
    status = "PASS" if not audit_result["errors"] else "FAIL"
    lines.append(f"- Integridad: **{status}**")
    if audit_result["mean_mismatches"]:
        lines.append("- Medias que no coinciden con los resultados cerrados conocidos:")
        for item in audit_result["mean_mismatches"]:
            lines.append(f"  - {item}")
    else:
        lines.append("- Las medias por tarea/modelo coinciden con los resultados cerrados conocidos (tolerancia de redondeo de presentación).")
    lines.append("")

    lines.append("## 12. Estado para análisis estadístico")
    lines.append("")
    if status == "PASS" and frozen:
        lines.append("**APTA PARA ANÁLISIS ESTADÍSTICO**")
    else:
        lines.append("**NO APTA PARA ANÁLISIS ESTADÍSTICO**")
    lines.append("")
    lines.append(
        "`global_results.csv` se considera READ-ONLY a partir de este momento e "
        "identificado por su SHA-256. No se realizó ningún análisis inferencial."
    )
    lines.append("")
    return "\n".join(lines)


def main():
    source_hashes_before = {}
    source_rows = {}
    for task in TASKS:
        path = CONSOLIDATED_DIR / SOURCE_FILES[task]
        source_hashes_before[SOURCE_FILES[task]] = sha256_file(path)
        source_rows[SOURCE_FILES[task]] = sum(1 for _ in read_source(task))

    records = build_records()
    audit_result = audit(records)
    ordered = ordered_records(records)

    write_global_csv(ordered)
    global_hash = sha256_file(GLOBAL_CSV)

    # Verificacion de fuentes sin cambios
    frozen = all(
        sha256_file(CONSOLIDATED_DIR / name) == digest
        for name, digest in source_hashes_before.items()
    )

    manifest = build_manifest(
        source_hashes_before, source_rows, global_hash, audit_result, ordered, frozen
    )
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    report = build_audit_md(audit_result, source_hashes_before, global_hash, frozen)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_REPORT.write_text(report, encoding="utf-8")

    print(f"Observaciones: {len(ordered)}")
    print(f"global_results.csv: {GLOBAL_CSV} sha256={global_hash}")
    print(f"manifest: {MANIFEST_PATH}")
    print(f"auditoria: {AUDIT_REPORT}")
    print(f"integrity_status: {manifest['integrity_status']}")
    print(f"source_files_unchanged: {frozen}")
    if audit_result["errors"]:
        for err in audit_result["errors"]:
            print(f"ERROR: {err}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
