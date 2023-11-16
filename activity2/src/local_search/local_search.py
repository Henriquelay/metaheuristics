from __future__ import  annotations

from typing import Callable
from enum import Enum

from utils.dropping_stack import DroppingStack
from networkx import Graph

class Problem[D, I]:
    """A generic minimization/optimization problem. D is the domain of the problem, and I is the image of the problem."""

    class ProblemKind(Enum):
        MAXIMIZATION = 1
        MINIMIZATION = 2

    def __init__(self, objective_function: Callable[[D], I], kind: ProblemKind, search_space: tuple[D, D], graph: Graph):
        self.objective_function = objective_function
        self.kind = kind
        self.search_space = search_space
        self.graph = graph

    def value_at(self, solution: D) -> I:
        """Returns the value of the solution in the point I"""

        return self.objective_function(solution)

class LocalSearch[D, I]:
    """A generic local search algorithm"""

    class N_OPT(Enum):
        TWO_OPT = 2
        THREE_OPT = 3

    def __init__(self, problem: Problem[D, I], max_iterations=1000, n_opt=N_OPT.TWO_OPT):
        self.max_iterations = max_iterations
        self.problem = problem
        self.last_solutions = DroppingStack(max_size=5)

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

    def run(self, initial_solution: D):
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
            # Get the neighbors of the current solution.
            neighbors = self.problem.neighbors(solution)

            # Get the best neighbor.
            best_neighbor = self.best_neighbor(neighbors)

            # Get the best neighbor value.
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

            # Increment the iteration.
            iteration += 1

        # Return the best solution.
        return best_solution
