"""A generic local search algorithm in graphs."""

from __future__ import annotations

from typing import Callable
from enum import Enum

from networkx import Graph

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
    ):
        self.objective_function = objective_function
        self.kind = kind
        self.search_space = search_space
        self.graph = graph

    def value_at(self, solution: int | float) -> int | float:
        """Returns the value of the solution in the point int | float"""

        return self.objective_function(solution)

    def neighbors(self, solution: int | float) -> list[int | float]:
        """Returns the neighbors of the solution"""

        return self.graph.neighbors(solution)

    def best_neighbor(self, solution: int | float) -> int | float:
        """Returns the best neighbor of the solution"""

        neighbors = self.neighbors(solution)
        neighbor_values = [self.value_at(neighbor) for neighbor in neighbors]

        if self.kind == Problem.ProblemKind.MAXIMIZATION:
            return max(neighbor_values, key=self.value_at)
        elif self.kind == Problem.ProblemKind.MINIMIZATION:
            return min(neighbor_values, key=self.value_at)
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
        max_iterations=1000,
        n_opt=NOpt.TWO_OPT,
    ):
        self.max_iterations = max_iterations
        self.problem = problem
        self.last_solutions = DroppingStack(max_size=5)
        self.neighborhood_size = neighborhood_size
        self.n_opt = n_opt

    def stopping_criterion(self, iteration: int) -> bool:
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
        return iteration >= self.max_iterations

    def run(self, initial_solution: int | float):
        """Runs the local search algorithm for the problem"""

        # Initialize the solution.
        solution = initial_solution

        # Initialize the best solution.
        best_solution = solution

        # Initialize the best solution's image.
        best_solution_value = self.problem.value_at(best_solution)

        # Initialize the iteration.
        iteration = 0

        # While the stopping criterion is not met.
        while not self.stopping_criterion(iteration):
            # Get the best neighbor  of the current solution.
            best_neighbor = self.problem.best_neighbor(solution)

            # Get the value of the best neighbor value.
            best_neighbor_value = self.problem.value_at(best_neighbor)

            # If the best neighbor is better than the current solution.
            if best_neighbor_value > best_solution_value:
                # Update the best solution.
                best_solution = best_neighbor

                # Update the best solution value.
                best_solution_value = best_neighbor_value

            # If the best neighbor is better than the current solution.
            if best_neighbor_value > self.problem.value_at(solution):
                # Update the solution.
                solution = best_neighbor

            # Increment the iteration counter.
            iteration += 1

        # Return the best solution.
        return best_solution
