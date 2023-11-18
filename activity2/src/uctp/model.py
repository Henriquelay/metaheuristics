from __future__ import annotations

from enum import Enum
from math import inf
from typing import Self, Sequence
from weakref import ref

from uctp.instance_parser import parse_int, parse_word, skip_white_lines
from networkx import Graph


class Room:
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

        self.constraints = []

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

        from uctp.instance_parser import keyword

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
                raise Exception(f"Expected end of line. Found {line}.")
            courses[course.name] = course
            body = body[1:]

        body = skip_white_lines(body)
        rooms = {}
        keyword(body[0], "ROOMS:")
        body = body[1:]
        for _ in range(rooms_amount):
            room, line = Room.parse(body[0])
            if line:
                raise Exception(f"Expected end of line. Found {line}.")
            rooms[room.name] = room
            body = body[1:]

        body = skip_white_lines(body)
        curricula = {}
        keyword(body[0], "CURRICULA:")
        body = body[1:]
        for _ in range(curricula_amount):
            curriculum, line = Curriculum.parse(body[0], courses)
            if line:
                raise Exception(f"Expected end of line. Found {line}.")
            curricula[curriculum.name] = curriculum
            body = body[1:]

        body = skip_white_lines(body)
        constraints = []
        keyword(body[0], "UNAVAILABILITY_CONSTRAINTS:")
        body = body[1:]
        for _ in range(constraints_amount):
            constraint, line = Constraint.parse(body[0], courses)
            if line:
                raise Exception(f"Expected end of line. Found {line}.")
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

        def add_edge(course1: str, course2: str) -> None:
            """Adds an edge between two courses. If one already exists, adds `1` to its weight."""

            try:
                graph.add_edge(course1, course2, weight=1)
            except KeyError:
                graph.edges[course1, course2]["weight"] += 1

        graph = Graph()
        for curriculum in self.curricula.values():
            graph.add_node(curriculum.name, color="curriculum")

            for course in curriculum.courses.values():
                try:
                    node = graph.nodes[course.name]
                    # add students info to course
                    node["students"].append(course.students)
                except KeyError:
                    # add course to graph
                    graph.add_node(
                        course.name,
                        color="course",
                        students=[course.students],
                    )
                finally:
                    # add curriculum to course
                    graph.add_edge(curriculum.name, course.name)

                try:
                    node = graph.nodes[course.teacher]
                except KeyError:
                    # add teacher to graph
                    graph.add_node(
                        course.teacher,
                        color="teacher",
                    )
                finally:
                    # add course to teacher
                    graph.add_edge(course.name, course.teacher)

        for room in self.rooms.values():
            for day in range(self.days):
                for period in range(self.periods_per_day):
                    graph.add_node(
                        f"{room.name}-{day}-{period}",
                        color="room-period",
                        capacity=room.capacity,
                    )

        return graph

    def evaluate_solution(
        self, solution: Graph, weights: tuple[float, float, float, float]
    ) -> float:
        """Evaluates a graph solution for UCTP and returns a score for the weighted number of rule violations. Returns the score."""

        # Checking hard violations

        for node in solution.nodes.data():
            # All courses of a discipline must be alocated, and in different periods.
            # This means that the number of edges between courses and room-periods must be equal to the number of lectures of the course.
            if node.color == "course":
                edge_count = sum([1 for _ in solution.neighbors(node)])
                expected_count = sum(
                    [
                        curriculum.courses[node].lectures
                        for curriculum in self.curricula.values()
                    ]
                )
                if edge_count != expected_count:
                    return inf

            # Two courses cannot be allocated in the same room-period.
            # This means that the number of edges between room-periods and courses must be less than or equal to 1.
            elif node.color == "room-period":
                edge_count = sum([1 for _ in solution.neighbors(node)])
                if edge_count > 1:
                    return inf

            # All courses from the same curricula, or teached by the same teacher must be allocated in different periods.
            # This means that the number of 

        return inf


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
