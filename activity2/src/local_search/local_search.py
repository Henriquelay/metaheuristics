"""A generic local search algorithm in graphs."""

from __future__ import annotations
from collections import defaultdict
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
        neighborhood_size: int,
        n_opt=NOpt.TWO_OPT,
    ):
        self.neighborhood_size = neighborhood_size
        self.n_opt = n_opt

    def stopping_criterion(
        self,
        iteration: int,
        max_iterations: int,
        last_solutions: DroppingStack[int | float],
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
            print(delta_relative)
            if delta_relative < 0.01:
                return True

        # If the maximum number of iterations has been reached.
        return iteration >= max_iterations

    def search(
        self,
        initial_solution: Solution,
        max_iterations: int,
        problem: UCTP,
        weights: tuple[
            tuple[float, float, float, float], tuple[float, float, float, float]
        ],
    ):
        """Runs the local search algorithm for the problem"""

        # Initialize the solution.
        current_solution = initial_solution
        current_solution_value = problem.evaluate(current_solution, weights)[0]

        # Initialize the best solution.
        best_solution = current_solution
        best_solution_value = current_solution_value

        last_solutions = DroppingStack(max_size=5)

        # Initialize the iteration.
        iteration = 0

        # While the stopping criterion is not met.
        while not self.stopping_criterion(iteration, max_iterations, last_solutions):
            # Increment the iteration counter.
            iteration += 1
            # Get the best neighbor of the current solution.

            neighbors = problem.neighbors(current_solution, 10)
            best_neighbor, best_neighbor_value = min(
                neighbors, key=lambda neighbor: neighbor[1]
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

        # Return the best solution.
        return best_solution


class GuidedLocalSearch(LocalSearch):
    """A Guided Local Search algorithm"""

    def __init__(
        self,
        neighborhood_size: int,
        llambda=0.3,
        alpha=1 / 4,
    ):
        self.penalties: dict[str, int] = defaultdict(int)
        self.llambda = llambda
        self.alpha = alpha

        super().__init__(neighborhood_size)

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
        weights: Weights,
        original_objective_function: Callable[
            [Solution, Weights], tuple[float, list[str]]
        ],
    ) -> tuple[float, list[str]]:
        """Augments the passed objetive function with the heuristic information"""

        value, properties = original_objective_function(solution, weights)

        return (
            value + self.augmentation_factor(properties, self.llambda, self.alpha),
            properties,
        )

    def search(
        self,
        initial_solution: Solution,
        max_iterations: int,
        problem: UCTP,
        weights: Weights,
    ):
        """Runs the local search algorithm for the problem"""

        original_objective_function = problem.evaluate
        problem.evaluate = lambda solution, weights: self.augmented_objective_function(
            solution, weights, original_objective_function
        )

        iteration = 0

        current_solution = initial_solution

        best_solution = initial_solution
        best_solution_value, _ = original_objective_function(best_solution, weights)

        last_solutions = DroppingStack(max_size=5)

        while not self.stopping_criterion(iteration, max_iterations, last_solutions):
            iteration += 1

            # Running a tenth of regular local search iterations
            current_solution = super().search(
                current_solution, max_iterations // 10, problem, weights
            )
            current_solution_value, _ = original_objective_function(
                current_solution, weights
            )

            last_solutions.push(current_solution_value)

            # Updating the best solution
            if current_solution_value < best_solution_value:
                best_solution = current_solution
                best_solution_value = current_solution_value

        return best_solution
