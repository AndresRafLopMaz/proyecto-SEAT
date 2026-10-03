"""Coordinador base del evaluador.

Responsabilidad futura: orquestar la secuencia

    sintaxis -> requisitos -> pytest -> Radon -> Bandit -> scoring -> resultado

En esta fase T1, T2 y T3 aun no estan definidas, por lo que unicamente se
implementa la infraestructura que puede construirse correctamente sin ellas:
plantilla de resultado, evaluacion de sintaxis y ejecucion de herramientas
estaticas. Los requisitos y las pruebas se inyectan como parametros cuando la
tarea exista.

Criterio metodologico:
- un error del codigo evaluado (sintaxis invalida, pruebas fallidas) es un
  resultado experimental;
- un error de la herramienta o del entorno es una incidencia metodologica,
  que se registra en la lista `incidents` del resultado.
"""

from __future__ import annotations

import re

from evaluator import bandit_runner, pytest_runner, radon_runner, scoring
from evaluator.requirements_checker import EXPECTED_REQUIREMENTS, evaluate_requirements
from evaluator.syntax_checker import check_syntax

# Reconoce casos de cualquier tarea: test_t1_c01_... , test_t2_c01_... , etc.
_CASE_NAME_RE = re.compile(r"test_t(\d+)_(c\d{2})(?:_|$)", re.IGNORECASE)

RESULT_TEMPLATE_FIELDS = (
    "sample_id",
    "model",
    "system",
    "task",
    "repetition",
    "syntax_valid",
    "requirements_satisfied",
    "tests_passed",
    "cyclomatic_complexity",
    "max_complexity",
    "maintainability_index",
    "security_low",
    "security_medium",
    "security_high",
    "R",
    "F",
    "C",
    "M",
    "S",
    "ICC",
    "incidents",
)


def create_result_template(sample_id, system, task, repetition):
    """Devuelve la plantilla de resultado con todos los campos en None."""
    return {
        "sample_id": sample_id,
        "model": system,
        "system": system,
        "task": task,
        "repetition": repetition,
        "syntax_valid": None,
        "requirements_satisfied": None,
        "tests_passed": None,
        "cyclomatic_complexity": None,
        "max_complexity": None,
        "maintainability_index": None,
        "security_low": None,
        "security_medium": None,
        "security_high": None,
        "R": None,
        "F": None,
        "C": None,
        "M": None,
        "S": None,
        "ICC": None,
        "cases": {},
        "requirements": {},
        "incidents": [],
    }


def _incident(stage, status, message):
    return {"stage": stage, "status": status, "message": message}


def _case_id_from_test_name(test_name):
    """Mapea 'test_t1_c07_...' -> 'T1-C07' y 'test_t2_c01_...' -> 'T2-C01'.

    Devuelve None si el nombre no corresponde al patron de caso de tarea.
    """
    match = _CASE_NAME_RE.search(test_name or "")
    if not match:
        return None
    return f"T{match.group(1)}-{match.group(2).upper()}"


def collect_case_results(pytest_result):
    """Convierte los casos del reporte JUnit en {case_id: 1|0}."""
    results = {}
    for name, status in (pytest_result.get("cases") or {}).items():
        case_id = _case_id_from_test_name(name)
        if case_id:
            results[case_id] = 1 if status == "pass" else 0
    return results


def derive_requirements(case_results, case_requirement_map):
    """Deriva el cumplimiento 1/0 de cada requisito a partir de sus casos.

    Un requisito se cumple (1) si todos los casos que lo evidencian aprueban.
    """
    detail = {}
    for requirement_id, required_cases in case_requirement_map.items():
        detail[requirement_id] = (
            1 if all(case_results.get(case, 0) == 1 for case in required_cases) else 0
        )
    return detail


def evaluate_syntax(code_path):
    """Comprueba la sintaxis de `code_path`."""
    return check_syntax(code_path)


def evaluate_static(code_path, timeout=300):
    """Ejecuta Radon y Bandit sobre `code_path`."""
    return {
        "radon": radon_runner.run_radon(code_path, timeout=timeout),
        "bandit": bandit_runner.run_bandit(code_path, timeout=timeout),
    }


