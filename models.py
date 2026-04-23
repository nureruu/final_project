"""
models.py — Data models for University Management System
Covers: Abstraction, Inheritance, Polymorphism, Encapsulation
"""

from abc import ABC, abstractmethod
from datetime import date
from typing import Optional


class Person(ABC):
    """Abstract base class for all people in the university."""

    def __init__(self, person_id: str, first_name: str, last_name: str, email: str, age: int):
        # Private fields  (Encapsulation requirement)
        self.__person_id = person_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__age = age

    @property
    def person_id(self) -> str:
        return self.__person_id

    @property
    def first_name(self) -> str:
        return self.__first_name

    @first_name.setter
    def first_name(self, value: str):
        if not value.strip():
            raise ValueError("First name cannot be empty.")
        self.__first_name = value.strip()

    @property
    def last_name(self) -> str:
        return self.__last_name

    @last_name.setter
    def last_name(self, value: str):
        if not value.strip():
            raise ValueError("Last name cannot be empty.")
        self.__last_name = value.strip()

    @property
    def full_name(self) -> str:
        return f"{self.__first_name} {self.__last_name}"

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str):
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email address.")
        self.__email = value.strip()

    @property
    def age(self) -> int:
        return self.__age

    @age.setter
    def age(self, value: int):
        if not (1 <= value <= 120):
            raise ValueError("Age must be between 1 and 120.")
        self.__age = value

    @abstractmethod
    def get_role(self) -> str:
        """Return the role/title of this person."""
        pass

    @abstractmethod
    def get_info(self) -> str:
        """Return a formatted info string."""
        pass

    def __str__(self) -> str:
        return self.get_info()


class Student(Person):
    """Represents a university student."""

    def __init__(self, student_id: str, first_name: str, last_name: str,
                 email: str, age: int, major: str, year: int):
        super().__init__(student_id, first_name, last_name, email, age)
        self.__major = major
        self.__year = year
        self.__enrolled_courses: list = []   
        self.__grades: dict = {}             

    @property
    def major(self) -> str:
        return self.__major

    @major.setter
    def major(self, value: str):
        if not value.strip():
            raise ValueError("Major cannot be empty.")
        self.__major = value.strip()

    @property
    def year(self) -> int:
        return self.__year

    @year.setter
    def year(self, value: int):
        if value not in range(1, 7):
            raise ValueError("Year must be between 1 and 6.")
        self.__year = value

    @property
    def enrolled_courses(self) -> list:
        return list(self.__enrolled_courses)

    @property
    def grades(self) -> dict:
        return dict(self.__grades)

    def enroll(self, course) -> None:
        if any(c.course_id == course.course_id for c in self.__enrolled_courses):
            raise ValueError(f"Already enrolled in '{course.title}'.")
        if len(self.__enrolled_courses) >= 8:
            raise ValueError("Cannot enroll in more than 8 courses.")
        self.__enrolled_courses.append(course)

    def drop_course(self, course_id: str) -> None:
        course = next((c for c in self.__enrolled_courses if c.course_id == course_id), None)
        if course is None:
            raise ValueError("Student is not enrolled in that course.")
        self.__enrolled_courses.remove(course)
        self.__grades.pop(course_id, None)

    def assign_grade(self, course_id: str, grade: float) -> None:
        if not any(c.course_id == course_id for c in self.__enrolled_courses):
            raise ValueError("Student is not enrolled in that course.")
        if not (0.0 <= grade <= 100.0):
            raise ValueError("Grade must be between 0 and 100.")
        self.__grades[course_id] = grade

    def gpa(self) -> float:
        if not self.__grades:
            return 0.0
        return round(sum(self.__grades.values()) / len(self.__grades), 2)

    def get_role(self) -> str:
        return "Student"

    def get_info(self) -> str:
        return (f"[Student] ID={self.person_id} | {self.full_name} | "
                f"Major: {self.__major} | Year {self.__year} | "
                f"GPA: {self.gpa()} | Courses: {len(self.__enrolled_courses)}")


