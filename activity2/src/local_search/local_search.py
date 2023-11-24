"""A generic local search algorithm in graphs."""

from __future__ import annotations
from collections import defaultdict
from time import time
from tracemalloc import start
from typing import Callable
from enum import Enum

from uctp.model import UCTP, Solution, Weights

from utils.dropping_stack import DroppingStack


class LocalSearch:
    """A generic local search algorithm"""

    class NOpt(Enum):
        """The kind of neighborhood search step."""

        TWO_OPT = 2
        THREE_OPT = 3

    def __init__(
        self,
        n_opt=NOpt.TWO_OPT,
        neighborhood_size: int = 10,
        # Time benchmarked for my machine at home
        time_limit_secs: int = 72,
    ):
        self.neighborhood_size = neighborhood_size
        self.n_opt = n_opt
        self.time_limit_secs = time_limit_secs

    def stopping_criterion(
        self,
        iteration: int,
        max_iterations: int,
        last_solutions: DroppingStack[int | float],
        start_time: float,
    ) -> bool:
        """Returns whether the local search should stop or not. True means stop, False means continue."""

        # At least three solutions must have been evaluated.
        if len(last_solutions) < 3:
            return False

        last: list[int | float] = last_solutions.stack

        # If the last 3 solutions only include the same 2 or less solutions.
        if len(last) >= 4:
            if len(set(last[-4:])) <= 2:
                return True

        # If the delta between the last five solutions is less than 1%.
        if len(last) >= 5:
            delta = abs(last[-1] - last[-5])
            delta_relative = delta / abs(last[-5])
            if delta_relative < 0.01:
                return True

        # If the time limit has been reached
        if time() - start_time >= self.time_limit_secs:
            return True

        # If the maximum number of iterations has been reached.
        return iteration >= max_iterations

    def search(
        self,
        initial_solution: Solution,
        max_iterations: int,
        problem: UCTP,
    ) -> tuple[Solution, float, int, float]:
        """Runs the local search algorithm for the problem. Returns the best solution, the score of the solution, the number of iterations and time elapsed."""

        # Start the timer
        start_time = time()

        # Initialize the solution.
        current_solution = initial_solution
        current_solution_value = problem.evaluate(current_solution)[0]

        # Initialize the best solution.
        best_solution = current_solution
        best_solution_value = current_solution_value

        last_solutions = DroppingStack(max_size=5)

        # Initialize the iteration.
        iteration = 0

        # While the stopping criterion is not met.
        while not self.stopping_criterion(
            iteration, max_iterations, last_solutions, start_time
        ):
            # Increment the iteration counter.
            iteration += 1
            # Get the best neighbor of the current solution.

            neighbors = problem.neighbors(current_solution, self.neighborhood_size)
            neighbors = [
                (neighbor, problem.evaluate(neighbor)) for neighbor in neighbors
            ]
            best_neighbor, (best_neighbor_value, _) = min(
                neighbors, key=lambda neighbor: neighbor[1][0]
            )

            last_solutions.push(best_neighbor_value)

            # If the best neighbor is better than the current solution.
            if best_neighbor_value < current_solution_value:
                # Update the solution.
                current_solution = best_neighbor
                current_solution_value = best_neighbor_value

                # If the new current solution is better than the previous best solution.
                if current_solution_value < best_solution_value:
                    # Update the best solution.
                    best_solution = current_solution
                    best_solution_value = current_solution_value

        # Finish the timer
        elapsed_time = time() - start_time

        # Return the best solution.
        return (best_solution, best_solution_value, iteration, elapsed_time)


class GuidedLocalSearch(LocalSearch):
    """A Guided Local Search algorithm"""

    def __init__(
        self,
        llambda=0.3,
        alpha=1 / 4,
        neighborhood_size: int = 10,
    ):
        self.penalties: dict[str, int] = defaultdict(int)
        self.llambda = llambda
        self.alpha = alpha

        super().__init__(neighborhood_size=neighborhood_size)

    def augmentation_factor(
        self,
        properties: list[str],
        llambda: float,
        _alpha: float,
    ) -> float:
        """Augments the passed objetive function with the heuristic information"""

        augmentation = (
            llambda
            # TODO play with alpha
            # * alpha
            * sum(self.penalties[prop] for prop in properties)
        )

        # Update the penalties for the properties of the found optima
        for prop in properties:
            self.penalties[prop] += 1

        return augmentation

    def augmented_objective_function(
        self,
        solution: Solution,
        original_objective_function: Callable[[Solution], tuple[float, list[str]]],
    ) -> tuple[float, list[str]]:
        """Augments the passed objetive function with the heuristic information"""

        value, properties = original_objective_function(solution)

        return (
            value + self.augmentation_factor(properties, self.llambda, self.alpha),
            properties,
        )

    def search(
        self,
        initial_solution: Solution,
        max_iterations: int,
        problem: UCTP,
    ) -> tuple[Solution, float, int, int, float]:
        """Runs the local search algorithm for the problem. Returns the best solution, the score of the solution, the number of iterations, the number of local search iterations and time elapsed."""

        # Start the timer
        start_time = time()

        original_objective_function = problem.evaluate
        problem.evaluate = lambda solution: self.augmented_objective_function(
            solution, original_objective_function
        )

        iteration = 0
        local_search_iterations = 0

        current_solution = initial_solution

        best_solution = initial_solution
        best_solution_value, _ = original_objective_function(best_solution)

        last_solutions = DroppingStack(max_size=5)

        while not self.stopping_criterion(
            iteration, max_iterations, last_solutions, start_time
        ):
            iteration += 1

            (
                current_solution,
                _current_solution_mappked_value,
                more_local_search_iterations,
                _time_elapsed,
                # Running a half local search iterations
            ) = super().search(current_solution, max_iterations // 2, problem)
            current_solution_value, _ = original_objective_function(current_solution)

            local_search_iterations += more_local_search_iterations

            last_solutions.push(current_solution_value)

            # Updating the best solution
            if current_solution_value < best_solution_value:
                best_solution = current_solution
                best_solution_value = current_solution_value

        # Finish the timer
        elapsed_time = time() - start_time

        return (
            best_solution,
            best_solution_value,
            iteration,
            local_search_iterations,
            elapsed_time,
        )
