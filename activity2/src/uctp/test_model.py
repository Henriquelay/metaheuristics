# pylint: disable=all

from math import inf
from pprint import pprint
from typing import Any

from pytest import raises
from uctp.model import TIME_SLOT_SEPARATOR, UCTP, Constraint

TOY_INSTANCE = """Name: Toy
Courses: 4
Rooms: 3
Days: 5
Periods_per_day: 4
Curricula: 2
Constraints: 8

COURSES:
SceCosC Ocra 3 3 30
ArcTec Indaco 4 3 42
TecCos Rosa 3 4 40
GeoTec Scarlatti 3 4 18

ROOMS:
rA 32
rB 50
rC 40

CURRICULA:
Cur1 3 SceCosC ArcTec TecCos
Cur2 2 TecCos GeoTec

UNAVAILABILITY_CONSTRAINTS:
TecCos 2 0
TecCos 2 1
TecCos 3 2
TecCos 3 3
ArcTec 4 0
ArcTec 4 1
ArcTec 4 2
ArcTec 4 3

END."""


def test_parse_all_instances():
    """UCTP can parse all instances in the instances folder"""

    instances = [f"instances/test/comp{instance:02}.ctt" for instance in range(1, 22)]

    print(instances)

    for path in instances:
        with open(path, "r") as file:
            print(f"Parsing {path}")
            problem = UCTP.parse(file.readlines())
            assert problem.name is not None
            assert problem.days is not None
            assert problem.periods_per_day is not None
            assert len(problem.rooms) > 0
            assert len(problem.curricula) > 0
            assert len(problem.constraints) > 0
        file.close()


def test_UCTP_parsing():
    """UCTP can parse toy intance successfully and no data is lost"""

    problem = UCTP.parse(TOY_INSTANCE.splitlines())
    assert problem.name == "Toy"
    assert problem.days == 5
    assert problem.periods_per_day == 4
    assert len(problem.rooms) == 3
    assert len(problem.curricula) == 2
    assert len(problem.constraints) == 8

    rooms_names = {room.name for room in problem.rooms.values()}
    assert rooms_names == {"rA", "rB", "rC"}

    curricula_names = {curriculum.name for curriculum in problem.curricula.values()}
    assert curricula_names == {"Cur1", "Cur2"}

    for curriculum in problem.curricula.values():
        if curriculum.name == "Cur1":
            assert {course.name for course in curriculum.courses.values()} == {
                "SceCosC",
                "ArcTec",
                "TecCos",
            }
        elif curriculum.name == "Cur2":
            assert {course.name for course in curriculum.courses.values()} == {
                "TecCos",
                "GeoTec",
            }
        else:
            assert False

    assert problem.rooms["rA"].capacity == 32
    assert problem.rooms["rB"].capacity == 50
    assert problem.rooms["rC"].capacity == 40

    assert {course.name for course in problem.curricula["Cur1"].courses.values()} == {
        "SceCosC",
        "ArcTec",
        "TecCos",
    }
    assert {course.name for course in problem.curricula["Cur2"].courses.values()} == {
        "TecCos",
        "GeoTec",
    }

    def assert_constraint(
        constraint: Constraint, course_name: str, day: int, period: int
    ):
        course = constraint.course()
        assert course is not None
        assert course.name == course_name
        assert constraint.day == day
        assert constraint.period == period

    assert_constraint(problem.constraints[0], "TecCos", 2, 0)
    assert_constraint(problem.constraints[1], "TecCos", 2, 1)
    assert_constraint(problem.constraints[2], "TecCos", 3, 2)
    assert_constraint(problem.constraints[3], "TecCos", 3, 3)
    assert_constraint(problem.constraints[4], "ArcTec", 4, 0)
    assert_constraint(problem.constraints[5], "ArcTec", 4, 1)
    assert_constraint(problem.constraints[6], "ArcTec", 4, 2)
    assert_constraint(problem.constraints[7], "ArcTec", 4, 3)


