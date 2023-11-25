"""Tests for the local search heuristics for the UCTP problem."""

from typing import Sequence

from gls_uctp.local_search.local_search import LocalSearch, GuidedLocalSearch
from gls_uctp.uctp.model import UCTP


def cases(instances: Sequence):
    """Decorator for running a test case for each instance."""

    def decorator(func):
        def wrapper(*_args, **kwargs):
            for instance in instances:
                print(f"Running test case: {instance}")
                func(instance)

        return wrapper

    return decorator


paths = [f"instances/test/comp{instance:02}.ctt" for instance in range(1, 22)]


@cases(paths)
def test_local_search(path: str):
    """Test the local search algorithm for the UCTP problem."""

    with open(path, "r", encoding="utf8") as file:
        problem = UCTP.parse(file.readlines())

        initial_solution = problem.random_solution()

        initial_solution_value, _ = problem.evaluate(initial_solution)

        print(f"Initial solution: {initial_solution_value}")

        print(f"Solving for {path}")
        (_solution, solution_value, _niter, _time_elapsed) = LocalSearch(
            neighborhood_size=10
        ).search(initial_solution, 10, problem)

        try:
            assert solution_value is not None
        finally:
            file.close()


@cases(paths)
def test_guided_local_search(path: str):
    """Test the guided local search algorithm for the UCTP problem."""

    with open(path, "r", encoding="utf8") as file:
        problem = UCTP.parse(file.readlines())

        initial_solution = problem.random_solution()

        initial_solution_value, _ = problem.evaluate(initial_solution)

        print(f"Initial solution: {initial_solution_value}")

        print(f"Solving for {path}")
        (
            _solution,
            solution_value,
            _niter,
            _local_searches_iter,
            _time_elapsed,
        ) = GuidedLocalSearch(neighborhood_size=10).search(
            initial_solution, 10, problem
        )

        try:
            assert solution_value is not None
        finally:
            file.close()
