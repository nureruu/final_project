"""
service.py — Business logic layer.
Covers: Object Interaction, System Logic
"""

from models import Student, Professor, Admin, Course, Department
from repository import StudentRepository, ProfessorRepository, CourseRepository, DepartmentRepository


class UniversityService:
    """
    Central service class that orchestrates interactions between
    Students, Professors, Courses and Departments.
    """

    def __init__(self):
        self.students = StudentRepository()
        self.professors = ProfessorRepository()
        self.courses = CourseRepository()
        self.departments = DepartmentRepository()
        self._id_counters = {"S": 1000, "P": 200, "C": 300, "D": 10, "A": 500}

    # ── ID generation ──────────────────────────────────────────────────────
    def _next_id(self, prefix: str) -> str:
        self._id_counters[prefix] += 1
        return f"{prefix}{self._id_counters[prefix]}"

    # ── Student operations ─────────────────────────────────────────────────
    def add_student(self, first_name: str, last_name: str, email: str,
                    age: int, major: str, year: int) -> Student:
        sid = self._next_id("S")
        student = Student(sid, first_name, last_name, email, age, major, year)
        self.students.add(student)
        return student

    def remove_student(self, student_id: str) -> str:
        student = self.students.remove(student_id)
        # Remove from all enrolled courses
        for course in student.enrolled_courses:
            try:
                course.remove_student(student_id)
            except ValueError:
                pass
        return student.full_name

    def enroll_student_in_course(self, student_id: str, course_id: str) -> None:
        student = self.students.find_by_id(student_id)
        if student is None:
            raise ValueError(f"Student '{student_id}' not found.")
        course = self.courses.find_by_id(course_id)
        if course is None:
            raise ValueError(f"Course '{course_id}' not found.")
        # Bidirectional relationship: Student ↔ Course
        student.enroll(course)
        course.add_student(student)

    def drop_student_from_course(self, student_id: str, course_id: str) -> None:
        student = self.students.find_by_id(student_id)
        if student is None:
            raise ValueError(f"Student '{student_id}' not found.")
        course = self.courses.find_by_id(course_id)
        if course is None:
            raise ValueError(f"Course '{course_id}' not found.")
        student.drop_course(course_id)
        course.remove_student(student_id)

    def assign_grade(self, student_id: str, course_id: str, grade: float) -> None:
        student = self.students.find_by_id(student_id)
        if student is None:
            raise ValueError(f"Student '{student_id}' not found.")
        student.assign_grade(course_id, grade)

    # ── Professor operations ───────────────────────────────────────────────
    def add_professor(self, first_name: str, last_name: str, email: str,
                      age: int, department: str, title: str = "Professor") -> Professor:
        pid = self._next_id("P")
        professor = Professor(pid, first_name, last_name, email, age, department, title)
        self.professors.add(professor)
        return professor

    def remove_professor(self, professor_id: str) -> str:
        prof = self.professors.remove(professor_id)
        return prof.full_name

    def assign_professor_to_course(self, professor_id: str, course_id: str) -> None:
        prof = self.professors.find_by_id(professor_id)
        if prof is None:
            raise ValueError(f"Professor '{professor_id}' not found.")
        course = self.courses.find_by_id(course_id)
        if course is None:
            raise ValueError(f"Course '{course_id}' not found.")
        # Professor ↔ Course relationship
        course.professor = prof
        prof.assign_course(course)

    # ── Course operations ──────────────────────────────────────────────────
    def add_course(self, title: str, credits: int, department: str) -> Course:
        cid = self._next_id("C")
        course = Course(cid, title, credits, department)
        self.courses.add(course)
        # Also register in department if it exists
        dept = next((d for d in self.departments.all() if d.name.lower() == department.lower()), None)
        if dept:
            try:
                dept.add_course(course)
            except ValueError:
                pass
        return course

    def remove_course(self, course_id: str) -> str:
        course = self.courses.remove(course_id)
        return course.title

    # ── Department operations ──────────────────────────────────────────────
    def add_department(self, name: str, faculty: str) -> Department:
        did = self._next_id("D")
        dept = Department(did, name, faculty)
        self.departments.add(dept)
        return dept

    def remove_department(self, dept_id: str) -> str:
        dept = self.departments.remove(dept_id)
        return dept.name

    # ── Statistics / Reports ───────────────────────────────────────────────
    def top_students(self, n: int = 5) -> list:
        return self.students.all_sorted_by_gpa(descending=True)[:n]

    def course_enrollment_report(self) -> list[dict]:
        result = []
        for course in self.courses.all_sorted_by_title():
            result.append({
                "course": course.title,
                "id": course.course_id,
                "professor": course.professor.full_name if course.professor else "TBA",
                "enrolled": len(course.students),
            })
        return result

    def department_summary(self) -> list[dict]:
        result = []
        for dept in self.departments.all_sorted_by_name():
            result.append({
                "dept": dept.name,
                "faculty": dept.faculty,
                "professors": len(dept.professors),
                "courses": len(dept.courses),
            })
        return result

    def student_transcript(self, student_id: str) -> dict:
        student = self.students.find_by_id(student_id)
        if student is None:
            raise ValueError(f"Student '{student_id}' not found.")
        transcript = {
            "student": student.full_name,
            "id": student.person_id,
            "major": student.major,
            "year": student.year,
            "gpa": student.gpa(),
            "courses": []
        }
        for course in student.enrolled_courses:
            grade = student.grades.get(course.course_id)
            transcript["courses"].append({
                "course_id": course.course_id,
                "title": course.title,
                "credits": course.credits,
                "grade": grade if grade is not None else "N/A"
            })
        return transcript

    # ── Polymorphism demo: print_all_persons ───────────────────────────────
    def print_all_persons(self) -> None:
        """
        Polymorphism in action: iterates a mixed collection of Person objects
        and calls get_info() — each subclass responds differently.
        """
        all_persons = (
            self.students.all() +
            self.professors.all()
        )
        print(f"\n{'─'*60}")
        print(f"  ALL PERSONS IN SYSTEM ({len(all_persons)} total)")
        print(f"{'─'*60}")
        for person in sorted(all_persons, key=lambda p: p.last_name):
            print(f"  {person.get_role():12s} | {person.get_info()}")
        print(f"{'─'*60}\n")
