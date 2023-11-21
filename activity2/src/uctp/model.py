"""This module contains the model for the University Course Timetabling Problem."""

from __future__ import annotations
from enum import Enum

from typing import Self, Sequence
from weakref import ref

from networkx import Graph

from uctp.instance_parser import parse_int, parse_word, skip_white_lines, keyword

TIME_SLOT_SEPARATOR = "-"


def format_room_period_name(room: str, day: int, period: int) -> str:
    """Returns a string representing a room-day-period."""

    return f"{room}{TIME_SLOT_SEPARATOR}{day}{TIME_SLOT_SEPARATOR}{period}"


class Room:
    """A room in the university."""

    def __init__(self, name: str, capacity: int) -> None:
        self.name = name
        self.capacity = capacity

    def __str__(self) -> str:
        return f"""Room(Name = {self.name}, Capacity = {self.capacity})"""

    @classmethod
    def parse(cls, line: str) -> tuple[Self, str]:
        """Parses a room from a line, removing it from the line."""

        name, line = parse_word(line)
        capacity, line = parse_int(line)
        return cls(name, capacity), line


class Course:
    """A course in the university."""

    def __init__(
        self,
        name: str,
        teacher: str,
        lectures: int,
        min_working_days: int,
        students: int,
    ) -> None:
        self.name = name
        self.teacher = teacher
        self.lectures = lectures
        self.min_working_days = min_working_days
        self.students = students

        self.constraints: list[Constraint] = []

    def __str__(self) -> str:
        return f"""Course(\
Name = {self.name},\
Teacher = {self.teacher},\
Lectures = {self.lectures},\
MinWorkingDays = {self.min_working_days},\
Students = {self.students},\
Constraints = {[v.__str__() for v in self.constraints]}\
)"""

    def add_constraint(self, constraint: Constraint):
        """Adds a constraint to the course."""
        self.constraints.append(constraint)

    @classmethod
    def parse(cls, line: str) -> tuple[Self, str]:
        """Parses a course from a line, removing it from the line."""

        name, line = parse_word(line)
        teacher, line = parse_word(line)
        lectures, line = parse_int(line)
        min_working_days, line = parse_int(line)
        students, line = parse_int(line)
        return cls(name, teacher, lectures, min_working_days, students), line


class Constraint:
    """A constraint for a course."""

    def __init__(self, course: Course, day: int, period: int) -> None:
        self.course = ref(course)
        self.day = day
        self.period = period
        course.add_constraint(self)

    def __str__(self) -> str:
        course = self.course()
        if course:
            return f"""Constraint(\
Course = @|{course.name}|,\
Day = {self.day},\
Period = {self.period}\
)"""
        return f"""Constraint(\
Course = @|{course}|,\
Day = {self.day},\
Period = {self.period}\
)"""

    @classmethod
    def parse(cls, line: str, courses: dict[str, Course]) -> tuple[Self, str]:
        """Parses a constraint from a line, removing it from the line."""

        word, line = parse_word(line)
        course = courses[word]
        day, line = parse_int(line)
        period, line = parse_int(line)
        return cls(course, day, period), line


class Curriculum:
    """A curriculum in the university."""

    def __init__(self, name: str, courses: list[Course]) -> None:
        self.name = name
        self.courses: dict[str, Course] = {}
        for course in courses:
            self.courses[course.name] = course

    def __str__(self) -> str:
        return f"""Curriculum(\
                Name = {self.name},\
                Courses = {[(k, v.__str__()) for k, v in self.courses.items()]}\
            )"""

    @classmethod
    def parse(cls, line: str, courses: dict[str, Course]) -> tuple[Self, str]:
        """Parses a curricula from a line, removing it from the line."""

        name, line = parse_word(line)
        classes, line = parse_int(line)
        curriculum_courses = []
        for _ in range(classes):
            course_name, line = parse_word(line)
            curriculum_courses.append(courses[course_name])

        return cls(name, curriculum_courses), line


