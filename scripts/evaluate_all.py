"""Descubre las muestras y orquesta la evaluacion masiva.

ESTADO: esqueleto de infraestructura. Las tareas T1/T2/T3 aun no estan
definidas, por lo que no existe todavia ninguna muestra oficial que evaluar.

Pendiente para la fase experimental:
- cargar los requisitos de cada tarea (tasks/<T>/requirements.json);
- localizar sus pruebas (tasks/<T>/tests);
- decidir la convencion de nombres de las 90 muestras
  (3 sistemas x 3 tareas x 10 repeticiones).

Este script NO inventa datos ni resultados.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SYSTEMS = ("chatgpt", "deepseek", "opencode")
TASKS = ("T1", "T2", "T3")


def discover_samples():
    """Devuelve las muestras .py encontradas por sistema y tarea."""
    found = {}
    for system in SYSTEMS:
        for task in TASKS:
            directory = PROJECT_ROOT / "samples" / system / task
            files = sorted(directory.glob("*.py")) if directory.is_dir() else []
            found[(system, task)] = files
    return found


def main():
    samples = discover_samples()
    total = sum(len(files) for files in samples.values())

    print("Descubrimiento de muestras (fase de preparacion)")
    print("-" * 50)
    print(f"Esperadas (futuro): {len(SYSTEMS)} sistemas x {len(TASKS)} tareas x 10 = 90")
    print(f"Encontradas ahora:  {total}")
    print("-" * 50)
    for (system, task), files in samples.items():
        print(f"{system:<9} {task:<3} {len(files)} archivo(s)")

    if total == 0:
        print("\nNo hay muestras oficiales: las tareas aun no estan definidas.")
        print("No se ejecuta evaluacion. Detenerse aqui.")
        return 0

    print(
        "\nHay archivos .py en samples/. La evaluacion masiva requiere cargar "
        "los requisitos y las pruebas de cada tarea, que todavia no existen."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
