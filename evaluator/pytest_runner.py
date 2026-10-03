"""Wrapper para ejecutar pytest usando el interprete del entorno virtual.

Ejecuta `sys.executable -m pytest` para no depender de que pytest este
instalado globalmente. Registra el comando, el exit code, stdout, stderr, el
estado y un posible error de herramienta. Un fallo de las pruebas del codigo
evaluado es un resultado experimental; un fallo de pytest es una incidencia.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

TOOL = "pytest"

# Variable de entorno que tasks/T1/tests/test_t1.py usa para cargar la muestra.
SAMPLE_ENV_VAR = "SEAT_SAMPLE_PATH"

_SUMMARY_PATTERNS = {
    "passed": re.compile(r"(\d+)\s+passed"),
    "failed": re.compile(r"(\d+)\s+failed"),
    "errors": re.compile(r"(\d+)\s+error"),
    "skipped": re.compile(r"(\d+)\s+skipped"),
    "xfailed": re.compile(r"(\d+)\s+xfailed"),
    "xpassed": re.compile(r"(\d+)\s+xpassed"),
}


def parse_pytest_summary(stdout):
    """Extrae los contadores del resumen de pytest a partir de la salida."""
    summary = {key: 0 for key in _SUMMARY_PATTERNS}
    if not stdout:
        return summary
    for key, pattern in _SUMMARY_PATTERNS.items():
        match = pattern.search(stdout)
        if match:
            summary[key] = int(match.group(1))
    return summary


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


def run_pytest(
    target,
    extra_args=None,
    timeout=600,
    cwd=None,
    sample_path=None,
    capture_cases=False,
    env=None,
):
    """Ejecuta pytest sobre `target` y devuelve un resultado estructurado.

    Parametros opcionales de integracion:
    - `sample_path`: ruta de la muestra a evaluar. Si se indica, se define
      `SEAT_SAMPLE_PATH` (ruta absoluta) unicamente en el entorno del proceso
      de pytest, sin alterar el entorno global.
    - `capture_cases`: si es True, solicita un reporte JUnit XML temporal para
      obtener el resultado individual de cada caso en `result["cases"]`.
    - `env`: variables de entorno adicionales para el proceso de pytest.
    """
    command = [sys.executable, "-m", "pytest", str(target), "-q"]
    if extra_args:
        command.extend(str(arg) for arg in extra_args)

    run_env = dict(os.environ)
    if env:
        run_env.update({key: str(value) for key, value in env.items()})
    if sample_path is not None:
        run_env[SAMPLE_ENV_VAR] = str(Path(sample_path).resolve())
        # Evita escribir __pycache__ dentro de las carpetas de muestras.
        run_env["PYTHONDONTWRITEBYTECODE"] = "1"

    junit_file = None
    exec_command = list(command)
    if capture_cases:
        handle, junit_file = tempfile.mkstemp(prefix="seat_pytest_", suffix=".xml")
        os.close(handle)
        exec_command.append(f"--junit-xml={junit_file}")

    try:
        process = subprocess.run(
            exec_command,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd,
            env=run_env,
        )
    except subprocess.TimeoutExpired as exc:
        _remove_file(junit_file)
        return _result(
            command,
            None,
            _decode(exc.stdout),
            _decode(exc.stderr),
            "timeout",
            f"pytest excedio el tiempo limite de {timeout}s",
        )
    except (OSError, ValueError) as exc:
        _remove_file(junit_file)
        return _result(
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
    elif process.returncode == 1:
        status = "failed"
        error = None
    else:
        status = "error"
        error = f"pytest termino con codigo {process.returncode}"

    result = _result(
        command,
        process.returncode,
        process.stdout,
        process.stderr,
        status,
        error,
    )
    result["summary"] = parse_pytest_summary(process.stdout)

    if capture_cases:
        result["cases"] = parse_junit_cases(junit_file)
        _remove_file(junit_file)

    return result


def parse_junit_cases(junit_path):
    """Devuelve {nombre_de_test: 'pass'|'fail'|'error'|'skipped'} desde JUnit XML."""
    if not junit_path or not Path(junit_path).is_file():
        return {}
    try:
        root = ET.parse(junit_path).getroot()
    except ET.ParseError:
        return {}

    cases = {}
    for testcase in root.iter("testcase"):
        name = testcase.get("name")
        if not name:
            continue
        if testcase.find("failure") is not None:
            status = "fail"
        elif testcase.find("error") is not None:
            status = "error"
        elif testcase.find("skipped") is not None:
            status = "skipped"
        else:
            status = "pass"
        cases[name] = status
    return cases


def _remove_file(path):
    if path and Path(path).exists():
        try:
            Path(path).unlink()
        except OSError:
            pass


def _decode(value):
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value