def evaluate_sample(
    *,
    sample_id,
    system,
    task,
    repetition,
    code_path,
    tests_path=None,
    requirements=None,
    case_requirement_map=None,
    timeout=600,
):
    """Evalua una muestra y devuelve un resultado estructurado.

    `requirements` es una secuencia binaria de longitud EXPECTED_REQUIREMENTS
    (uno por requisito) o None si la tarea aun no define requisitos.
    `case_requirement_map` deriva los requisitos a partir de los casos pytest
    ({requisito: [case_id, ...]}); tiene prioridad sobre `requirements`.
    `tests_path` es la ruta al directorio o archivo de pruebas, o None.
    """
    result = create_result_template(sample_id, system, task, repetition)

    # 1) Sintaxis
    syntax = check_syntax(code_path)
    result["syntax_valid"] = syntax.valid
    syntax_dict = syntax.to_dict()
    result["syntax"] = syntax_dict
    if not syntax.valid:
        result["incidents"].append(
            _incident("syntax", syntax.status, syntax.message or "")
        )
        # Sin codigo valido no se puede continuar con las herramientas.
        return result

    # 2) Herramientas estaticas (Radon + Bandit)
    static = evaluate_static(code_path, timeout=timeout)
    radon = static["radon"]
    bandit = static["bandit"]
    result["radon"] = radon
    result["bandit"] = bandit

    if radon["status"] == "ok":
        result["cyclomatic_complexity"] = radon["average_complexity"]
        result["max_complexity"] = radon.get("max_complexity")
        result["maintainability_index"] = radon["maintainability_index"]
    else:
        result["incidents"].append(
            _incident("radon", radon["status"], radon.get("error") or "")
        )

    if bandit["status"] in ("clean", "issues_found"):
        result["security_low"] = bandit["security_low"]
        result["security_medium"] = bandit["security_medium"]
        result["security_high"] = bandit["security_high"]
    else:
        result["incidents"].append(
            _incident("bandit", bandit["status"], bandit.get("error") or "")
        )

    # 3) Pruebas funcionales (opcional: depende de la tarea)
    case_results = {}
    if tests_path is not None:
        pytest_result = pytest_runner.run_pytest(
            tests_path,
            timeout=timeout,
            sample_path=code_path,
            capture_cases=True,
        )
        result["pytest"] = pytest_result
        case_results = collect_case_results(pytest_result)
        result["cases"] = case_results
        for case_id, value in case_results.items():
            result[case_id] = value
        if pytest_result["status"] in ("ok", "failed"):
            result["tests_passed"] = pytest_result["summary"]["passed"]
        else:
            result["incidents"].append(
                _incident(
                    "pytest",
                    pytest_result["status"],
                    pytest_result.get("error") or "",
                )
            )

    # 4) Requisitos (opcional: depende de la tarea)
    if case_requirement_map is not None:
        detail = derive_requirements(case_results, case_requirement_map)
        result["requirements"] = detail
        for requirement_id, value in detail.items():
            result[requirement_id] = value
        result["requirements_satisfied"] = sum(detail.values())
    elif requirements is not None:
        if len(requirements) != EXPECTED_REQUIREMENTS:
            raise ValueError(
                f"El diseno exige {EXPECTED_REQUIREMENTS} requisitos, "
                f"se recibieron {len(requirements)}"
            )
        checker = evaluate_requirements(requirements)
        result["requirements_satisfied"] = checker.satisfied_count()

    _apply_scoring(result)
    return result


def _apply_scoring(result):
    """Calcula R, F, C, M, S e ICC a partir de los campos disponibles."""
    r = f = c = m = s = None

    if result["requirements_satisfied"] is not None:
        r = scoring.calculate_requirements_score(
            result["requirements_satisfied"], EXPECTED_REQUIREMENTS
        )
        result["R"] = r

    if result["tests_passed"] is not None:
        f = scoring.calculate_functional_score(result["tests_passed"], 10)
        result["F"] = f

    if result["cyclomatic_complexity"] is not None:
        try:
            complexity = float(result["cyclomatic_complexity"])
            c = scoring.calculate_complexity_score(complexity)
            result["C"] = c
        except (TypeError, ValueError) as exc:
            result["incidents"].append(
                _incident(
                    "scoring",
                    "invalid_complexity",
                    f"Complejidad ciclomatica invalida "
                    f"({result['cyclomatic_complexity']!r}): {exc}",
                )
            )

    if result["maintainability_index"] is not None:
        m = min(100.0, max(0.0, float(result["maintainability_index"])))
        result["M"] = m

    if (
        result["security_low"] is not None
        and result["security_medium"] is not None
        and result["security_high"] is not None
    ):
        s = scoring.calculate_security_score(
            result["security_low"],
            result["security_medium"],
            result["security_high"],
        )
        result["S"] = s

    if all(value is not None for value in (r, f, c, m, s)):
        result["ICC"] = scoring.calculate_icc(r, f, c, m, s)
