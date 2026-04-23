"""
repository.py — In-memory storage with collections & operations.
Covers: Collections requirement (add / remove / iterate / search / sort / filter)
"""

from typing import Optional
from models import Student, Professor, Admin, Course, Department


class StudentRepository:
    """Manages a collection of Student objects."""

    def __init__(self):
        self.__students: list[Student] = []   # Collection (List)

    # ── Add / Remove ───────────────────────────────────────────────────────
    def add(self, student: Student) -> None:
        if self.find_by_id(student.person_id):
            raise ValueError(f"Student with ID '{student.person_id}' already exists.")
        self.__students.append(student)

    def remove(self, student_id: str) -> Student:
        student = self.find_by_id(student_id)
        if student is None:
            raise ValueError(f"Student '{student_id}' not found.")
        self.__students.remove(student)
        return student

    # ── Search / Filter ────────────────────────────────────────────────────
    def find_by_id(self, student_id: str) -> Optional[Student]:
        return next((s for s in self.__students if s.person_id == student_id), None)

    def find_by_name(self, name: str) -> list[Student]:
        name_lower = name.lower()
        return [s for s in self.__students if name_lower in s.full_name.lower()]

    def find_by_major(self, major: str) -> list[Student]:
        return [s for s in self.__students if major.lower() in s.major.lower()]

    def find_by_year(self, year: int) -> list[Student]:
        return [s for s in self.__students if s.year == year]

    # ── Sort ───────────────────────────────────────────────────────────────
    def all_sorted_by_name(self) -> list[Student]:
        return sorted(self.__students, key=lambda s: s.last_name)

    def all_sorted_by_gpa(self, descending: bool = True) -> list[Student]:
        return sorted(self.__students, key=lambda s: s.gpa(), reverse=descending)

    # ── Iterate ────────────────────────────────────────────────────────────
    def all(self) -> list[Student]:
        return list(self.__students)

    def count(self) -> int:
        return len(self.__students)


class ProfessorRepository:
    """Manages a collection of Professor objects."""

    def __init__(self):
        self.__professors: list[Professor] = []

    def add(self, professor: Professor) -> None:
        if self.find_by_id(professor.person_id):
            raise ValueError(f"Professor '{professor.person_id}' already exists.")
        self.__professors.append(professor)

    def remove(self, professor_id: str) -> Professor:
        prof = self.find_by_id(professor_id)
        if prof is None:
            raise ValueError(f"Professor '{professor_id}' not found.")
        self.__professors.remove(prof)
        return prof

    def find_by_id(self, professor_id: str) -> Optional[Professor]:
        return next((p for p in self.__professors if p.person_id == professor_id), None)

    def find_by_name(self, name: str) -> list[Professor]:
        return [p for p in self.__professors if name.lower() in p.full_name.lower()]

    def find_by_department(self, department: str) -> list[Professor]:
        return [p for p in self.__professors if department.lower() in p.department.lower()]

    def all_sorted_by_name(self) -> list[Professor]:
        return sorted(self.__professors, key=lambda p: p.last_name)

    def all(self) -> list[Professor]:
        return list(self.__professors)

    def count(self) -> int:
        return len(self.__professors)


class CourseRepository:
    """Manages a collection of Course objects."""

    def __init__(self):
        self.__courses: list[Course] = []

    def add(self, course: Course) -> None:
        if self.find_by_id(course.course_id):
            raise ValueError(f"Course '{course.course_id}' already exists.")
        self.__courses.append(course)

    def remove(self, course_id: str) -> Course:
        course = self.find_by_id(course_id)
        if course is None:
            raise ValueError(f"Course '{course_id}' not found.")
        self.__courses.remove(course)
        return course

    def find_by_id(self, course_id: str) -> Optional[Course]:
        return next((c for c in self.__courses if c.course_id == course_id), None)

    def find_by_title(self, title: str) -> list[Course]:
        return [c for c in self.__courses if title.lower() in c.title.lower()]

    def find_by_department(self, department: str) -> list[Course]:
        return [c for c in self.__courses if department.lower() in c.department.lower()]

    def all_sorted_by_title(self) -> list[Course]:
        return sorted(self.__courses, key=lambda c: c.title)

    def all_sorted_by_credits(self, descending: bool = False) -> list[Course]:
        return sorted(self.__courses, key=lambda c: c.credits, reverse=descending)

    def all(self) -> list[Course]:
        return list(self.__courses)

    def count(self) -> int:
        return len(self.__courses)


class DepartmentRepository:
    """Manages a collection of Department objects."""

    def __init__(self):
        self.__departments: list[Department] = []

    def add(self, department: Department) -> None:
        if self.find_by_id(department.dept_id):
            raise ValueError(f"Department '{department.dept_id}' already exists.")
        self.__departments.append(department)

    def remove(self, dept_id: str) -> Department:
        dept = self.find_by_id(dept_id)
        if dept is None:
            raise ValueError(f"Department '{dept_id}' not found.")
        self.__departments.remove(dept)
        return dept

    def find_by_id(self, dept_id: str) -> Optional[Department]:
        return next((d for d in self.__departments if d.dept_id == dept_id), None)

    def find_by_name(self, name: str) -> list[Department]:
        return [d for d in self.__departments if name.lower() in d.name.lower()]

    def all_sorted_by_name(self) -> list[Department]:
        return sorted(self.__departments, key=lambda d: d.name)

    def all(self) -> list[Department]:
        return list(self.__departments)

    def count(self) -> int:
        return len(self.__departments)
