"""Pruebas del instrumento: interfaz de requisitos."""

import pytest

from evaluator.requirements_checker import (
    EXPECTED_REQUIREMENTS,
    RequirementsChecker,
    evaluate_requirements,
)


def test_expected_requirements_is_five():
    assert EXPECTED_REQUIREMENTS == 5


def test_register_and_score():
    checker = RequirementsChecker()
    for index in range(1, 6):
        checker.register(f"R{index}", 1 if index <= 3 else 0)
    assert checker.total() == 5
    assert checker.satisfied_count() == 3
    assert checker.score() == 60.0


def test_register_updates_existing():
    checker = RequirementsChecker()
    checker.register("R1", 0)
    checker.register("R1", 1)
    assert checker.total() == 1
    assert checker.satisfied_count() == 1


def test_score_requires_complete_registration():
    checker = RequirementsChecker(["R1", "R2"])
    checker.register("R1", 1)
    with pytest.raises(ValueError):
        checker.score()


def test_register_invalid_value():
    checker = RequirementsChecker()
    with pytest.raises(ValueError):
        checker.register("R1", "si")


def test_evaluate_requirements_from_flags():
    checker = evaluate_requirements([1, 1, 0, 1, 0])
    assert checker.satisfied_count() == 3
    assert checker.score() == 60.0
