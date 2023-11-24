"""Tests for the UCTP model"""

from copy import copy
from pprint import pprint

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
        with open(path, "r", encoding="utf8") as file:
            print(f"Parsing {path}")
            problem = UCTP.parse(file.readlines())
            assert problem.name is not None
            assert problem.days is not None
            assert problem.periods_per_day is not None
            assert len(problem.rooms) > 0
            assert len(problem.curricula) > 0
            assert len(problem.constraints) > 0
        file.close()


def test_uctp_parsing():
    """UCTP can parse toy intance successfully and no data is lost"""

    problem = UCTP.parse(TOY_INSTANCE.splitlines())
    assert problem.name == "Toy"
    assert problem.days == 5
    assert problem.periods_per_day == 4
    assert len(problem.rooms) == 3
    assert len(problem.curricula) == 2
    assert len(problem.constraints) == 8

    assert problem.room_names == ["rA", "rB", "rC"]

    curricula_names = [curriculum.name for curriculum in problem.curricula]
    assert curricula_names == ["Cur1", "Cur2"]

    for curriculum in problem.curricula:
        if curriculum.name == "Cur1":
            assert [course.name for course in curriculum.courses] == [
                "SceCosC",
                "ArcTec",
                "TecCos",
            ]
        elif curriculum.name == "Cur2":
            assert [course.name for course in curriculum.courses] == [
                "TecCos",
                "GeoTec",
            ]
        else:
            assert False

    assert [room.capacity for room in problem.rooms] == [32, 50, 40]

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


def test_uctp_graph():
    """Asserts graph generation for UCTP curricula"""

    problem = UCTP.parse(TOY_INSTANCE.splitlines())
    graph = problem.to_graph()

    assert graph == [
        [0 for _ in range(len(problem.courses))]
        for _ in range(len(problem.rooms) * problem.days * problem.periods_per_day)
    ]


