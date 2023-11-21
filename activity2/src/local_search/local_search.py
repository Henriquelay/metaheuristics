"""A generic local search algorithm in graphs."""

from __future__ import annotations

from typing import Callable
from enum import Enum

from networkx import Graph
from uctp.model import UCTP

from utils.dropping_stack import DroppingStack


class Problem:
    """A generic minimization/optimization problem."""

    class ProblemKind(Enum):
        """The kind of the problem."""

        MAXIMIZATION = 1
        MINIMIZATION = 2

    def __init__(
        self,
        objective_function: Callable[[int | float], int | float],
        kind: ProblemKind,
        search_space: tuple[int | float, int | float],
        graph: Graph,
        properties_function: Callable[[int | float], dict[str, int]] = lambda x: {},
    ):
        self.objective_function = objective_function
        self.properties_function = properties_function
        self.kind = kind
        self.search_space = search_space
        self.graph = graph

    def value_at(self, solution: int | float) -> int | float:
        """Returns the value of the solution in the point int | float"""

        return self.objective_function(solution)

    def properties(self, solution: int | float) -> dict[str, int]:
        """Returns the present properties of the solution in the point int | float"""

        return self.properties_function(solution)

    def neighbors(self, solution: int | float) -> list[int | float]:
        """Returns the neighbors of the solution"""

        return list(self.graph.neighbors(solution))

    def best_neighbor(self, solution: int | float) -> int | float:
        """Returns the best neighbor of the solution"""

        neighbors = self.neighbors(solution)
        best_neighbor = neighbors[0]
        best_neighbor_value = self.value_at(best_neighbor)

        for neighbor in neighbors[1:]:
            neighbor_value = self.value_at(neighbor)
            if self.better(neighbor_value, best_neighbor_value):
                best_neighbor = neighbor
                best_neighbor_value = neighbor_value

        return best_neighbor

    def better(self, solution_a: int | float, solution_b: int | float) -> bool:
        """Returns whether solution_a is better than solution_b"""

        if self.kind == Problem.ProblemKind.MAXIMIZATION:
            return self.value_at(solution_a) > self.value_at(solution_b)
        elif self.kind == Problem.ProblemKind.MINIMIZATION:
            return self.value_at(solution_a) < self.value_at(solution_b)
        else:
            raise ValueError("Invalid problem kind")


class LocalSearch:
    """A generic local search algorithm"""

    class NOpt(Enum):
        """The kind of neighborhood search step."""

        TWO_OPT = 2
        THREE_OPT = 3

    def __init__(
        self,
        problem: Problem,
        neighborhood_size: int,
        n_opt=NOpt.TWO_OPT,
    ):
        self.problem = problem
        self.last_solutions = DroppingStack(max_size=5)
        self.neighborhood_size = neighborhood_size
        self.n_opt = n_opt

    def stopping_criterion(self, iteration: int, max_iterations: int) -> bool:
        """Returns whether the local search should stop or not. True means stop, False means continue."""

        # At least three solutions must have been evaluated.
        if len(self.last_solutions) < 3:
            return False

        # If the last three solutions are the same.
        last = self.last_solutions[-1]
        if last == self.last_solutions[-2] and last == self.last_solutions[-3]:
            return True

        # If the delta between the last five solutions is less than 1%.
        if len(self.last_solutions) >= 5:
            delta = self.last_solutions[-1] - self.last_solutions[-5]
            if delta / self.last_solutions[-1] < 0.01:
                return True

        # If the maximum number of iterations has been reached.
        return iteration >= max_iterations

    def search(self, initial_solution: int | float, max_iterations: int):
        """Runs the local search algorithm for the problem"""

        # Initialize the solution.
        current_solution = initial_solution
        current_solution_value = self.problem.value_at(initial_solution)

        # Initialize the best solution.
        best_solution = current_solution
        best_solution_value = current_solution_value

        # Initialize the iteration.
        iteration = 0

        # While the stopping criterion is not met.
        while not self.stopping_criterion(iteration, max_iterations):
            # Increment the iteration counter.
            iteration += 1
            # Get the best neighbor of the current solution.
            best_neighbor = self.problem.best_neighbor(current_solution)

            # Get the value of the best neighbor value.
            best_neighbor_value = self.problem.value_at(best_neighbor)

            # If the best neighbor is better than the current solution.
            if self.problem.better(best_neighbor_value, current_solution_value):
                # Update the solution.
                current_solution = best_neighbor
                current_solution_value = best_neighbor_value

                # If the new current solution is better than the previous best solution.
                if self.problem.better(best_neighbor_value, best_solution_value):
                    # Update the best solution.
                    best_solution = best_neighbor

                    # Update the best solution value.
                    best_solution_value = best_neighbor_value

            else:
                # If the best neighbor is not better than the current solution, we are done
                # TODO 3-Opt
                break

        self.last_solutions.clear()

        # Return the best solution.
        return best_solution


class GuidedLocalSearch(LocalSearch):
    """A Guided Local Search algorithm"""

    def __init__(
        self,
        problem: Problem,
        neighborhood_size: int,
        alpha=0.3,
    ):
        self.penalties: dict[str, int] = {}

        self.original_objective_function = problem.objective_function

        self.alpha = alpha

        # Replacing the objective function with the augmented one
        if problem.kind == Problem.ProblemKind.MAXIMIZATION:
            problem.objective_function = lambda x: self.original_objective_function(
                x
            ) - self.objective_function_augmentation(x)
        elif problem.kind == Problem.ProblemKind.MINIMIZATION:
            problem.objective_function = lambda x: self.original_objective_function(
                x
            ) + self.objective_function_augmentation(x)
        else:
            raise ValueError("Invalid problem kind")

        super().__init__(problem, neighborhood_size)

    def objective_function_augmentation(
        self,
        x: int | float,
    ) -> int | float:
        """Augments the passed objetive function with the heuristic information"""
        return self.alpha * sum(
            [self.penalties.get(prop, 0) for prop in self.problem.properties(x)]
        )

    def search(self, initial_solution: int | float, max_iterations: int):
        """Runs the local search algorithm for the problem"""

        iteration = 0

        best_solution = initial_solution

        best_solution_value = self.original_objective_function(initial_solution)

        while not self.stopping_criterion(iteration, max_iterations):
            iteration += 1

            # Running regular local search
            solution = super().search(initial_solution, max_iterations // 10)
            solution_value = self.original_objective_function(solution)

            # Updating the best solution
            if self.problem.better(solution_value, best_solution_value):
                best_solution = solution
                best_solution_value = solution_value

            # Updating the penalties for the properties of the found optima
            for prop in self.problem.properties(solution):
                self.penalties[prop] += 1

        return best_solution
