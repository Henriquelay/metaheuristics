import networkx as nx
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
    """ UCTP can parse all instances in the instances folder """

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
    """ UCTP can parse toy intance successfully and no data is lost """

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
            assert {course.name for course in curriculum.courses.values()} == {"SceCosC", "ArcTec", "TecCos"}
        elif curriculum.name == "Cur2":
            assert {course.name for course in curriculum.courses.values()} == {"TecCos", "GeoTec"}
        else:
            assert False

    assert problem.rooms["rA"].capacity == 32
    assert problem.rooms["rB"].capacity == 50
    assert problem.rooms["rC"].capacity == 40

    assert {course.name for course in problem.curricula["Cur1"].courses.values()} == {"SceCosC", "ArcTec", "TecCos"}
    assert {course.name for course in problem.curricula["Cur2"].courses.values()} == {"TecCos", "GeoTec"}

    def assert_constraint(constraint: Constraint, course_name: str, day: int, period: int):
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
    """ Asserts graph generation for UCTP curricula """

    problem = UCTP.parse(TOY_INSTANCE.splitlines())
    graph = problem.to_graph()

    def edges_in_clique(size: int) -> int:
        return size * (size - 1) // 2

    assert len(graph.edges("GeoTec")) == 1
    assert len(graph.edges("TecCos")) == 3
    assert len(graph.edges("ArcTec")) == 2
    assert len(graph.edges("SceCosC")) == 2

    assert len(graph.nodes) == 4
    assert len(graph.edges) == edges_in_clique(3) + edges_in_clique(2)
    
    cliques = nx.find_cliques(graph)
    assert sum(1 for _ in cliques) == 2