def test_uctp_solution_drawing():
    """Asserts that the solution drawing is correct"""

    problem = UCTP.parse(TOY_INSTANCE.splitlines())

    solution = {
        "SceCosC": [("rA", 0, 0), ("rA", 1, 0), ("rA", 2, 0)],
        "ArcTec": [("rB", 0, 1), ("rB", 1, 1), ("rB", 2, 1), ("rB", 3, 1)],
        "TecCos": [("rC", 0, 2), ("rC", 1, 2), ("rC", 2, 2)],
        "GeoTec": [("rA", 0, 3), ("rC", 1, 3), ("rC", 2, 3)],
    }

    drawing = problem.solution_to_graph(solution)

    expected = [
        # SceCos; ArcTec; TecCos; GeoTec
        [1, 0, 0, 0],  # rA day 0 period 0
        [0, 0, 0, 0],  # rA day 0 period 1
        [0, 0, 0, 0],  # rA day 0 period 2
        [0, 0, 0, 1],  # rA day 0 period 3
        [1, 0, 0, 0],  # rA day 1 period 0
        [0, 0, 0, 0],  # rA day 1 period 1
        [0, 0, 0, 0],  # rA day 1 period 2
        [0, 0, 0, 0],  # rA day 1 period 3
        [1, 0, 0, 0],  # rA day 2 period 0
        [0, 0, 0, 0],  # rA day 2 period 1
        [0, 0, 0, 0],  # rA day 2 period 2
        [0, 0, 0, 0],  # rA day 2 period 3
        [0, 0, 0, 0],  # rA day 3 period 0
        [0, 0, 0, 0],  # rA day 3 period 1
        [0, 0, 0, 0],  # rA day 3 period 2
        [0, 0, 0, 0],  # rA day 3 period 3
        [0, 0, 0, 0],  # rA day 4 period 0
        [0, 0, 0, 0],  # rA day 4 period 1
        [0, 0, 0, 0],  # rA day 4 period 2
        [0, 0, 0, 0],  # rA day 4 period 3
        [0, 0, 0, 0],  # rB day 0 period 0
        [0, 1, 0, 0],  # rB day 0 period 1
        [0, 0, 0, 0],  # rB day 0 period 2
        [0, 0, 0, 0],  # rB day 0 period 3
        [0, 0, 0, 0],  # rB day 1 period 0
        [0, 1, 0, 0],  # rB day 1 period 1
        [0, 0, 0, 0],  # rB day 1 period 2
        [0, 0, 0, 0],  # rB day 1 period 3
        [0, 0, 0, 0],  # rB day 2 period 0
        [0, 1, 0, 0],  # rB day 2 period 1
        [0, 0, 0, 0],  # rB day 2 period 2
        [0, 0, 0, 0],  # rB day 2 period 3
        [0, 0, 0, 0],  # rB day 3 period 0
        [0, 1, 0, 0],  # rB day 3 period 1
        [0, 0, 0, 0],  # rB day 3 period 2
        [0, 0, 0, 0],  # rB day 3 period 3
        [0, 0, 0, 0],  # rB day 4 period 0
        [0, 0, 0, 0],  # rB day 4 period 1
        [0, 0, 0, 0],  # rB day 4 period 2
        [0, 0, 0, 0],  # rB day 4 period 3
        [0, 0, 0, 0],  # rC day 0 period 0
        [0, 0, 0, 0],  # rC day 0 period 1
        [0, 0, 1, 0],  # rC day 0 period 2
        [0, 0, 0, 0],  # rC day 0 period 3
        [0, 0, 0, 0],  # rC day 1 period 0
        [0, 0, 0, 0],  # rC day 1 period 1
        [0, 0, 1, 0],  # rC day 1 period 2
        [0, 0, 0, 1],  # rC day 1 period 3
        [0, 0, 0, 0],  # rC day 2 period 0
        [0, 0, 0, 0],  # rC day 2 period 1
        [0, 0, 1, 0],  # rC day 2 period 2
        [0, 0, 0, 1],  # rC day 2 period 3
        [0, 0, 0, 0],  # rC day 3 period 0
        [0, 0, 0, 0],  # rC day 3 period 1
        [0, 0, 0, 0],  # rC day 3 period 2
        [0, 0, 0, 0],  # rC day 3 period 3
        [0, 0, 0, 0],  # rB day 4 period 0
        [0, 0, 0, 0],  # rB day 4 period 1
        [0, 0, 0, 0],  # rB day 4 period 2
        [0, 0, 0, 0],  # rB day 4 period 3
    ]
    pprint(expected)

    assert drawing == expected


