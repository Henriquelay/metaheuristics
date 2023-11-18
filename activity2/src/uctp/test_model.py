# pylint: disable=all

from math import inf
from pprint import pprint
from typing import Any

from pytest import raises
from uctp.model import UCTP, Constraint

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

    for node in nodes:
        # All nodes must have a color
        assert "color" in nodes[node]

        # Same color nodes must not be adjacent.
        for neighbor in graph.neighbors(node):
            print(neighbor)
            assert nodes[node]["color"] != nodes[neighbor]["color"]

        if nodes[node]["color"] == "course":
            # Course nodes must be connected to curriculum nodes which have the said course.
            curricula_with_course = {
                curriculum
                for curriculum in problem.curricula.values()
                if node in curriculum.courses
            }
            curricula_name_with_course = {
                curriculum.name
                for curriculum in curricula_with_course
            }
            course_node_curricula = {
                neighbor
                for neighbor in graph.neighbors(node)
                if nodes[neighbor]["color"] == "curriculum"
            }
            assert curricula_name_with_course == course_node_curricula

            # Course nodes must be connected to no room nodes.
            assert (
                len(
                    {
                        neighbor
                        for neighbor in graph.neighbors(node)
                        if nodes[neighbor]["color"] == "room"
                    }
                )
                == 0
            )

            # Course n odes must be connected to one and only one teacher node
            expected_course = {problem.courses[node]}
            assert len(expected_course) == 1
            expected_course = expected_course.pop()

            teacher_nodes = [
                neighbor
                for neighbor in graph.neighbors(node)
                if nodes[neighbor]["color"] == "teacher"
            ]
            assert len(teacher_nodes) == 1
            teacher_node = teacher_nodes[0]
            assert expected_course.teacher == teacher_node

        elif nodes[node]["color"] == "curriculum":
            # Curriculum nodes must be connected to course nodes which are in the curriculum.
            curriculum = problem.curricula[node]
            course_nodes = {
                neighbor
                for neighbor in graph.neighbors(node)
                if nodes[neighbor]["color"] == "course"
            }
            assert len(curriculum.courses) == len(course_nodes)
            assert {course.name for course in curriculum.courses.values()} == {
                problem.courses[node].name for node in course_nodes
            }

            # Curriculum nodes must be connected to no room nodes.
            assert (
                len(
                    {
                        neighbor
                        for neighbor in graph.neighbors(node)
                        if nodes[neighbor]["color"] == "room"
                    }
                )
                == 0
            )

            # Curriculum nodes must be connected to no teacher nodes.
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
        
        elif nodes[node]["color"] == "teacher":
            # Teacher should exist in the problem
            assert node in problem.teachers

            # Teacher nodes must be connected to course nodes
            course_nodes = {
                neighbor
                for neighbor in graph.neighbors(node)
                if nodes[neighbor]["color"] == "course"
            }
            assert len(course_nodes) > 0

            # Teacher nodes must be connected to no room nodes.
            assert (
                len(
                    {
                        neighbor
                        for neighbor in graph.neighbors(node)
                        if nodes[neighbor]["color"] == "room"
                    }
                )
                == 0
            )

            # Teacher nodes must be connected to no curriculum nodes.
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

        elif nodes[node]["color"] == "room":
            # Room should exist in the problem
            assert node.split()[0] in problem.rooms.keys()

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

class TestEvaluation:
    def test_evaluation_hard_constraints(self):
        """Asserts that the solution evaluation is correct"""

        problem = UCTP.parse(TOY_INSTANCE.splitlines())

        # Weights for soft constraints
        weights = (0, 0, 0, 0)
        evaluate = lambda solution: problem.evaluate(solution, weights)

        # A valid solution
        solution = {
            "SceCosC":  [("rA", 0, 0), ("rA", 1, 0), ("rA", 2, 0)],
            "ArcTec":   [("rB", 0, 1), ("rB", 1, 1), ("rB", 2, 1), ("rB", 3, 1)],
            "TecCos":   [("rC", 0, 2), ("rC", 1, 2), ("rC", 2, 2)],
            "GeoTec":   [("rA", 0, 3), ("rC", 1, 3), ("rC", 2, 3)],
        }
        assert evaluate(solution) is not None

        # A solution with a course in an unavailable period
        solution = {
            "SceCosC":  [("rA", 0, 0), ("rA", 1, 0), ("rA", 2, 3)],
            "ArcTec":   [("rB", 0, 1), ("rB", 1, 1), ("rB", 2, 1), ("rB", 3, 1)],
            "TecCos":   [("rC", 0, 2), ("rC", 1, 2), ("rC", 2, 0)],
            "GeoTec":   [("rA", 0, 3), ("rC", 1, 3), ("rC", 2, 3)],
        }
        with raises(ValueError, match="H4 violated"):
            evaluate(solution)

        # Two lectures of the same course in the same day-period
        solution = {
            "SceCosC":  [("rA", 0, 0), ("rA", 0, 0), ("rA", 2, 0)],
            "ArcTec":   [("rB", 0, 1), ("rB", 1, 1), ("rB", 2, 1), ("rB", 3, 1)],
            "TecCos":   [("rC", 0, 2), ("rC", 1, 2), ("rC", 2, 2)],
            "GeoTec":   [("rA", 0, 3), ("rC", 1, 3), ("rC", 2, 3)],
        }
        with raises(ValueError, match="H1 violated"):
            evaluate(solution)

        # Two courses in the same room at the same time
        solution = {
            "SceCosC":  [("rA", 0, 0), ("rA", 1, 0), ("rA", 2, 0)],
            "ArcTec":   [("rB", 0, 1), ("rB", 1, 1), ("rB", 2, 1), ("rB", 3, 1)],
            "TecCos":   [("rC", 0, 2), ("rC", 1, 2), ("rC", 2, 2)],
            "GeoTec":   [("rA", 0, 0), ("rC", 1, 3), ("rC", 2, 3)],
        }
        with raises(ValueError, match="H2 violated"):
            evaluate(solution)

        # Two courses of the same curriculum in the same day-period
        solution = {
            "SceCosC":  [("rA", 0, 0), ("rA", 1, 0), ("rA", 2, 0)],
            "ArcTec":   [("rB", 0, 0), ("rB", 1, 1), ("rB", 2, 1), ("rB", 3, 1)],
            "TecCos":   [("rC", 0, 2), ("rC", 1, 2), ("rC", 2, 2)],
            "GeoTec":   [("rA", 0, 3), ("rC", 1, 3), ("rC", 2, 3)],
        }
        with raises(ValueError, match="H3 violated"):
            evaluate(solution)

    def test_evaluation_soft_constraints(self):
        """Asserts that the solution evaluation is correct"""

        problem = UCTP.parse(TOY_INSTANCE.splitlines())

        # Weights for soft constraints
        weights = (0, 0, 0, 0)
        evaluate = lambda solution: problem.evaluate(solution, weights)

        # A valid solution
        solution = {
            "SceCosC":  [("rA", 0, 0), ("rA", 1, 0), ("rA", 2, 0)],
            "ArcTec":   [("rB", 0, 1), ("rB", 1, 1), ("rB", 2, 1), ("rB", 3, 1)],
            "TecCos":   [("rC", 0, 2), ("rC", 1, 2), ("rC", 2, 2)],
            "GeoTec":   [("rA", 0, 3), ("rC", 1, 3), ("rC", 2, 3)],
        }
        assert evaluate(solution) == 0 

        
