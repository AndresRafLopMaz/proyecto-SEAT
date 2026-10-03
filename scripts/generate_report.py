"""Genera un resumen descriptivo para el informe academico.

ESTADO: esqueleto documentado. Los resultados consolidados aun no existen
porque el experimento oficial (90 muestras) todavia no se ha ejecutado.

Alcance actual (implementable sin dependencias extra, usando `statistics`):
- media, mediana, desviacion estandar, minimo, maximo y rango intercuartilico.

Pendiente para la fase de analisis (NO implementado aqui):
- cargar results/consolidated/*.json;
- agregar por sistema, por tarea y global;
- estadistica inferencial (tests de normalidad, comparacion de grupos,
  tamanos de efecto), que requeriria dependencias adicionales no instaladas.

Regla: las interpretaciones deben derivarse de resultados reales. Este script
no genera ni inventa valores.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DIMENSIONS = ("R", "F", "C", "M", "S", "ICC")
CONSOLIDATED_DIR = PROJECT_ROOT / "results" / "consolidated"


def describe(values):
    """Estadistica descriptiva basica de una secuencia numerica."""
    clean = [float(value) for value in values if value is not None]
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
    summary["iqr"] = _interquartile_range(clean)
    return summary


def _interquartile_range(values):
    ordered = sorted(values)
    if len(ordered) < 2:
        return 0.0
    quartiles = statistics.quantiles(ordered, n=4, method="inclusive")
    return quartiles[2] - quartiles[0]


def load_consolidated_results():
    """Carga los resultados consolidados si existen."""
    if not CONSOLIDATED_DIR.is_dir():
        return []
    results = []
    for path in sorted(CONSOLIDATED_DIR.glob("*.json")):
        results.append(json.loads(path.read_text(encoding="utf-8")))
    return results


def load_raw_results():
    raw_dir = PROJECT_ROOT / "results" / "raw"
    if not raw_dir.is_dir():
        return []
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(raw_dir.glob("*.json"))
    ]


def summarize(results):
    """Resumen descriptivo por dimension para una lista de resultados."""
    summary = {}
    for dimension in DIMENSIONS:
        values = [result.get(dimension) for result in results]
        summary[dimension] = describe(values)
    return summary


def _parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Genera resumen descriptivo.")
    parser.add_argument(
        "--source",
        choices=("consolidated", "raw"),
        default="consolidated",
        help="Conjunto de resultados a resumir",
    )
    parser.add_argument("--output", default=None, help="Ruta JSON de salida")
    return parser.parse_args(argv)


def main(argv=None):
    args = _parse_args(argv)
    results = (
        load_consolidated_results()
        if args.source == "consolidated"
        else load_raw_results()
    )

    if not results:
        print("No hay resultados disponibles todavia.")
        print(f"Origen: {args.source}. El experimento oficial aun no se ejecuta.")
        print("No se genera ningun resumen con valores inventados.")
        return 0

    summary = summarize(results)
    output = Path(args.output) if args.output else PROJECT_ROOT / "results" / "reports" / "summary.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"\nResumen escrito en: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