class Professor(Person):
    """Represents a university professor."""

    def __init__(self, professor_id: str, first_name: str, last_name: str,
                 email: str, age: int, department: str, title: str = "Professor"):
        super().__init__(professor_id, first_name, last_name, email, age)
        self.__department = department
        self.__title = title
        self.__courses_taught: list = []

    @property
    def department(self) -> str:
        return self.__department

    @department.setter
    def department(self, value: str):
        if not value.strip():
            raise ValueError("Department cannot be empty.")
        self.__department = value.strip()

    @property
    def title(self) -> str:
        return self.__title

    @property
    def courses_taught(self) -> list:
        return list(self.__courses_taught)

    def assign_course(self, course) -> None:
        if any(c.course_id == course.course_id for c in self.__courses_taught):
            raise ValueError("Already assigned to this course.")
        self.__courses_taught.append(course)

    def remove_course(self, course_id: str) -> None:
        course = next((c for c in self.__courses_taught if c.course_id == course_id), None)
        if course is None:
            raise ValueError("Course not found in professor's list.")
        self.__courses_taught.remove(course)

    def get_role(self) -> str:
        return f"{self.__title}"

    def get_info(self) -> str:
        return (f"[Professor] ID={self.person_id} | {self.full_name} | "
                f"{self.__title}, Dept: {self.__department} | "
                f"Courses: {len(self.__courses_taught)}")


class Admin(Person):
    """Represents an administrative staff member."""

    def __init__(self, admin_id: str, first_name: str, last_name: str,
                 email: str, age: int, office: str):
        super().__init__(admin_id, first_name, last_name, email, age)
        self.__office = office

    @property
    def office(self) -> str:
        return self.__office

    def get_role(self) -> str:
        return "Admin"

    def get_info(self) -> str:
        return (f"[Admin] ID={self.person_id} | {self.full_name} | "
                f"Office: {self.__office}")


class Course:
    """Represents a university course."""

    def __init__(self, course_id: str, title: str, credits: int, department: str):
        self.__course_id = course_id
        self.__title = title
        self.__credits = credits
        self.__department = department
        self.__professor: Optional[Professor] = None
        self.__students: list = []

    @property
    def course_id(self) -> str:
        return self.__course_id

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value: str):
        if not value.strip():
            raise ValueError("Title cannot be empty.")
        self.__title = value.strip()

    @property
    def credits(self) -> int:
        return self.__credits

    @credits.setter
    def credits(self, value: int):
        if not (1 <= value <= 10):
            raise ValueError("Credits must be between 1 and 10.")
        self.__credits = value

    @property
    def department(self) -> str:
        return self.__department

    @property
    def professor(self) -> Optional[Professor]:
        return self.__professor

    @professor.setter
    def professor(self, prof: Professor):
        self.__professor = prof

    @property
    def students(self) -> list:
        return list(self.__students)

    def add_student(self, student: Student) -> None:
        if any(s.person_id == student.person_id for s in self.__students):
            raise ValueError("Student already in course.")
        self.__students.append(student)

    def remove_student(self, student_id: str) -> None:
        student = next((s for s in self.__students if s.person_id == student_id), None)
        if student is None:
            raise ValueError("Student not found in course.")
        self.__students.remove(student)

    def get_info(self) -> str:
        prof_name = self.__professor.full_name if self.__professor else "TBA"
        return (f"[Course] {self.__course_id} | {self.__title} | "
                f"{self.__credits} credits | Dept: {self.__department} | "
                f"Prof: {prof_name} | Students: {len(self.__students)}")

    def __str__(self) -> str:
        return self.get_info()


class Department:
    """Represents a university department."""

    def __init__(self, dept_id: str, name: str, faculty: str):
        self.__dept_id = dept_id
        self.__name = name
        self.__faculty = faculty
        self.__professors: list = []
        self.__courses: list = []

    @property
    def dept_id(self) -> str:
        return self.__dept_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def faculty(self) -> str:
        return self.__faculty

    @property
    def professors(self) -> list:
        return list(self.__professors)

    @property
    def courses(self) -> list:
        return list(self.__courses)

    def add_professor(self, prof: Professor) -> None:
        if any(p.person_id == prof.person_id for p in self.__professors):
            raise ValueError("Professor already in department.")
        self.__professors.append(prof)

    def add_course(self, course: Course) -> None:
        if any(c.course_id == course.course_id for c in self.__courses):
            raise ValueError("Course already in department.")
        self.__courses.append(course)

    def get_info(self) -> str:
        return (f"[Dept] {self.__dept_id} | {self.__name} | "
                f"Faculty: {self.__faculty} | "
                f"Professors: {len(self.__professors)} | Courses: {len(self.__courses)}")

    def __str__(self) -> str:
        return self.get_info()