def test_UCTP_graph():
    """Asserts graph generation for UCTP curricula"""

    problem = UCTP.parse(TOY_INSTANCE.splitlines())
    graph = problem.to_graph()

    nodes_data = graph.nodes.data()
    # Convert into a dict[node_name, data]
    nodes: dict[str, dict[str, Any]] = {node[0]: node[1] for node in nodes_data}
    pprint(nodes)

    # "course" colored nodes must exist
    assert len(
        {node for node in nodes if nodes[node]["color"] == problem.Colors.COURSE}
    ) == len(problem.courses)

    # "room-day-period" colored nodes must exist
    assert (
        len({node for node in nodes if nodes[node]["color"] == problem.Colors.ROOM})
        == len(problem.rooms) * problem.days * problem.periods_per_day
    )

    for node in nodes:
        # All nodes must have a color
        assert "color" in nodes[node]

        # Same color nodes must not be adjacent.
        for neighbor in graph.neighbors(node):
            print(neighbor)
            assert nodes[node]["color"] != nodes[neighbor]["color"]

        if nodes[node]["color"] == problem.Colors.COURSE:
            # Course nodes must be intially connected to no room nodes.
            assert (
                len(
                    {
                        neighbor
                        for neighbor in graph.neighbors(node)
                        if nodes[neighbor]["color"] == "room-day-period"
                    }
                )
                == 0
            )

            # Course n odes must be connected to one and only one teacher node
            expected_course = {problem.courses[node]}
            assert len(expected_course) == 1
            expected_course = expected_course.pop()

        elif nodes[node]["color"] == problem.Colors.ROOM:
            # Room should exist in the problem
            assert node.split(TIME_SLOT_SEPARATOR)[0] in problem.rooms.keys()

            # Room nodes must be connected to no course nodes.
            assert (
                len(
                    {
                        neighbor
                        for neighbor in graph.neighbors(node)
                        if nodes[neighbor]["color"] == "course"
                    }
                )
                == 0
            )

            # Room nodes must be connected to no curriculum nodes.
            assert (
                len(
                    {
                        neighbor
                        for neighbor in graph.neighbors(node)
                        if nodes[neighbor]["color"] == "curriculum"
                    }
                )
                == 0
            )

            # Room nodes must be connected to no teacher nodes.
            assert (
                len(
                    {
                        neighbor
                        for neighbor in graph.neighbors(node)
                        if nodes[neighbor]["color"] == "teacher"
                    }
                )
                == 0
            )

        else:
            # Other nodes must not exist
            print(node)
            print(nodes[node])
            assert False


