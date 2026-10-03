"""Comprobacion estatica de restricciones externas para el instrumento T3 (R5).

Analiza el AST/fuente de una muestra de T3 y detecta unicamente usos
inequivocos de mecanismos prohibidos por `tasks/T3/prompt.md`:

- entrada interactiva: input(), breakpoint();
- archivos: open(), io.open(), metodos .open/.read_text/.write_text/
  .read_bytes/.write_bytes;
- comandos externos: os.system/os.popen/os.spawn*/os.exec*/os.fork,
  subprocess.*;
- red: socket.*, urllib.*, http.*, ftplib.*, smtplib.*, poplib.*, imaplib.*,
  telnetlib.*, xmlrpc.*, requests.*;
- biblioteca no estandar: imports cuyo modulo raiz no pertenece a
  `sys.stdlib_module_names`.

NO penaliza eval, exec, ast, tokenize, operator, re, math ni otros modulos de
la biblioteca estandar que no impliquen por si mismos una operacion prohibida.
La auditoria de seguridad estatica (Bandit) corresponde a la fase T3-B.

La comprobacion esta pensada para ejecutarse sobre la representacion que
realmente se evalua (UTF-8). Es reutilizable por el orquestador de T3-B.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

# Categorias
ENTRADA = "entrada_interactiva"
ARCHIVOS = "archivos"
COMANDOS = "comandos_externos"
RED = "red"
NO_ESTANDAR = "biblioteca_no_estandar"

_PROHIBITED_NAME_CALLS = {
    "input": (ENTRADA, "input()"),
    "breakpoint": (ENTRADA, "breakpoint()"),
    "open": (ARCHIVOS, "open()"),
}

_FILE_METHODS = {"open", "read_text", "write_text", "read_bytes", "write_bytes"}

NET_PREFIXES = (
    "socket.",
    "urllib.",
    "http.",
    "ftplib.",
    "smtplib.",
    "poplib.",
    "imaplib.",
    "telnetlib.",
    "xmlrpc.",
    "requests.",
)

_OS_EXEC_MEMBERS = {
    "system",
    "popen",
    "fork",
    "forkpty",
    "spawnl",
    "spawnle",
    "spawnlp",
    "spawnlpe",
    "spawnv",
    "spawnve",
    "spawnvp",
    "spawnvpe",
    "execv",
    "execve",
    "execvp",
    "execvpe",
    "execl",
    "execle",
    "execlp",
    "execlpe",
}

_STDLIB_EXTRA_ALLOWED = {"__future__"}


def _dotted_name(node):
    """Devuelve el nombre punteado de un ast.Attribute/Name, o None."""
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return ".".join(reversed(parts))
    return None


def _is_stdlib(module_name):
    if not module_name:
        return True
    if module_name in _STDLIB_EXTRA_ALLOWED:
        return True
    return module_name in sys.stdlib_module_names


def check_source(source, filename="<muestra>"):
    """Comprueba restricciones sobre una cadena de codigo fuente."""
    violations = []
    imports = []
    non_stdlib = []

    try:
        tree = ast.parse(source, filename=str(filename))
    except SyntaxError as exc:
        return {
            "passed": False,
            "syntax_error": True,
            "violations": [
                {
                    "category": "sintaxis",
                    "detail": f"no se pudo analizar el AST: {exc}",
                    "lineno": exc.lineno,
                }
            ],
            "imports": [],
            "non_stdlib_imports": [],
        }

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                entry = _PROHIBITED_NAME_CALLS.get(func.id)
                if entry is not None:
                    violations.append(
                        {
                            "category": entry[0],
                            "detail": entry[1],
                            "lineno": getattr(node, "lineno", None),
                        }
                    )
            elif isinstance(func, ast.Attribute):
                dotted = _dotted_name(func)
                attr = func.attr
                if dotted == "io.open":
                    violations.append(
                        {"category": ARCHIVOS, "detail": "io.open()", "lineno": getattr(node, "lineno", None)}
                    )
                elif dotted and any(dotted.startswith(p) for p in NET_PREFIXES):
                    violations.append(
                        {"category": RED, "detail": f"{dotted}()", "lineno": getattr(node, "lineno", None)}
                    )
                elif dotted and dotted.startswith("subprocess."):
                    violations.append(
                        {"category": COMANDOS, "detail": f"{dotted}()", "lineno": getattr(node, "lineno", None)}
                    )
                elif dotted and dotted.startswith("os.") and attr in _OS_EXEC_MEMBERS:
                    violations.append(
                        {"category": COMANDOS, "detail": f"{dotted}()", "lineno": getattr(node, "lineno", None)}
                    )
                elif attr in _FILE_METHODS:
                    violations.append(
                        {"category": ARCHIVOS, "detail": f".{attr}()", "lineno": getattr(node, "lineno", None)}
                    )

        elif isinstance(node, ast.Import):
            for alias in node.names:
                top = alias.name.split(".")[0]
                imports.append(alias.name)
                if not _is_stdlib(top):
                    non_stdlib.append(alias.name)
                    violations.append(
                        {
                            "category": NO_ESTANDAR,
                            "detail": f"import {alias.name}",
                            "lineno": getattr(node, "lineno", None),
                        }
                    )

        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                continue
            module = node.module or ""
            top = module.split(".")[0]
            if module:
                imports.append(module)
            if module and not _is_stdlib(top):
                non_stdlib.append(module)
                violations.append(
                    {
                        "category": NO_ESTANDAR,
                        "detail": f"from {module} import ...",
                        "lineno": getattr(node, "lineno", None),
                    }
                )

    return {
        "passed": not violations,
        "syntax_error": False,
        "violations": violations,
        "imports": sorted(set(imports)),
        "non_stdlib_imports": sorted(set(non_stdlib)),
    }


def check_external_restrictions(sample_path):
    """Comprueba restricciones sobre un archivo de muestra (UTF-8)."""
    path = Path(sample_path)
    try:
        source = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return {
            "passed": False,
            "syntax_error": False,
            "violations": [
                {
                    "category": "lectura",
                    "detail": f"no se pudo leer la muestra: {type(exc).__name__}: {exc}",
                    "lineno": None,
                }
            ],
            "imports": [],
            "non_stdlib_imports": [],
        }
    return check_source(source, filename=str(path))