class TestEvaluation:
    """Tests for the evaluation of a solution"""

    hard_weights = (10, 11, 12, 13)
    soft_weights = (4, 3, 2, 1)
    problem = UCTP.parse(TOY_INSTANCE.splitlines())

    problem_soft = copy(problem)
    problem_soft.weights = ((0,0,0,0), soft_weights)

    problem_hard = problem
    problem_hard.weights = (hard_weights, (0,0,0,0))

    def test_evaluation_hard_constraints_ok(self):
        """Asserts that the solution evaluation is correct for a valid solution"""

        # A valid solution
        solution = {
            "SceCosC": [("rA", 0, 0), ("rA", 1, 0), ("rA", 2, 0)],
            "ArcTec": [("rB", 0, 1), ("rB", 1, 1), ("rB", 2, 1), ("rB", 3, 1)],
            "TecCos": [("rC", 0, 2), ("rC", 1, 2), ("rC", 2, 2)],
            "GeoTec": [("rA", 0, 3), ("rC", 1, 3), ("rC", 2, 3)],
        }
        assert self.problem_hard.evaluate_dict(solution)[0] == 0

    def test_evaluation_hard_constraints_h1(self):
        """Asserts that the solution evaluation is correct for solution that violates hard constraint H1"""

        # Missing a lecture
        solution = {
            "SceCosC": [("rA", 0, 0), ("rA", 1, 0)],
            "ArcTec": [("rB", 0, 1), ("rB", 1, 1), ("rB", 2, 1), ("rB", 3, 1)],
            "TecCos": [("rC", 0, 2), ("rC", 1, 2), ("rC", 2, 2)],
            "GeoTec": [("rA", 0, 3), ("rC", 1, 3), ("rC", 2, 3)],
        }
        assert self.problem_hard.evaluate_dict(solution)[0] == self.hard_weights[0]

        # Two lectures of the same course in the same day-period
        solution = {
            "SceCosC": [("rA", 0, 0), ("rA", 1, 0), ("rA", 1, 0)],
            "ArcTec": [("rB", 0, 1), ("rB", 1, 1), ("rB", 2, 1), ("rB", 3, 1)],
            "TecCos": [("rC", 0, 2), ("rC", 1, 2), ("rC", 2, 2)],
            "GeoTec": [("rA", 0, 3), ("rC", 1, 3), ("rC", 2, 3)],
        }
        assert self.problem_hard.evaluate_dict(solution)[0] == self.hard_weights[0]

    def test_evaluation_hard_constraints_h2(self):
        """Asserts that the solution evaluation is correct for solution that violates hard constraint H2"""

        # Two courses in the same room at the same time, different curriculum
        solution = {
            "SceCosC": [("rA", 0, 0), ("rA", 1, 0), ("rA", 2, 0)],
            "ArcTec": [("rB", 0, 1), ("rB", 1, 1), ("rB", 2, 1), ("rB", 3, 1)],
            "TecCos": [("rC", 0, 2), ("rC", 1, 2), ("rC", 2, 2)],
            "GeoTec": [("rA", 0, 3), ("rC", 1, 3), ("rA", 2, 0)],
        }
        assert self.problem_hard.evaluate_dict(solution)[0] == self.hard_weights[1]

    def test_evaluation_hard_constraints_h3(self):
        """Asserts that the solution evaluation is correct for solution that violates hard constraint H3"""

        # Two courses of the same curriculum in the same day-period
        solution = {
            "SceCosC": [("rA", 0, 0), ("rA", 1, 0), ("rA", 2, 0)],
            "ArcTec": [("rB", 0, 0), ("rB", 1, 1), ("rB", 2, 1), ("rB", 3, 1)],
            "TecCos": [("rC", 0, 2), ("rC", 1, 2), ("rC", 2, 2)],
            "GeoTec": [("rA", 0, 3), ("rC", 1, 3), ("rC", 2, 3)],
        }
        assert self.problem_hard.evaluate_dict(solution)[0] == self.hard_weights[2]

    def test_evaluation_hard_constraints_h4(self):
        """Asserts that the solution evaluation is correct for solution that violates hard constraint H4"""

        # A solution with a course in an unavailable period
        solution = {
            "SceCosC": [("rA", 0, 0), ("rA", 1, 0), ("rA", 2, 0)],
            "ArcTec": [("rB", 0, 1), ("rB", 1, 1), ("rB", 2, 1), ("rB", 4, 0)],
            "TecCos": [("rC", 0, 2), ("rC", 1, 2), ("rC", 2, 2)],
            "GeoTec": [("rA", 0, 3), ("rC", 1, 3), ("rC", 2, 3)],
        }
        assert self.problem_hard.evaluate_dict(solution)[0] == self.hard_weights[3]

    def test_evaluation_soft_constraints(self):
        """Asserts that the solution evaluation is correct for a valid solution with soft constraints weights"""

        # A optimal solution
        solution = {
            "SceCosC": [("rA", 0, 0), ("rA", 1, 0), ("rA", 2, 0)],
            "ArcTec": [("rB", 0, 1), ("rB", 1, 1), ("rB", 2, 1), ("rB", 3, 1)],
            "TecCos": [("rC", 0, 2), ("rC", 1, 2), ("rC", 2, 2)],
            "GeoTec": [("rA", 0, 3), ("rA", 1, 3), ("rA", 2, 3)],
        }
        assert self.problem_soft.evaluate_dict(solution) == (
            self.soft_weights[1] * 2,
            # Optimal solution
            ["S2", "S2"],
        )