class TestEvaluation:
    """Tests for the evaluation of a solution"""

    hard_weights = (10, 11, 12, 13)
    soft_weights = (4, 3, 2, 1)
    problem = UCTP.parse(TOY_INSTANCE.splitlines())

    def test_evaluation_hard_constraints_ok(self):
        """Asserts that the solution evaluation is correct for a valid solution"""

        weights = (self.hard_weights, (0, 0, 0, 0))

        # A valid solution
        solution = {
            "SceCosC": [("rA", 0, 0), ("rA", 1, 0), ("rA", 2, 0)],
            "ArcTec": [("rB", 0, 1), ("rB", 1, 1), ("rB", 2, 1), ("rB", 3, 1)],
            "TecCos": [("rC", 0, 2), ("rC", 1, 2), ("rC", 2, 2)],
            "GeoTec": [("rA", 0, 3), ("rC", 1, 3), ("rC", 2, 3)],
        }
        assert self.problem.evaluate(solution, weights) == 0

    def test_evaluation_hard_constraints_h1(self):
        """Asserts that the solution evaluation is correct for solution that violates hard constraint H1"""

        weights = (self.hard_weights, (0, 0, 0, 0))

        # Missing a lecture
        solution = {
            "SceCosC": [("rA", 0, 0), ("rA", 1, 0)],
            "ArcTec": [("rB", 0, 1), ("rB", 1, 1), ("rB", 2, 1), ("rB", 3, 1)],
            "TecCos": [("rC", 0, 2), ("rC", 1, 2), ("rC", 2, 2)],
            "GeoTec": [("rA", 0, 3), ("rC", 1, 3), ("rC", 2, 3)],
        }
        assert self.problem.evaluate(solution, weights) == self.hard_weights[0]

        # Two lectures of the same course in the same day-period
        solution = {
            "SceCosC": [("rA", 0, 0), ("rA", 1, 0), ("rA", 1, 0)],
            "ArcTec": [("rB", 0, 1), ("rB", 1, 1), ("rB", 2, 1), ("rB", 3, 1)],
            "TecCos": [("rC", 0, 2), ("rC", 1, 2), ("rC", 2, 2)],
            "GeoTec": [("rA", 0, 3), ("rC", 1, 3), ("rC", 2, 3)],
        }
        assert self.problem.evaluate(solution, weights) == self.hard_weights[0]

    def test_evaluation_hard_constraints_h2(self):
        """Asserts that the solution evaluation is correct for solution that violates hard constraint H2"""

        weights = (self.hard_weights, (0, 0, 0, 0))

        # Two courses in the same room at the same time, different curriculum
        solution = {
            "SceCosC": [("rA", 0, 0), ("rA", 1, 0), ("rA", 2, 0)],
            "ArcTec": [("rB", 0, 1), ("rB", 1, 1), ("rB", 2, 1), ("rB", 3, 1)],
            "TecCos": [("rC", 0, 2), ("rC", 1, 2), ("rC", 2, 2)],
            "GeoTec": [("rA", 0, 3), ("rC", 1, 3), ("rA", 2, 0)],
        }
        assert self.problem.evaluate(solution, weights) == self.hard_weights[1]

    def test_evaluation_hard_constraints_h3(self):
        """Asserts that the solution evaluation is correct for solution that violates hard constraint H3"""

        weights = (self.hard_weights, (0, 0, 0, 0))

        # Two courses of the same curriculum in the same day-period
        solution = {
            "SceCosC": [("rA", 0, 0), ("rA", 1, 0), ("rA", 2, 0)],
            "ArcTec": [("rB", 0, 0), ("rB", 1, 1), ("rB", 2, 1), ("rB", 3, 1)],
            "TecCos": [("rC", 0, 2), ("rC", 1, 2), ("rC", 2, 2)],
            "GeoTec": [("rA", 0, 3), ("rC", 1, 3), ("rC", 2, 3)],
        }
        assert self.problem.evaluate(solution, weights) == self.hard_weights[2]

    def test_evaluation_hard_constraints_h4(self):
        """Asserts that the solution evaluation is correct for solution that violates hard constraint H4"""

        weights = (self.hard_weights, (0, 0, 0, 0))

        # A solution with a course in an unavailable period
        solution = {
            "SceCosC": [("rA", 0, 0), ("rA", 1, 0), ("rA", 2, 0)],
            "ArcTec": [("rB", 0, 1), ("rB", 1, 1), ("rB", 2, 1), ("rB", 4, 0)],
            "TecCos": [("rC", 0, 2), ("rC", 1, 2), ("rC", 2, 2)],
            "GeoTec": [("rA", 0, 3), ("rC", 1, 3), ("rC", 2, 3)],
        }
        assert self.problem.evaluate(solution, weights) == self.hard_weights[3]

    def test_evaluation_soft_constraints(self):
        """Asserts that the solution evaluation is correct for a valid solution with soft constraints weights"""

        weights = ((0, 0, 0, 0), self.soft_weights)

        # A optimal solution
        solution = {
            "SceCosC": [("rA", 0, 0), ("rA", 1, 0), ("rA", 2, 0)],
            "ArcTec": [("rB", 0, 1), ("rB", 1, 1), ("rB", 2, 1), ("rB", 3, 1)],
            "TecCos": [("rC", 0, 2), ("rC", 1, 2), ("rC", 2, 2)],
            "GeoTec": [("rA", 0, 3), ("rC", 1, 3), ("rC", 2, 3)],
        }
        assert self.problem.evaluate(solution, weights) == 7
