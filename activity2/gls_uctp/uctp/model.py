"""This module contains the model for the University Course Timetabling Problem."""

from __future__ import annotations
from collections import defaultdict
from enum import Enum
from random import randint
from typing import Self, Sequence

# from weakref import ref

from gls_uctp.uctp.instance_parser import (
    parse_int,
    parse_word,
    skip_white_lines,
    keyword,
)


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

    def has_constraint(self, day: int, period: int) -> bool:
        """Checks if the day and period are constrained for the course."""

        return any(
            constraint.day == day and constraint.period == period
            for constraint in self.constraints
        )

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
        self.day = day
        self.period = period
        course.add_constraint(self)

    def __str__(self) -> str:
        return f"""Constraint(\
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
        self.courses = courses

    def __str__(self) -> str:
        return f"""Curriculum(\
                Name = {self.name},\
                Courses = {self.courses}\
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


# A Solution for UCTP.
# Adjacency list of room_day_period -> course
type Solution = list[list[int]]

# Weights for the objective function
# (H1, H2, H3, H4), (S1, S2, S3, S4)
type Weights = tuple[tuple[int, int, int, int], tuple[int, int, int, int]]


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
        rooms: list[Room],
        curricula: list[Curriculum],
        constraints: list[Constraint],
    ) -> None:
        self.name = name
        self.days = days
        self.periods_per_day = periods_per_day
        self.rooms = rooms
        self.room_names = [room.name for room in rooms]
        self.curricula = curricula
        self.constraints = constraints
        self.courses = list(
            # Dedups in-place
            dict.fromkeys(
                course for curriculum in curricula for course in curriculum.courses
            )
        )
        self.teachers = list({course.teacher for course in self.courses})

        self.weights: Weights = ((0, 0, 0, 0), (1, 5, 2, 1))

    def __str__(self) -> str:
        return f"""UCTP(\
Name = {self.name}\
Days = {self.days}\
PeriodsPerDay = {self.periods_per_day}\
Rooms = {self.rooms}\
Curricula = {self.curricula}\
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
        rooms: list[Room] = []
        keyword(body[0], "ROOMS:")
        body = body[1:]
        for _ in range(rooms_amount):
            room, line = Room.parse(body[0])
            if line:
                raise ValueError(f"Expected end of line. Found {line}.")
            rooms.append(room)
            body = body[1:]

        body = skip_white_lines(body)
        curricula: list[Curriculum] = []
        keyword(body[0], "CURRICULA:")
        body = body[1:]
        for _ in range(curricula_amount):
            curriculum, line = Curriculum.parse(body[0], courses)
            if line:
                raise ValueError(f"Expected end of line. Found {line}.")
            curricula.append(curriculum)
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

    @classmethod
    def from_file(cls, path: str) -> Self:
        """Parses a whole instance definition that lives in the system file path given."""

        problem_instance = None
        with open(path, encoding="utf8") as file:
            lines = file.readlines()
            problem_instance = cls.parse(lines)
        file.close()
        return problem_instance

    def to_graph(self) -> Solution:
        """Returns a graph base representation of the problem, with no solutions drawn."""

        return [
            [0 for _ in range(len(self.courses))]
            for _ in range(len(self.rooms) * self.days * self.periods_per_day)
        ]

    def random_solution(self) -> Solution:
        """Returns a random solution for the problem. Tries a reasonably random and as valid solution as it can"""

        solution = self.to_graph()

        total_lectures = sum(course.lectures for course in self.courses)

        for _ in range(total_lectures):
            i = 0
            while True:
                i += 1
                period_index, course_index = self.random_valid_indexes(solution)
                if i == 50:
                    solution[period_index][course_index] += 1
                    break
                day = period_index // self.periods_per_day
                period = period_index % self.periods_per_day
                if (solution[period_index][course_index] < 1) and (
                    not self.courses[course_index].has_constraint(day, period)
                ):
                    solution[period_index][course_index] += 1
                    break

        return solution

    def solution_to_graph(
        self, solution: dict[str, list[tuple[str, int, int]]]
    ) -> Solution:
        """Returns a graph base representation of the problem, with the solution drawn."""

        base_solution = self.to_graph()

        for course_name, periods in solution.items():
            for room_name, day, period in periods:
                room_index = self.room_names.index(room_name)
                # Day and Period both starts at zero
                room_offset = room_index * self.days * self.periods_per_day
                day_offset = day * self.periods_per_day

                period_offset = room_offset + day_offset + period

                course_index = next(
                    i
                    for i, course in enumerate(self.courses)
                    if course.name == course_name
                )

                base_solution[period_offset][course_index] += 1

        return base_solution

    def random_valid_indexes(self, solution: Solution) -> tuple[int, int]:
        """Returns two random indexes for the solution variable."""

        while True:
            row = randint(0, len(solution) - 1)
            column = randint(0, len(solution[row]) - 1)

            # If the cell is contrained and zero, then regenerate
            if solution[row][column] == 0:
                day = row // self.periods_per_day
                period = row % self.periods_per_day
                if self.courses[column].has_constraint(day, period):
                    continue

            return (row, column)

    def lecture_move(self, solution: Solution) -> Solution:
        """Modify the solution variable to swap value from two random cells."""

        row1, column1 = self.random_valid_indexes(solution)
        row2, column2 = self.random_valid_indexes(solution)

        solution[row1][column1], solution[row2][column2] = (
            solution[row2][column2],
            solution[row1][column1],
        )

        return solution

    def neighbors(self, solution: Solution, neighborhood_size: int) -> list[Solution]:
        """Generates graphs neighboring the passed solution."""
        return [self.lecture_move(solution) for _ in range(neighborhood_size)]

    def evaluate_dict(
        self,
        solution_dict: dict[str, list[tuple[str, int, int]]],
    ) -> tuple[float, dict[str, int]]:
        """Evaluates a graph solution for UCTP and returns a score for the weighted number of rule violations. Returns the score."""
        graph = self.solution_to_graph(solution_dict)
        return self.evaluate(graph)

    def evaluate(
        self,
        solution: Solution,
    ) -> tuple[int, dict[str, int]]:
        """Evaluates a graph solution for UCTP and returns a score for the weighted number of rule violations. Returns the score."""

        # List of Rooms and timeslots assigned to each course
        course_timeslots: dict[int, list[tuple[Room, int, int]]] = defaultdict(list)
        # List of timeslots assigned to each teacher
        teacher_timeslots: dict[str, list[tuple[int, int]]] = defaultdict(list)
        # List of courses assigned to each timeslot
        timeslot_courses: dict[
            tuple[int, int], list[tuple[Room, Course]]
        ] = defaultdict(list)
        # List of timeslots assigned to each curriculum
        curriculum_timeslots: dict[str, list[tuple[int, int]]] = defaultdict(list)

        for course_index, course in enumerate(self.courses):
            assigned_timeslots = [
                index
                for index in range(len(solution))
                if solution[index][course_index] > 0
            ]

            timeslots = [
                # (room, day, period)
                (
                    slot // (self.days * self.periods_per_day),
                    (slot % (self.days * self.periods_per_day)) // self.periods_per_day,
                    (slot % (self.days * self.periods_per_day)) % self.periods_per_day,
                )
                for slot in assigned_timeslots
            ]

            for room, day, period in timeslots:
                room = self.rooms[room]

                course_timeslots[course_index].append((room, day, period))
                teacher_timeslots[course.teacher].append((day, period))
                timeslot_courses[(day, period)].append((room, course))

                curricula = [
                    curriculum
                    for curriculum in self.curricula
                    if course in curriculum.courses
                ]

                for curriculum in curricula:
                    curriculum_timeslots[curriculum.name].append((day, period))

        properties: dict[str, int] = defaultdict(int)

        score = 0

        for course_index, periods in course_timeslots.items():
            course = self.courses[course_index]

            # H1 - Lectures: All lectures of a course must be alocated, and in  different periods. Each lecture not allocated is a violation. Each lecture more than one allocated on the same period is also a violation.
            # if some lecture is not allocated, then there is a violation
            if len(periods) < course.lectures:
                score += self.weights[0][0] * (course.lectures - len(periods))
                properties["H1"] += 1

            # if lectures are allocated in the same period, then there is a violation
            periods_stripped_room = [(day, period) for _, day, period in periods]
            score += self.weights[0][0] * (
                len(periods_stripped_room) - len(set(periods_stripped_room))
            )
            if len(periods_stripped_room) != len(set(periods_stripped_room)):
                properties["H1"] += 1

            # H4 - Unavailability: If a course is assigned to slot that it is unavailable, It is a violation.
            constraints = {
                (constraint.day, constraint.period) for constraint in course.constraints
            }
            intersection = constraints.intersection(set(periods_stripped_room))
            score += self.weights[0][3] * len(intersection)
            if len(intersection) > 0:
                properties["H4"] += 1

            # S2 - Minimum working days: The number of days where at least one lecture is scheduled must be greater or equal than the minimum working days of the course. Each day below the minimum is a violation.
            days = {day for day, _ in periods_stripped_room}
            if len(days) < course.min_working_days:
                score += self.weights[1][1] * (course.min_working_days - len(days))
                properties["S2"] += 1

            # S4 - Room stability: All lectures of a course must be allocated in the same room. Each lecture not allocated in the same room is a violation.
            rooms_of_lecture = len({room for room, _, _ in periods})
            score += self.weights[1][3] * (rooms_of_lecture - 1)
            if rooms_of_lecture > 1:
                properties["S4"] += 1

        # H3 - Conflits: Lectures of courses in the same curriculum, or teached by the same teacher must be allocated in different periods. Each lecture allocated in the same period is a violation.
        for periods in teacher_timeslots.values():
            score += self.weights[0][2] * (len(periods) - len(set(periods)))
            if len(periods) != len(set(periods)):
                properties["H3"] += 1

        for periods in curriculum_timeslots.values():
            score += self.weights[0][2] * (len(periods) - len(set(periods)))
            if len(periods) != len(set(periods)):
                properties["H3"] += 1

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
                        score += self.weights[1][2]
                        properties["S3"] += 1
                    else:
                        in_gap = False
                last_period = period

        # H2 - Room occupancy: Two lectures can't be allocated in the same room-period. Each extra lecture allocated in the same room-period is a violation.
        for room_courses in timeslot_courses.values():
            # If Room repeats in the list, then there is a violation
            rooms = [room for room, _ in room_courses]
            score += self.weights[0][1] * (len(rooms) - len(set(rooms)))
            if len(rooms) != len(set(rooms)):
                properties["H2"] += 1

            # S1 - Room capacity: The number of students in a room-period can't exceed the capacity of the room. Each student over the capacity is a violation.
            for room, course in room_courses:
                if course.students > room.capacity:
                    score += self.weights[1][0] * (course.students - room.capacity)
                    properties["S1"] += 1

        return (score, properties)
