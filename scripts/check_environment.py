"""Verificacion del entorno tecnico del instrumento de investigacion.

Comprueba version/ubicacion de Python, herramientas instaladas, estructura de
carpetas, archivos principales e importabilidad del paquete `evaluator`.

Uso:
    .venv\\Scripts\\python.exe scripts\\check_environment.py

Salida simple con estado OK/FAIL y veredicto final READY / NOT READY.
"""

from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

EXPECTED_DIRECTORIES = (
    "config",
    "tasks/T1/tests",
    "tasks/T2/tests",
    "tasks/T3/tests",
    "samples/chatgpt/T1",
    "samples/chatgpt/T2",
    "samples/chatgpt/T3",
    "samples/deepseek/T1",
    "samples/deepseek/T2",
    "samples/deepseek/T3",
    "samples/opencode/T1",
    "samples/opencode/T2",
    "samples/opencode/T3",
    "evaluator",
    "results/raw",
    "results/consolidated",
    "results/reports",
    "incidents",
    "scripts",
    "tests/test_evaluator",
)

EXPECTED_FILES = (
    "README.md",
    "requirements.txt",
    "requirements-lock.txt",
    ".gitignore",
    "config/experiment.json",
    "tasks/T1/requirements.json",
    "tasks/T2/requirements.json",
    "tasks/T3/requirements.json",
    "evaluator/__init__.py",
    "evaluator/scoring.py",
    "evaluator/syntax_checker.py",
    "evaluator/requirements_checker.py",
    "evaluator/pytest_runner.py",
    "evaluator/radon_runner.py",
    "evaluator/bandit_runner.py",
    "evaluator/evaluator.py",
    "scripts/check_environment.py",
    "scripts/evaluate_sample.py",
    "scripts/evaluate_all.py",
    "scripts/generate_report.py",
)

TOOLS = (
    ("pytest", "pytest", ["--version"]),
    ("radon", "radon", ["--version"]),
    ("bandit", "bandit", ["--version"]),
)

EVALUATOR_MODULES = (
    "evaluator",
    "evaluator.scoring",
    "evaluator.syntax_checker",
    "evaluator.requirements_checker",
    "evaluator.pytest_runner",
    "evaluator.radon_runner",
    "evaluator.bandit_runner",
    "evaluator.evaluator",
)


def _line(label, ok, detail=""):
    state = "OK" if ok else "FAIL"
    text = f"{label:<26} {state}"
    if detail:
        text += f"  {detail}"
    print(text)
    return ok


def check_python():
    version = ".".join(str(part) for part in sys.version_info[:3])
    ok = sys.version_info[:2] == (3, 12)
    _line("Python 3.12.x", ok, f"{version} -> {sys.executable}")
    return ok


def check_tools():
    all_ok = True
    for display, module, args in TOOLS:
        try:
            process = subprocess.run(
                [sys.executable, "-m", module, *args],
                capture_output=True,
                text=True,
                timeout=60,
            )
            first_line = (process.stdout or process.stderr).strip().splitlines()
            detail = first_line[0] if first_line else ""
            all_ok &= _line(display, process.returncode == 0, detail)
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            all_ok &= _line(display, False, f"{type(exc).__name__}: {exc}")
    return all_ok


def check_structure():
    missing_dirs = [
        path for path in EXPECTED_DIRECTORIES if not (PROJECT_ROOT / path).is_dir()
    ]
    missing_files = [
        path for path in EXPECTED_FILES if not (PROJECT_ROOT / path).is_file()
    ]
    ok = not missing_dirs and not missing_files
    detail = ""
    if missing_dirs:
        detail += f"faltan dirs: {', '.join(missing_dirs)}; "
    if missing_files:
        detail += f"faltan archivos: {', '.join(missing_files)}"
    return _line("Project structure", ok, detail)


def check_imports():
    all_ok = True
    for module_name in EVALUATOR_MODULES:
        try:
            importlib.import_module(module_name)
            all_ok &= _line(f"import {module_name}", True)
        except Exception as exc:  # noqa: BLE001 - reportar cualquier fallo de import
            all_ok &= _line(f"import {module_name}", False, f"{type(exc).__name__}: {exc}")
    return all_ok


def check_scoring():
    try:
        from evaluator import scoring

        checks = [
            scoring.calculate_requirements_score(5, 5) == 100.0,
            scoring.calculate_functional_score(10, 10) == 100.0,
            scoring.calculate_complexity_score(1) == 100.0,
            scoring.calculate_complexity_score(41) == 0.0,
            scoring.calculate_security_score(0, 0, 0) == 100.0,
            scoring.calculate_icc(100, 100, 100, 100, 100) == 100.0,
        ]
        return _line("scoring.py", all(checks), "formulas verificadas")
    except Exception as exc:  # noqa: BLE001
        return _line("scoring.py", False, f"{type(exc).__name__}: {exc}")


def check_syntax_checker():
    try:
        from evaluator.syntax_checker import check_syntax

        target = PROJECT_ROOT / "evaluator" / "scoring.py"
        result = check_syntax(target)
        return _line(
            "syntax_checker.py",
            result.valid and result.status == "valid",
            f"analizado {target.name}",
        )
    except Exception as exc:  # noqa: BLE001
        return _line("syntax_checker.py", False, f"{type(exc).__name__}: {exc}")


def check_wrappers():
    try:
        from evaluator import bandit_runner, pytest_runner, radon_runner

        results = []
        target = PROJECT_ROOT / "evaluator" / "scoring.py"
        radon_result = radon_runner.run_radon(target)
        results.append(radon_result["status"] == "ok")
        bandit_result = bandit_runner.run_bandit(target)
        results.append(bandit_result["status"] in ("clean", "issues_found"))
        required_keys = {"command", "exit_code", "stdout", "stderr", "status", "error"}
        results.append(required_keys.issubset(radon_result.keys()))
        results.append(required_keys.issubset(bandit_result.keys()))
        results.append(callable(pytest_runner.run_pytest))
        return _line(
            "tool wrappers",
            all(results),
            "radon/bandit ejecutados y salida capturada",
        )
    except Exception as exc:  # noqa: BLE001
        return _line("tool wrappers", False, f"{type(exc).__name__}: {exc}")


def main():
    print("=" * 64)
    print("CHECK ENVIRONMENT - proyecto-SEAT")
    print(f"Proyecto: {PROJECT_ROOT}")
    print("=" * 64)

    checks = [
        check_python(),
        check_tools(),
        check_structure(),
        check_imports(),
        check_scoring(),
        check_syntax_checker(),
        check_wrappers(),
    ]

    print("-" * 64)
    ready = all(checks)
    print(f"Environment: {'READY' if ready else 'NOT READY'}")
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
