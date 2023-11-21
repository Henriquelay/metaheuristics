"""Tests for the local search algorithm"""

from networkx import Graph

from local_search.local_search import LocalSearch, Problem


def graph_for_function_problems():
    """Returns a graph for function problems. The graph creates a node for each solution, with a step of 0.1, and connects each node to its neighbors within a distance of 0.2"""

    graph = Graph()
    for i in range(-100, 100):
        graph.add_node(i / 10)

    for i in range(-100, 100):
        for j in range(-100, 100):
            if abs(i - j) <= 2 and i != j:
                graph.add_edge(i / 10, j / 10)

    return graph


class TestProblem:
    """Tests for the Problem class"""

    def test_value_at_works(self):
        """Test that value_at works"""

        def objective_function(x: int | float) -> int | float:
            """A quadratic function with root 2"""
            return -((x - 2) ** 2)

        graph = graph_for_function_problems()

        problem = Problem(
            objective_function=objective_function,
            kind=Problem.ProblemKind.MAXIMIZATION,
            search_space=(-10, 10),
            graph=graph,
        )

        assert problem.value_at(2) == 0
        assert problem.value_at(1) == -1
        assert problem.value_at(3) == -1

    def test_neighbors_works(self):
        """Test that neighbors works"""

        def objective_function(x: int | float) -> int | float:
            """A quadratic function with root 2"""
            return -((x - 2) ** 2)

        graph = graph_for_function_problems()

        problem = Problem(
            objective_function=objective_function,
            kind=Problem.ProblemKind.MAXIMIZATION,
            search_space=(-10, 10),
            graph=graph,
        )

        assert problem.neighbors(2) == [1.8, 1.9, 2.1, 2.2]
        assert problem.neighbors(1) == [0.8, 0.9, 1.1, 1.2]
        assert problem.neighbors(3) == [2.8, 2.9, 3.1, 3.2]
        assert problem.neighbors(0.1) == [-0.1, 0.0, 0.2, 0.3]

    def test_best_neighbor_works(self):
        """Test that best_neighbor works"""

        def objective_function(x: int | float) -> int | float:
            """A quadratic function with root 2"""
            return -((x - 2) ** 2)

        graph = graph_for_function_problems()

        problem = Problem(
            objective_function=objective_function,
            kind=Problem.ProblemKind.MAXIMIZATION,
            search_space=(-10, 10),
            graph=graph,
        )

        assert problem.best_neighbor(2) == 1.9
        assert problem.best_neighbor(1.9) == 2.0
        assert problem.best_neighbor(2.1) == 2.0
        assert problem.best_neighbor(1) == 1.2
        assert problem.best_neighbor(0.1) == 0.3
        assert problem.best_neighbor(-0.1) == 0.1

    def test_better_works(self):
        """Test that better works"""

        def objective_function(x: int | float) -> int | float:
            """A quadratic function with root 2"""
            return -((x - 2) ** 2)

        graph = graph_for_function_problems()

        problem = Problem(
            objective_function=objective_function,
            kind=Problem.ProblemKind.MAXIMIZATION,
            search_space=(-10, 10),
            graph=graph,
        )

        assert problem.better(2, 1) is True
        assert problem.better(1, 2) is False
        assert problem.better(2, 2) is False


class TestLocalSearch:
    """Tests for the LocalSearch class"""

    def test_search_works(self):
        """Test that search works"""

        def objective_function(x: int | float) -> int | float:
            """A quadratic function with root 2"""
            return -((x - 2) ** 2)

        graph = graph_for_function_problems()

        problem = Problem(
            objective_function=objective_function,
            kind=Problem.ProblemKind.MAXIMIZATION,
            search_space=(-10, 10),
            graph=graph,
        )

        local_search = LocalSearch(problem=problem, neighborhood_size=-1)

        assert local_search.search(initial_solution=0, max_iterations=10) == 2
