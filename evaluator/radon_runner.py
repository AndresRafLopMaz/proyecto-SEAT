"""Wrapper para ejecutar Radon (complejidad ciclomatica e indice de mantenibilidad).

Ejecuta `sys.executable -m radon ...` para no depender de una instalacion
global. Registra comando, exit code, stdout, stderr, estado y error.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

TOOL = "radon"


def _result(command, exit_code, stdout, stderr, status, error=None):
    return {
        "tool": TOOL,
        "command": command,
        "exit_code": exit_code,
        "stdout": stdout,
        "stderr": stderr,
        "status": status,
        "error": error,
    }


def _run(command, timeout):
    try:
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        return None, _result(
            command,
            None,
            _decode(exc.stdout),
            _decode(exc.stderr),
            "timeout",
            f"radon excedio el tiempo limite de {timeout}s",
        )
    except (OSError, ValueError) as exc:
        return None, _result(
            command,
            None,
            "",
            "",
            "error",
            f"{type(exc).__name__}: {exc}",
        )

    if process.returncode == 0:
        status = "ok"
        error = None
    else:
        status = "error"
        error = f"radon termino con codigo {process.returncode}"

    return process, _result(
        command,
        process.returncode,
        process.stdout,
        process.stderr,
        status,
        error,
    )


def run_radon_cc(target, timeout=300):
    """Complejidad ciclomatica por bloque (JSON) y sus agregados."""
    command = [sys.executable, "-m", "radon", "cc", str(target), "-j"]
    process, result = _run(command, timeout)
    if process is None:
        return result

    data, parse_error = _load_json(process.stdout)
    if parse_error is not None:
        result["status"] = "error"
        result["error"] = parse_error
        result["average_complexity"] = None
        result["max_complexity"] = None
        result["blocks"] = None
        return result

    if not data:
        result["status"] = "error"
        result["error"] = "radon no analizo ningun archivo (ruta inexistente?)"
        result["average_complexity"] = None
        result["max_complexity"] = None
        result["blocks"] = None
        return result

    complexities = []
    blocks = 0
    for entries in data.values():
        for entry in _iter_entries(entries):
            if isinstance(entry, dict) and "complexity" in entry:
                complexities.append(entry["complexity"])
                blocks += 1

    result["blocks"] = blocks
    result["average_complexity"] = (
        sum(complexities) / len(complexities) if complexities else None
    )
    result["max_complexity"] = max(complexities) if complexities else None
    return result


def run_radon_mi(target, timeout=300):
    """Indice de Mantenibilidad por bloque (JSON) y su promedio."""
    command = [sys.executable, "-m", "radon", "mi", str(target), "-j"]
    process, result = _run(command, timeout)
    if process is None:
        return result

    data, parse_error = _load_json(process.stdout)
    if parse_error is not None:
        result["status"] = "error"
        result["error"] = parse_error
        result["maintainability_index"] = None
        return result

    if not data:
        result["status"] = "error"
        result["error"] = "radon no analizo ningun archivo (ruta inexistente?)"
        result["maintainability_index"] = None
        return result

    values = []
    for entries in data.values():
        for entry in _iter_entries(entries):
            if isinstance(entry, dict) and "mi" in entry:
                values.append(entry["mi"])

    result["maintainability_index"] = (
        round(sum(values) / len(values), 2) if values else None
    )
    return result


def run_radon(target, timeout=300):
    """Ejecuta ambas analisis de Radon y los resume en un unico resultado.

    Los campos de registro de nivel superior (command, exit_code, stdout,
    stderr, error) reflejan la ejecucion de `cc`; el detalle completo de cada
    analisis queda en `cc` y `mi`.
    """
    cc = run_radon_cc(target, timeout=timeout)
    mi = run_radon_mi(target, timeout=timeout)

    if cc["status"] == "ok" and mi["status"] == "ok":
        status = "ok"
    elif cc["status"] == "timeout" or mi["status"] == "timeout":
        status = "timeout"
    else:
        status = "error"

    return {
        "tool": TOOL,
        "status": status,
        "average_complexity": cc.get("average_complexity"),
        "max_complexity": cc.get("max_complexity"),
        "maintainability_index": mi.get("maintainability_index"),
        "command": cc.get("command"),
        "exit_code": cc.get("exit_code"),
        "stdout": cc.get("stdout"),
        "stderr": cc.get("stderr"),
        "error": cc.get("error") or mi.get("error"),
        "cc": cc,
        "mi": mi,
    }


def _load_json(stdout):
    if not stdout or not stdout.strip():
        return {}, "radon no produjo salida JSON"
    try:
        return json.loads(stdout), None
    except json.JSONDecodeError as exc:
        return {}, f"JSON invalido de radon: {exc}"


def _iter_entries(entries):
    """Normaliza la estructura JSON de Radon (dict o lista) a una lista."""
    if isinstance(entries, dict):
        return [entries]
    if isinstance(entries, list):
        return entries
    return []


def _decode(value):
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value