class UCTP:
    """A University Course Timetabling Problem instance."""

    class Colors(Enum):
        """Colors for the graph representation of the problem."""

        COURSE = "course"
        ROOM = "room-day-period"

    def __init__(
        self,
        name: str,
        days: int,
        periods_per_day: int,
        rooms: dict[str, Room],
        curricula: dict[str, Curriculum],
        constraints: list[Constraint],
    ) -> None:
        self.name = name
        self.days = days
        self.periods_per_day = periods_per_day
        self.rooms = rooms
        self.curricula = curricula
        self.constraints = constraints
        self.courses = {
            course.name: course
            for curriculum in curricula.values()
            for course in curriculum.courses.values()
        }
        self.teachers = {course.teacher for course in self.courses.values()}

    def __str__(self) -> str:
        return f"""UCTP(\
Name = {self.name}\
Days = {self.days}\
PeriodsPerDay = {self.periods_per_day}\
Rooms = {[(k, v.__str__()) for k, v in self.rooms.items()]}\
Curricula = {[(k, v.__str__()) for k, v in self.curricula.items()]}\
Constraints = {[v.__str__() for v in self.constraints]}\
)"""

    @classmethod
    def parse(cls, body: Sequence[str]) -> Self:
        """Parses a whole instance definition from a list of lines."""

        line = keyword(body[0], "Name: ")
        name, _ = parse_word(line)

        line = keyword(body[1], "Courses: ")
        courses_amount, _ = parse_int(line)

        line = keyword(body[2], "Rooms: ")
        rooms_amount, _ = parse_int(line)

        line = keyword(body[3], "Days: ")
        days, _ = parse_int(line)

        line = keyword(body[4], "Periods_per_day: ")
        periods_per_day, _ = parse_int(line)

        line = keyword(body[5], "Curricula: ")
        curricula_amount, _ = parse_int(line)

        line = keyword(body[6], "Constraints: ")
        constraints_amount, _ = parse_int(line)

        body = body[7:]

        body = skip_white_lines(body)
        courses = {}
        keyword(body[0], "COURSES:")
        body = body[1:]
        for _ in range(courses_amount):
            course, line = Course.parse(body[0])
            if line:
                raise ValueError(f"Expected end of line. Found {line}.")
            courses[course.name] = course
            body = body[1:]

        body = skip_white_lines(body)
        rooms = {}
        keyword(body[0], "ROOMS:")
        body = body[1:]
        for _ in range(rooms_amount):
            room, line = Room.parse(body[0])
            if line:
                raise ValueError(f"Expected end of line. Found {line}.")
            rooms[room.name] = room
            body = body[1:]

        body = skip_white_lines(body)
        curricula = {}
        keyword(body[0], "CURRICULA:")
        body = body[1:]
        for _ in range(curricula_amount):
            curriculum, line = Curriculum.parse(body[0], courses)
            if line:
                raise ValueError(f"Expected end of line. Found {line}.")
            curricula[curriculum.name] = curriculum
            body = body[1:]

        body = skip_white_lines(body)
        constraints = []
        keyword(body[0], "UNAVAILABILITY_CONSTRAINTS:")
        body = body[1:]
        for _ in range(constraints_amount):
            constraint, line = Constraint.parse(body[0], courses)
            if line:
                raise ValueError(f"Expected end of line. Found {line}.")
            constraints.append(constraint)
            body = body[1:]

        return cls(
            name,
            days,
            periods_per_day,
            rooms,
            curricula,
            constraints,
        )

    def to_graph(self) -> Graph:
        """Returns a graph base representation of the problem, with no solutions drawn."""

        graph = Graph()
        for course in self.courses:
            # add course to graph
            graph.add_node(
                course,
                color=self.Colors.COURSE,
            )

        for node_name in [
            format_room_period_name(room.name, day, period)
            for room in self.rooms.values()
            for day in range(self.days)
            for period in range(self.periods_per_day)
        ]:
            graph.add_node(
                node_name,
                color=self.Colors.ROOM,
            )

        return graph

    def solution_to_graph(
        self, solution: dict[str, list[tuple[str, int, int]]]
    ) -> Graph:
        """Returns a graph base representation of the problem, with the solution drawn."""

        base_graph = self.to_graph()

        for course, room_time_slots in solution.items():
            for room, day, period in room_time_slots:
                base_graph.add_edge(
                    course,
                    format_room_period_name(room, day, period),
                )

        return base_graph

    def best_neighbor(self, solution: Graph, neighborhood_size: int) -> Graph:
        """Generates graphs neighboring the passed solution, and returns the best one."""
        # TODO 
        return solution

    def evaluate_dict(
        self,
        solution_dict: dict[str, list[tuple[str, int, int]]],
        weights: tuple[
            tuple[float, float, float, float], tuple[float, float, float, float]
        ],
    ) -> tuple[float, set[str]]:
        """Evaluates a graph solution for UCTP and returns a score for the weighted number of rule violations. Returns the score."""
        graph = self.solution_to_graph(solution_dict)
        return self.evaluate(graph, weights)

    def evaluate(
        self,
        solution: Graph,
        weights: tuple[
            tuple[float, float, float, float], tuple[float, float, float, float]
        ],
    ) -> tuple[float, set[str]]:
        """Evaluates a graph solution for UCTP and returns a score for the weighted number of rule violations. Returns the score."""
        # TODO convert to matrix representation evaluation

        nodes_data = solution.nodes.data()
        # nodes: dict[str, dict[str, Any]] = {node: data for node, data in nodes_data}

        # List of Rooms and timeslots assigned to each course
        course_timeslots: dict[str, list[tuple[Room, int, int]]] = {}
        # List of timeslots assigned to each teacher
        teacher_timeslots: dict[str, list[tuple[int, int]]] = {}
        # List of courses assigned to each timeslot
        timeslot_courses: dict[tuple[int, int], list[tuple[Room, Course]]] = {}
        # List of timeslots assigned to each curriculum
        curriculum_timeslots: dict[str, list[tuple[int, int]]] = {}

        properties: set[str] = set()

        score = 0.0

        for node_name, node_data in nodes_data:
            if node_data["color"] == self.Colors.COURSE:
                course = self.courses[node_name]
                course_curricula = [
                    curriculum
                    for curriculum in self.curricula.values()
                    if course.name in curriculum.courses.keys()
                ]
                timeslots: list[str] = list(solution.neighbors(course.name))
                for timeslot in timeslots:
                    (room, day, period) = timeslot.split(TIME_SLOT_SEPARATOR)
                    day = int(day)
                    period = int(period)
                    room = self.rooms[room]

                    if course.name not in course_timeslots:
                        course_timeslots[course.name] = [(room, day, period)]
                    else:
                        course_timeslots[course.name].append((room, day, period))

                    if course.teacher not in teacher_timeslots:
                        teacher_timeslots[course.teacher] = [(day, period)]
                    else:
                        teacher_timeslots[course.teacher].append((day, period))

                    if (day, period) not in timeslot_courses:
                        timeslot_courses[(day, period)] = [(room, course)]
                    else:
                        timeslot_courses[(day, period)].append((room, course))

                    for curriculum in course_curricula:
                        if curriculum.name not in curriculum_timeslots:
                            curriculum_timeslots[curriculum.name] = [(day, period)]
                        else:
                            curriculum_timeslots[curriculum.name].append((day, period))

            elif node_data["color"] == self.Colors.ROOM:
                pass
            else:
                raise ValueError(f"Invalid node color: {node_data['color']}")

        for course, periods in course_timeslots.items():
            course = self.courses[course]

            # H1 - Lectures: All lectures of a course must be alocated, and in  different periods. Each lecture not allocated is a violation. Each lecture more than one allocated on the same period is also a violation.
            # if some lecture is not allocated, then there is a violation
            if len(periods) < course.lectures:
                score += weights[0][0] * (course.lectures - len(periods))
                properties.add("H1")

            # if lectures are allocated in the same period, then there is a violation
            periods_stripped_room = [(day, period) for _, day, period in periods]
            score += weights[0][0] * (
                len(periods_stripped_room) - len(set(periods_stripped_room))
            )
            if len(periods_stripped_room) != len(set(periods_stripped_room)):
                properties.add("H1")

            # H4 - Unavailability: If a course is assigned to slot that it is unavailable, It is a violation.
            constraints = {
                (constraint.day, constraint.period) for constraint in course.constraints
            }
            intersection = constraints.intersection(set(periods_stripped_room))
            score += weights[0][3] * len(intersection)
            if len(intersection) > 0:
                properties.add("H4")

            # S2 - Minimum working days: The number of days where at least one lecture is scheduled must be greater or equal than the minimum working days of the course. Each day below the minimum is a violation.
            days = {day for day, _ in periods_stripped_room}
            if len(days) < course.min_working_days:
                score += weights[1][1] * (course.min_working_days - len(days))
                properties.add("S2")

            # S4 - Room stability: All lectures of a course must be allocated in the same room. Each lecture not allocated in the same room is a violation.
            rooms_of_lecture = len({room for room, _, _ in periods})
            score += weights[1][3] * (rooms_of_lecture - 1)
            if rooms_of_lecture > 1:
                properties.add("S4")

        # H3 - Conflits: Lectures of courses in the same curriculum, or teached by the same teacher must be allocated in different periods. Each lecture allocated in the same period is a violation.
        for periods in teacher_timeslots.values():
            score += weights[0][2] * (len(periods) - len(set(periods)))
            if len(periods) != len(set(periods)):
                properties.add("H3")

        for periods in curriculum_timeslots.values():
            score += weights[0][2] * (len(periods) - len(set(periods)))
            if len(periods) != len(set(periods)):
                properties.add("H3")

            # S3 - Curriculum compactness: All lectures of a curriculum must have as few isolated lectures as possible. Each lecture that is not adjacent to another lecture in the same curriculum is a violation.
            in_gap = False
            last_day = -1
            last_period = -1
            for day, period in sorted(periods):
                if day != last_day:
                    in_gap = False
                    last_day = day
                else:
                    if period > last_period + 1 and not in_gap:
                        # Skipped a period
                        in_gap = True
                    elif period > last_period + 1 and in_gap:
                        # Last period was a gap, and this is a gap too, so it's a violation
                        score += weights[1][2]
                        properties.add("S3")
                    else:
                        in_gap = False
                last_period = period

        # H2 - Room occupancy: Two lectures can't be allocated in the same room-period. Each extra lecture allocated in the same room-period is a violation.
        for timeslot, room_courses in timeslot_courses.items():
            # If Room repeats in the list, then there is a violation
            rooms = [room for room, _ in room_courses]
            score += weights[0][1] * (len(rooms) - len(set(rooms)))
            if len(rooms) != len(set(rooms)):
                properties.add("H2")

            # S1 - Room capacity: The number of students in a room-period can't exceed the capacity of the room. Each student over the capacity is a violation.
            for room, course in room_courses:
                if course.students > room.capacity:
                    score += weights[1][0] * (course.students - room.capacity)
                    properties.add("S1")

        return (score, properties)


# Name: Toy
# Courses: 4
# Rooms: 3
# Days: 5
# Periods_per_day: 4
# Curricula: 2
# Constraints: 8

# COURSES:
# SceCosC Ocra 3 3 30
# ArcTec Indaco 4 3 42
# TecCos Rosa 3 4 40
# Geotec Scarlatti 3 4 18

# ROOMS:
# rA 32
# rB 50
# rC 40

# CURRICULA:
# Cur1 3 SceCosC ArcTec TecCos
# Cur2 2 TecCos Geotec

# UNAVAILABILITY_CONSTRAINTS:
# TecCos 2 0
# TecCos 2 1
# TecCos 3 2
# TecCos 3 3
# ArcTec 4 0
# ArcTec 4 1
# ArcTec 4 2
# ArcTec 4 3

# END.
