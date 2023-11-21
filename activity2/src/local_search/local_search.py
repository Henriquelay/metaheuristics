"""A generic local search algorithm in graphs."""

from __future__ import annotations
from pprint import pprint

from typing import Callable
from enum import Enum

from networkx import Graph
from uctp.model import UCTP

from utils.dropping_stack import DroppingStack


# class Problem:
#     """A generic minimization/optimization problem."""

#     class ProblemKind(Enum):
#         """The kind of the problem."""

#         MAXIMIZATION = 1
#         MINIMIZATION = 2

#     def __init__(
#         self,
#         objective_function: Callable[[int | float], int | float],
#         kind: ProblemKind,
#         search_space: tuple[int | float, int | float],
#         graph: Graph,
#         properties_function: Callable[[int | float], dict[str, int]] = lambda x: {},
#     ):
#         self.objective_function = objective_function
#         self.properties_function = properties_function
#         self.kind = kind
#         self.search_space = search_space
#         self.graph = graph

#     def value_at(self, solution: int | float) -> int | float:
#         """Returns the value of the solution in the point int | float"""

#         return self.objective_function(solution)

#     def properties(self, solution: int | float) -> dict[str, int]:
#         """Returns the present properties of the solution in the point int | float"""

#         return self.properties_function(solution)

#     def neighbors(self, solution: int | float) -> list[int | float]:
#         """Returns the neighbors of the solution"""
#         # TODO bound within search space

#         return list(self.graph.neighbors(solution))

#     def best_neighbor(self, solution: int | float) -> int | float:
#         """Returns the best neighbor of the solution"""

#         neighbors = self.neighbors(solution)
#         best_neighbor = neighbors[0]
#         best_neighbor_value = self.value_at(best_neighbor)

#         for neighbor in neighbors[1:]:
#             neighbor_value = self.value_at(neighbor)
#             if self.better(neighbor_value, best_neighbor_value):
#                 best_neighbor = neighbor
#                 best_neighbor_value = neighbor_value

#         return best_neighbor

#     def better(self, value_a: int | float, value_b: int | float) -> bool:
#         """Returns whether value_a is better than value_b"""

#         if self.kind == Problem.ProblemKind.MAXIMIZATION:
#             return value_a > value_b
#         elif self.kind == Problem.ProblemKind.MINIMIZATION:
#             return value_a < value_b
#         else:
#             raise ValueError("Invalid problem kind")


class LocalSearch:
    """A generic local search algorithm"""

    class NOpt(Enum):
        """The kind of neighborhood search step."""

        TWO_OPT = 2
        THREE_OPT = 3

    def __init__(
        self,
        # problem: Problem,
        neighborhood_size: int,
        n_opt=NOpt.TWO_OPT,
    ):
        # self.problem = problem
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
        initial_solution: Graph,
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
            best_neighbor = problem.best_neighbor(
                current_solution, self.neighborhood_size
            )
            best_neighbor_value = problem.evaluate(best_neighbor, weights)[0]

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
        self.penalties: dict[str, int] = {}
        self.llambda = llambda
        self.alpha = alpha

        # # Replacing the objective function with the augmented one
        # if problem.kind == Problem.ProblemKind.MAXIMIZATION:
        #     problem.objective_function = lambda x: self.original_objective_function(
        #         x
        #     ) - self.objective_function_augmentation(x, alpha, llambda)

        # elif problem.kind == Problem.ProblemKind.MINIMIZATION:
        #     problem.objective_function = lambda x: self.original_objective_function(
        #         x
        #     ) + self.objective_function_augmentation(x, alpha, llambda)

        # else:
        #     raise ValueError("Invalid problem kind")

        super().__init__(neighborhood_size)

    def search(
        self,
        initial_solution: Graph,
        max_iterations: int,
        problem: UCTP,
        weights: tuple[
            tuple[float, float, float, float], tuple[float, float, float, float]
        ],
    ):
        """Runs the local search algorithm for the problem"""

        def augmented_objective_function(
            self,
            solution: Graph,
            weights: tuple[
                tuple[float, float, float, float], tuple[float, float, float, float]
            ],
            evaluation: Callable[
                [
                    Graph,
                    tuple[
                        tuple[float, float, float, float],
                        tuple[float, float, float, float],
                    ],
                ],
                tuple[float, set[str]],
            ],
            alpha: float,
            llambda: float,
        ) -> tuple[float, set[str]]:
            """Augments the passed objetive function with the heuristic information"""
            original_value, properties = evaluation(solution, weights)
            augmentation = (
                llambda
                # * alpha
                * sum([self.penalties.get(prop, 0) for prop in properties])
            )

            return (original_value + augmentation, properties)

        original_objective_function = problem.evaluate
        problem.evaluate = lambda solution, weights: augmented_objective_function(
            self,
            solution,
            weights,
            original_objective_function,
            self.alpha,
            self.llambda,
        )

        iteration = 0

        current_solution = initial_solution

        best_solution = initial_solution
        best_solution_value = original_objective_function(best_solution, weights)[0]

        last_solutions = DroppingStack(max_size=5)

        while not self.stopping_criterion(iteration, max_iterations, last_solutions):
            iteration += 1

            # Running a tenth of regular local search iterations
            current_solution = super().search(
                current_solution, max_iterations // 10, problem, weights
            )
            current_solution_value, properties = original_objective_function(
                current_solution, weights
            )

            last_solutions.push(current_solution_value)

            # Updating the best solution
            if current_solution_value < best_solution_value:
                best_solution = current_solution
                best_solution_value = current_solution_value

            # Updating the penalties for the properties of the found optima
            for prop in properties:
                # TODO utility function
                self.penalties[prop] += 1

        return best_solution
