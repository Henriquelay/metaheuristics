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
Geotec Scarlatti 3 4 18

ROOMS:
rA 32
rB 50
rC 40

CURRICULA:
Cur1 3 SceCosC ArcTec TecCos
Cur2 2 TecCos Geotec

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
            assert len(problem.courses) > 0
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
    assert len(problem.courses) == 4
    assert len(problem.rooms) == 3
    assert len(problem.curricula) == 2
    assert len(problem.constraints) == 8

    courses_names = {course.name for course in problem.courses.values()}
    assert courses_names == {"SceCosC", "ArcTec", "TecCos", "Geotec"}

    rooms_names = {room.name for room in problem.rooms.values()}
    assert rooms_names == {"rA", "rB", "rC"}

    curricula_names = {curriculum.name for curriculum in problem.curricula.values()}
    assert curricula_names == {"Cur1", "Cur2"}

    assert problem.courses["SceCosC"].lectures == 3
    assert problem.courses["SceCosC"].min_working_days == 3
    assert problem.courses["SceCosC"].students == 30

    assert problem.courses["ArcTec"].lectures == 4
    assert problem.courses["ArcTec"].min_working_days == 3
    assert problem.courses["ArcTec"].students == 42

    assert problem.courses["TecCos"].lectures == 3
    assert problem.courses["TecCos"].min_working_days == 4
    assert problem.courses["TecCos"].students == 40

    assert problem.courses["Geotec"].lectures == 3
    assert problem.courses["Geotec"].min_working_days == 4
    assert problem.courses["Geotec"].students == 18

    assert problem.rooms["rA"].capacity == 32
    assert problem.rooms["rB"].capacity == 50
    assert problem.rooms["rC"].capacity == 40

    assert {course.name for course in problem.curricula["Cur1"].courses.values()} == {"SceCosC", "ArcTec", "TecCos"}
    assert {course.name for course in problem.curricula["Cur2"].courses.values()} == {"TecCos", "Geotec"}

    def assert_constraint(constraint: Constraint, course_name: str, period: int, day: int):
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
