"""This module contains the model for the University Course Timetabling Problem."""

from __future__ import annotations
from enum import Enum
from pprint import pprint

from typing import Any, Self, Sequence
from weakref import ref

from networkx import Graph

from uctp.instance_parser import parse_int, parse_word, skip_white_lines, keyword

TIME_SLOT_SEPARATOR = "-"


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
        for curriculum in self.curricula.values():
            for course in curriculum.courses.values():
                try:
                    graph.nodes[course.name]
                except KeyError:
                    # add course to graph
                    graph.add_node(
                        course.name,
                        color=self.Colors.COURSE,
                    )

        for room in self.rooms.values():
            for day in range(self.days):
                for period in range(self.periods_per_day):
                    graph.add_node(
                        f"{room.name}{TIME_SLOT_SEPARATOR}{day}{TIME_SLOT_SEPARATOR}{period}",
                        color=self.Colors.ROOM,
                        capacity=room.capacity,
                    )

        return graph

    def solution_to_graph(
        self, solution: dict[str, list[tuple[str, int, int]]]
    ) -> Graph:
        """Returns a graph base representation of the problem, with the solution drawn."""

        base_graph = self.to_graph()

        for course, lectures in solution.items():
            for room, day, period in lectures:
                base_graph.add_edge(
                    course,
                    f"{room}{TIME_SLOT_SEPARATOR}{day}{TIME_SLOT_SEPARATOR}{period}",
                )

        return base_graph

    def evaluate(
        self,
        solution_dict: dict[str, list[tuple[str, int, int]]],
        weights: tuple[float, float, float, float],
    ) -> float:
        """Evaluates a graph solution for UCTP and returns a score for the weighted number of rule violations. Returns the score."""

        solution = self.solution_to_graph(solution_dict)

        nodes_data = solution.nodes.data()
        nodes: dict[str, dict[str, Any]] = {node: data for node, data in nodes_data}

        score = 0.0

        for node_name, node_data in nodes.items():
            if node_data["color"] == self.Colors.COURSE:
                course = self.courses[node_name]
                time_slots: list[tuple[str, int, int]] = [
                    (
                        slot.split(TIME_SLOT_SEPARATOR)[0],
                        int(slot.split(TIME_SLOT_SEPARATOR)[1]),
                        int(slot.split(TIME_SLOT_SEPARATOR)[2]),
                    )
                    for slot in solution.neighbors(node_name)
                ]

                # H1 All lectures of a course must be alocated, and in different periods.
                # This means that the number of edges between courses and room-periods must be equal to the number of lectures of the course.
                if len(time_slots) != course.lectures:
                    raise ValueError(
                        "Invalid solution. H1 violated due to count of lectures not equal to count of room-day-periods."
                    )

                assigned_rooms: set[str] = set()
                assigned_time_slots: set[tuple[int, int]] = set()
                for room, day, period in time_slots:
                    # H4 if a course is assigned to slot that it is unavailable, then the solution is infeasible.
                    # This means that the number of edges between courses and day-periods to which it is unavailable must be equal to 0.
                    if (day, period) in course.constraints:
                        raise ValueError(
                            "Invalid solution. H4 violated due to course assigned in an unavailable slot."
                        )

                    if room not in assigned_rooms:
                        # S1: Room capacity, For each course, the number of students that attend the course must be less than or equal  to the capacity of the room. Each student above the capacity of the room is a violation.
                        room_capacity = self.rooms[room].capacity
                        if course.students > room_capacity:
                            score += weights[0] * (course.students - room_capacity)
                        assigned_rooms.add(room)

                    if (day, period) in assigned_time_slots:
                        raise ValueError(
                            "Invalid solution. H1 violated due to course assigned in two different rooms in the same day-period."
                        )
                    assigned_time_slots.add((day, period))

                # S4: Room stability, For each course, the number of different rooms in which the course is taught must be as closely as possible to 1. For each course, there is a violation for every room in which the course is taught, except the first one.
                score += weights[3] * (len(assigned_rooms) - 1)

                # S2: Minimum working days, For each course, the number of days in which the course is taught must be greater than or equal to the minimum working days of the course. Each day below the minimum working days of the course is a violation.
                days_assigned = len(set([day for room, day, period in time_slots]))
                if days_assigned < course.min_working_days:
                    score += weights[1] * (course.min_working_days - days_assigned)

            # H2 Two courses cannot be allocated in the same room-period.
            # This means that the number of edges between room-periods and courses must be less than or equal to 1.
            elif node_data["color"] == self.Colors.ROOM:
                (room, day, period) = node_name.split(TIME_SLOT_SEPARATOR)
                day = int(day)
                period = int(period)
                assigned_courses: list[str] = list(solution.neighbors(node_name))
                teacher_periods: dict[str, list[tuple[int, int]]] = {}
                if len(assigned_courses) > 1:
                    raise ValueError(
                        "Invalid solution. H2 violated due to two courses assigned in the same room-day-period."
                    )
                elif len(assigned_courses) == 1:
                    assigned_course = self.courses[assigned_courses[0]]
                    # H3 All courses from the same curricula, or teached by the same teacher must be allocated in different periods.
                    # This means that the number of edges between courses of a teacher or curricula to periods must never overlap day-periods.
                    teacher = assigned_course.teacher
                    if teacher not in teacher_periods:
                        teacher_periods[teacher] = [(day, period)]
                    elif (day, period) in teacher_periods[teacher]:
                        raise ValueError(
                            "Invalid solution. H3 violated due to two courses teached by the same teacher in the same day-period."
                        )
                    else:
                        teacher_periods[teacher].append((day, period))

            # S3: Curriculum compactness, For each curriculum, the number of periods in a day in which the courses of the curriculum are taught must be as closely as possible. For each curriculum, there is a violation for every course which is not adjacent to another course of the same curriculum in the same day.
            for _ in self.curricula.values():
                assigned_slots_curriculum: dict[int, list[int]] = {}
                for course in self.courses.values():
                    for neighbor in solution.neighbors(course.name):
                        [
                            _room_name,
                            room_day,
                            room_period,
                        ] = neighbor.split(TIME_SLOT_SEPARATOR)
                        room_day = int(room_day)
                        room_period = int(room_period)
                        if room_day not in assigned_slots_curriculum:
                            assigned_slots_curriculum[room_day] = [room_period]
                        else:
                            # H3 All courses from the same curricula, or teached by the same teacher must be allocated in different periods.
                            if room_period not in assigned_slots_curriculum[room_day]:
                                assigned_slots_curriculum[room_day].append(room_period)
                            else:
                                pprint((room_day, room_period))
                                pprint(assigned_slots_curriculum)
                                raise ValueError(
                                    "Invalid solution. H3 violated due to course in the same curriculum being teached at the same day-period."
                                )

                # This means that if there are courses in the same curriculum that are not adjacent in the same day, then there is a violation.
                for day, periods in assigned_slots_curriculum.items():
                    periods.sort()
                    for i in range(len(periods) - 1):
                        if periods[i + 1] - periods[i] > 1:
                            score += weights[2]

        return score


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
