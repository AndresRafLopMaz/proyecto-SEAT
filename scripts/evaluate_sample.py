"""Evalua una unica muestra y guarda su resultado en JSON.

Infraestructura de la fase de preparacion. Las tareas T1/T2/T3 y sus
requisitos/pruebas aun no estan definidos; cuando lo esten, se pasaran con
`--requirements` y `--tests`.

Uso:
    .venv\\Scripts\\python.exe scripts\\evaluate_sample.py ^
        --system chatgpt --task T1 --repetition 1 --code samples\\chatgpt\\T1\\sample.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from evaluator.evaluator import evaluate_sample


def _parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Evalua una muestra individual.")
    parser.add_argument("--system", required=True, help="chatgpt | deepseek | opencode")
    parser.add_argument("--task", required=True, help="Identificador de tarea, p. ej. T1")
    parser.add_argument("--repetition", required=True, type=int, help="Numero de repeticion")
    parser.add_argument("--code", required=True, help="Ruta al archivo Python evaluado")
    parser.add_argument("--tests", default=None, help="Ruta a las pruebas de la tarea")
    parser.add_argument(
        "--requirements",
        nargs="*",
        type=int,
        default=None,
        help="Cinco valores binarios (1/0) de requisitos satisfechos",
    )
    parser.add_argument("--output", default=None, help="Ruta de salida JSON")
    parser.add_argument("--timeout", type=int, default=600)
    return parser.parse_args(argv)


def main(argv=None):
    args = _parse_args(argv)
    sample_id = f"{args.system}_{args.task}_{args.repetition:02d}"

    result = evaluate_sample(
        sample_id=sample_id,
        system=args.system,
        task=args.task,
        repetition=args.repetition,
        code_path=args.code,
        tests_path=args.tests,
        requirements=args.requirements,
        timeout=args.timeout,
    )

    output = (
        Path(args.output)
        if args.output
        else PROJECT_ROOT / "results" / "raw" / f"{sample_id}.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Resultado escrito en: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
