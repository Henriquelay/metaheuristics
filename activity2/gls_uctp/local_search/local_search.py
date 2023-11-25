"""A generic local search algorithm in graphs."""

from __future__ import annotations
from collections import defaultdict
from time import time
from typing import Callable
from enum import Enum

from gls_uctp.uctp.model import UCTP, Solution


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
        start_time: float,
    ) -> bool:
        """Returns whether the local search should stop or not. True means stop, False means continue."""

        # At least three solutions must have been evaluated.
        # if len(last_solutions) < 3:
        #     return False

        # last: list[int | float] = last_solutions.stack

        # # If the last 3 solutions only include the same 2 or less solutions.
        # if len(last) >= 3:
        #     if len(set(last[-3:])) <= 2:
        #         print(f"Stopped because of same solutions found in the last 4 iterations: {set(last[-3:])}")
        #         return True

        # # If the delta between the last five solutions is less than 1%.
        # if len(last) >= 5:
        #     delta = abs(last[-1] - last[-5])
        #     delta_relative = delta / abs(last[-5])
        #     if delta_relative < 0.001:
        #         print("Stopped because of small delta between the last 5 solutions.")
        #         return True

        # If the time limit has been reached
        if (time() - start_time) >= self.time_limit_secs:
            # print("Stopped because of time limit.")
            return True

        # If the maximum number of iterations has been reached
        if iteration >= max_iterations:
            # print("Stopped because of maximum number of iterations.")
            return True

        return False

    # TODO make it yield instead of returning a list
    def search(
        self,
        initial_solution: Solution,
        max_iterations: int,
        problem: UCTP,
    ) -> tuple[Solution, list[int], int, float]:
        """Runs the local search algorithm for the problem. Returns the best solution, the score of the solution, the number of iterations and time elapsed."""

        # Start the timer
        start_time = time()

        def is_solution_valid(constraints: list[str]) -> bool:
            """Returns whether the solution is valid or not."""

            # If any constraint starts with H, the solution is not valid
            return not any(constraint.startswith("H") for constraint in constraints)

        # Initialize the solution.
        current_solution = initial_solution
        current_solution_value, constraints = problem.evaluate(current_solution)
        current_solution_is_valid = is_solution_valid(constraints)

        # Initialize the best solution.
        best_solution = current_solution
        best_solution_value = current_solution_value
        best_solution_value_list = [best_solution_value]
        best_solution_is_valid = current_solution_is_valid

        # Initialize the iteration.
        iteration = 0

        # While the stopping criterion is not met.
        while not self.stopping_criterion(iteration, max_iterations, start_time):
            # Increment the iteration counter.
            iteration += 1
            # Get the best neighbor of the current solution.

            neighbors = problem.neighbors(current_solution, self.neighborhood_size)
            neighbors = [
                (neighbor, problem.evaluate(neighbor)) for neighbor in neighbors
            ]
            best_neighbor, (best_neighbor_value, constraints) = min(
                neighbors, key=lambda neighbor: neighbor[1][0]
            )
            best_neighbor_is_valid = is_solution_valid(constraints)

            # If the best neighbor is better than the current solution.
            if best_neighbor_value < current_solution_value:
                if not current_solution_is_valid or best_neighbor_is_valid:
                    # Update the solution.
                    current_solution = best_neighbor
                    current_solution_value = best_neighbor_value
                    current_solution_is_valid = best_neighbor_is_valid

                # If the new current solution is better than the previous best solution.
                if current_solution_value < best_solution_value:
                    if not best_solution_is_valid or current_solution_is_valid:
                        # Update the best solution.
                        best_solution = current_solution
                        best_solution_value = current_solution_value
                        best_solution_is_valid = current_solution_is_valid

            best_solution_value_list.append(best_solution_value)
        # Finish the timer
        elapsed_time = time() - start_time

        # Return the best solution.
        return (best_solution, best_solution_value_list, iteration, elapsed_time)


class GuidedLocalSearch(LocalSearch):
    """A Guided Local Search algorithm"""

    def __init__(
        self,
        llambda=0.3,
        alpha=1 / 4,
        neighborhood_size: int = 10,
        time_limit_secs: int = 72,
    ):
        self.penalties: dict[str, int] = defaultdict(int)
        self.llambda = llambda
        self.alpha = alpha

        super().__init__(
            neighborhood_size=neighborhood_size, time_limit_secs=time_limit_secs
        )

    def augmentation_factor(
        self,
        properties: list[str],
    ) -> int:
        """Augments the passed objetive function with the heuristic information"""

        augmentation = (
            self.llambda
            * self.alpha
            * sum(self.penalties[prop] for prop in properties)
        )

        # Update the penalties for the properties of the found optima
        for prop in set(properties):
            self.penalties[prop] += 1

        return int(augmentation)

    def augmented_objective_function(
        self,
        solution: Solution,
        original_objective_function: Callable[[Solution], tuple[int, list[str]]],
    ) -> tuple[int, list[str]]:
        """Augments the passed objetive function with the heuristic information"""

        value, properties = original_objective_function(solution)

        return (
            value + self.augmentation_factor(properties),
            properties,
        )

    def search(
        self,
        initial_solution: Solution,
        max_iterations: int,
        problem: UCTP,
    ) -> tuple[Solution, list[int], int, float, int]:
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
        best_solution_value_list = [best_solution_value]

        while not self.stopping_criterion(iteration, max_iterations, start_time):
            iteration += 1

            (
                current_solution,
                _current_solution_value_list,
                additional_local_search_iterations,
                _time_elapsed,
                # Running a half local search iterations
            ) = super().search(current_solution, max_iterations // 2, problem)
            # print("Mapped:", current_solution_value_list[-1])
            current_solution_value, _ = original_objective_function(current_solution)

            # print("Current:", current_solution_value)

            local_search_iterations += additional_local_search_iterations

            # Updating the best solution
            if current_solution_value < best_solution_value:
                best_solution = current_solution
                best_solution_value = current_solution_value

            best_solution_value_list.append(best_solution_value)

        # Finish the timer
        elapsed_time = time() - start_time

        return (
            best_solution,
            best_solution_value_list,
            iteration,
            elapsed_time,
            local_search_iterations,
        )
