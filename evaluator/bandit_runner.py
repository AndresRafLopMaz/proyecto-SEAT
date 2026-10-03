"""Wrapper para ejecutar Bandit (analisis estatico de seguridad).

Ejecuta `sys.executable -m bandit ...` para no depender de una instalacion
global. Cuenta los hallazgos por severidad (baja, media, alta) y conserva la
salida cruda. Registra comando, exit code, stdout, stderr, estado y error.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

TOOL = "bandit"


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


def run_bandit(target, recursive=None, timeout=600):
    """Ejecuta Bandit sobre un archivo o directorio y resume las severidades."""
    path = Path(target)
    if recursive is None:
        recursive = path.is_dir()

    command = [sys.executable, "-m", "bandit", "-f", "json"]
    if recursive:
        command.append("-r")
    command.append(str(target))

    try:
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        return _result(
            command,
            None,
            _decode(exc.stdout),
            _decode(exc.stderr),
            "timeout",
            f"bandit excedio el tiempo limite de {timeout}s",
        )
    except (OSError, ValueError) as exc:
        return _result(
            command,
            None,
            "",
            "",
            "error",
            f"{type(exc).__name__}: {exc}",
        )

    if process.returncode == 0:
        status = "clean"
        error = None
    elif process.returncode == 1:
        status = "issues_found"
        error = None
    else:
        status = "error"
        error = f"bandit termino con codigo {process.returncode}"

    result = _result(
        command,
        process.returncode,
        process.stdout,
        process.stderr,
        status,
        error,
    )

    data, parse_error = _load_json(process.stdout)
    if parse_error is not None:
        result["security_low"] = None
        result["security_medium"] = None
        result["security_high"] = None
        result["total_issues"] = None
        if status != "error":
            result["status"] = "error"
            result["error"] = parse_error
        return result

    errors = data.get("errors") or []
    if errors:
        reasons = "; ".join(
            str(error.get("reason", error)) if isinstance(error, dict) else str(error)
            for error in errors
        )
        result["security_low"] = None
        result["security_medium"] = None
        result["security_high"] = None
        result["total_issues"] = None
        if status != "error":
            result["status"] = "error"
            result["error"] = f"bandit reporto errores: {reasons}"
        return result

    counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
    for issue in data.get("results", []):
        severity = str(issue.get("issue_severity", "")).upper()
        if severity in counts:
            counts[severity] += 1

    result["security_low"] = counts["LOW"]
    result["security_medium"] = counts["MEDIUM"]
    result["security_high"] = counts["HIGH"]
    result["total_issues"] = sum(counts.values())
    return result


def _load_json(stdout):
    if not stdout or not stdout.strip():
        return {}, "bandit no produjo salida JSON"
    try:
        return json.loads(stdout), None
    except json.JSONDecodeError as exc:
        return {}, f"JSON invalido de bandit: {exc}"


def _decode(value):
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value
