"""Comprobador de validez sintactica de archivos Python.

Utiliza `ast.parse` para analizar el codigo sin ejecutarlo y sin modificar
nunca el archivo analizado. Distingue al menos cuatro estados:

    valid          -> el codigo es sintacticamente valido
    syntax_error   -> el codigo presenta un error de sintaxis
    file_not_found -> la ruta no existe
    read_error     -> el archivo existe pero no se pudo leer
"""

from __future__ import annotations

import ast
from dataclasses import asdict, dataclass
from pathlib import Path

VALID = "valid"
SYNTAX_ERROR = "syntax_error"
FILE_NOT_FOUND = "file_not_found"
READ_ERROR = "read_error"


@dataclass
class SyntaxCheckResult:
    """Resultado estructurado y serializable de la comprobacion."""

    path: str
    status: str
    valid: bool
    exists: bool
    error_type: str | None = None
    message: str | None = None
    line: int | None = None
    column: int | None = None

    def to_dict(self):
        return asdict(self)


def check_syntax(file_path):
    """Comprueba la sintaxis de `file_path` y devuelve un SyntaxCheckResult."""
    path = Path(file_path)

    if not path.exists():
        return SyntaxCheckResult(
            path=str(path),
            status=FILE_NOT_FOUND,
            valid=False,
            exists=False,
            error_type="FileNotFoundError",
            message=f"El archivo no existe: {path}",
        )

    if not path.is_file():
        return SyntaxCheckResult(
            path=str(path),
            status=READ_ERROR,
            valid=False,
            exists=True,
            error_type="IsADirectoryError",
            message=f"La ruta no es un archivo regular: {path}",
        )

    try:
        source = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError) as exc:
        return SyntaxCheckResult(
            path=str(path),
            status=READ_ERROR,
            valid=False,
            exists=True,
            error_type=type(exc).__name__,
            message=str(exc),
        )

    try:
        ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        return SyntaxCheckResult(
            path=str(path),
            status=SYNTAX_ERROR,
            valid=False,
            exists=True,
            error_type="SyntaxError",
            message=exc.msg,
            line=exc.lineno,
            column=exc.offset,
        )

    return SyntaxCheckResult(
        path=str(path),
        status=VALID,
        valid=True,
        exists=True,
    )
