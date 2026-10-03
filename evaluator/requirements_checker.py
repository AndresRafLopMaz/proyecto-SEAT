"""Interfaz generica para registrar requisitos y calcular R.

IMPORTANTE: este modulo no define requisitos para T1, T2 ni T3. Solo ofrece
la mecanica para registrar N requisitos con resultado binario (cumple=1,
no cumple=0) y calcular R reutilizando `evaluator.scoring`.
"""

from __future__ import annotations

from evaluator.scoring import calculate_requirements_score

# El diseno metodologico evalua 5 requisitos por tarea.
EXPECTED_REQUIREMENTS = 5


class RequirementsChecker:
    """Registro de requisitos evaluados de forma binaria."""

    def __init__(self, requirement_ids=None):
        self._entries = []
        if requirement_ids is not None:
            for requirement_id in requirement_ids:
                self.register(requirement_id, None)

    def register(self, requirement_id, satisfied):
        """Registra o actualiza un requisito. `satisfied` es None/True/False/0/1."""
        if satisfied not in (None, True, False, 0, 1):
            raise ValueError(
                "satisfied debe ser None, True, False, 0 o 1"
            )
        normalized = None if satisfied is None else int(bool(satisfied))
        self._entries = [
            entry
            for entry in self._entries
            if entry["id"] != str(requirement_id)
        ]
        self._entries.append({"id": str(requirement_id), "satisfied": normalized})
        return self

    @property
    def entries(self):
        return [dict(entry) for entry in self._entries]

    def total(self):
        return len(self._entries)

    def satisfied_count(self):
        return sum(1 for entry in self._entries if entry["satisfied"] == 1)

    def is_complete(self):
        return self.total() > 0 and all(
            entry["satisfied"] is not None for entry in self._entries
        )

    def score(self):
        """Calcula R. Requiere que todos los requisitos esten evaluados."""
        if not self.is_complete():
            raise ValueError(
                "No se puede calcular R: hay requisitos sin evaluar o el "
                "registro esta vacio"
            )
        return calculate_requirements_score(
            self.satisfied_count(), self.total()
        )

    def to_dict(self):
        return {
            "requirements": self.entries,
            "total": self.total(),
            "satisfied": self.satisfied_count(),
            "complete": self.is_complete(),
            "R": self.score() if self.is_complete() else None,
        }


def evaluate_requirements(satisfied_flags):
    """Crea un RequirementsChecker a partir de una secuencia binaria."""
    checker = RequirementsChecker()
    for index, flag in enumerate(satisfied_flags, start=1):
        checker.register(f"R{index}", flag)
    return checker
