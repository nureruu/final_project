"""
ui.py — Console-based menu interface.
Covers: User Interface, Error Handling, Input Validation
"""

from service import UniversityService


# ── Helper utilities ───────────────────────────────────────────────────────────

def clear_line():
    print()

def header(title: str):
    width = 60
    print("\n" + "═" * width)
    print(f"  {title}")
    print("═" * width)

def subheader(title: str):
    print(f"\n  ── {title} {'─' * (54 - len(title))}")

def info(msg: str):
    print(f"  ✓  {msg}")

def error(msg: str):
    print(f"  ✗  ERROR: {msg}")

def warn(msg: str):
    print(f"  ⚠  {msg}")

def prompt(label: str) -> str:
    return input(f"  → {label}: ").strip()

def prompt_int(label: str, min_val: int = None, max_val: int = None) -> int:
    while True:
        raw = prompt(label)
        try:
            val = int(raw)
            if min_val is not None and val < min_val:
                error(f"Value must be ≥ {min_val}")
                continue
            if max_val is not None and val > max_val:
                error(f"Value must be ≤ {max_val}")
                continue
            return val
        except ValueError:
            error("Please enter a valid integer.")

def prompt_float(label: str, min_val: float = 0.0, max_val: float = 100.0) -> float:
    while True:
        raw = prompt(label)
        try:
            val = float(raw)
            if val < min_val or val > max_val:
                error(f"Value must be between {min_val} and {max_val}")
                continue
            return val
        except ValueError:
            error("Please enter a valid number.")

def pause():
    input("\n  Press Enter to continue...")


# ── Main UI class ──────────────────────────────────────────────────────────────

class ConsoleUI:

    def __init__(self):
        self.service = UniversityService()
        self._seed_demo_data()

    # ── Demo data ──────────────────────────────────────────────────────────
    def _seed_demo_data(self):
        """Load sample data so the system isn't empty on first run."""
        # Departments
        cs   = self.service.add_department("Computer Science", "Engineering")
        math = self.service.add_department("Mathematics", "Sciences")
        bus  = self.service.add_department("Business", "Economics")

        # Professors
        p1 = self.service.add_professor("Alice", "Ivanova",  "a.ivanova@uni.kg",  45, "Computer Science", "Professor")
        p2 = self.service.add_professor("Boris", "Petrov",   "b.petrov@uni.kg",   52, "Mathematics",      "Associate Professor")
        p3 = self.service.add_professor("Clara", "Smirnova", "c.smirnova@uni.kg", 38, "Business",         "Lecturer")

        cs.add_professor(p1)
        math.add_professor(p2)
        bus.add_professor(p3)

        # Courses
        c1 = self.service.add_course("Introduction to Programming", 4, "Computer Science")
        c2 = self.service.add_course("Data Structures & Algorithms", 5, "Computer Science")
        c3 = self.service.add_course("Calculus I", 4, "Mathematics")
        c4 = self.service.add_course("Business English", 3, "Business")

        self.service.assign_professor_to_course(p1.person_id, c1.course_id)
        self.service.assign_professor_to_course(p1.person_id, c2.course_id)
        self.service.assign_professor_to_course(p2.person_id, c3.course_id)
        self.service.assign_professor_to_course(p3.person_id, c4.course_id)

        # Students
        s1 = self.service.add_student("Aibek",   "Dzhaksybekov", "aibek@student.kg",   20, "Computer Science", 2)
        s2 = self.service.add_student("Ainura",  "Bekova",        "ainura@student.kg",  19, "Computer Science", 1)
        s3 = self.service.add_student("Daniyar", "Sultanov",      "daniyar@student.kg", 22, "Mathematics",      3)
        s4 = self.service.add_student("Gulnara", "Asanova",       "gulnara@student.kg", 21, "Business",         2)

        for s, c in [(s1, c1), (s1, c2), (s2, c1), (s3, c3), (s4, c4)]:
            self.service.enroll_student_in_course(s.person_id, c.course_id)

        self.service.assign_grade(s1.person_id, c1.course_id, 88.0)
        self.service.assign_grade(s1.person_id, c2.course_id, 92.5)
        self.service.assign_grade(s2.person_id, c1.course_id, 75.0)
        self.service.assign_grade(s3.person_id, c3.course_id, 95.0)
        self.service.assign_grade(s4.person_id, c4.course_id, 80.0)

    # ── Main loop ──────────────────────────────────────────────────────────
    def run(self):
        while True:
            header("UNIVERSITY MANAGEMENT SYSTEM")
            print("  1. Students")
            print("  2. Professors")
            print("  3. Courses")
            print("  4. Departments")
            print("  5. Reports & Statistics")
            print("  0. Exit")
            clear_line()
            choice = prompt("Select option")

            if   choice == "1": self._menu_students()
            elif choice == "2": self._menu_professors()
            elif choice == "3": self._menu_courses()
            elif choice == "4": self._menu_departments()
            elif choice == "5": self._menu_reports()
            elif choice == "0":
                print("\n  Goodbye!\n")
                break
            else:
                warn("Invalid option. Please try again.")

    # ── Students menu ──────────────────────────────────────────────────────
    def _menu_students(self):
        while True:
            header("STUDENTS")
            print("  1. List all students")
            print("  2. Add student")
            print("  3. Remove student")
            print("  4. Search students")
            print("  5. View student details / transcript")
            print("  6. Enroll student in course")
            print("  7. Drop student from course")
            print("  8. Assign grade")
            print("  0. Back")
            clear_line()
            choice = prompt("Select option")

            if   choice == "1": self._list_students()
            elif choice == "2": self._add_student()
            elif choice == "3": self._remove_student()
            elif choice == "4": self._search_students()
            elif choice == "5": self._student_transcript()
            elif choice == "6": self._enroll_student()
            elif choice == "7": self._drop_student()
            elif choice == "8": self._assign_grade()
            elif choice == "0": break
            else: warn("Invalid option.")

    def _list_students(self):
        subheader("ALL STUDENTS")
        students = self.service.students.all_sorted_by_name()
        if not students:
            warn("No students registered.")
        else:
            for s in students:
                print(f"  {s.get_info()}")
        pause()

    def _add_student(self):
        subheader("ADD STUDENT")
        try:
            first   = prompt("First name")
            last    = prompt("Last name")
            email   = prompt("Email")
            age     = prompt_int("Age", 16, 80)
            major   = prompt("Major")
            year    = prompt_int("Year (1-6)", 1, 6)
            student = self.service.add_student(first, last, email, age, major, year)
            info(f"Student added: {student.get_info()}")
        except ValueError as e:
            error(str(e))
        pause()

    def _remove_student(self):
        subheader("REMOVE STUDENT")
        student_id = prompt("Student ID")
        try:
            name = self.service.remove_student(student_id)
            info(f"Student '{name}' removed.")
        except ValueError as e:
            error(str(e))
        pause()

    def _search_students(self):
        subheader("SEARCH STUDENTS")
        print("  1. By name   2. By major   3. By year")
        choice = prompt("Filter type")
        results = []
        try:
            if choice == "1":
                name = prompt("Name (partial)")
                results = self.service.students.find_by_name(name)
            elif choice == "2":
                major = prompt("Major (partial)")
                results = self.service.students.find_by_major(major)
            elif choice == "3":
                year = prompt_int("Year", 1, 6)
                results = self.service.students.find_by_year(year)
            else:
                warn("Invalid choice.")
                pause()
                return
            if not results:
                warn("No students found.")
            else:
                for s in results:
                    print(f"  {s.get_info()}")
        except ValueError as e:
            error(str(e))
        pause()

    def _student_transcript(self):
        subheader("STUDENT TRANSCRIPT")
        student_id = prompt("Student ID")
        try:
            t = self.service.student_transcript(student_id)
            print(f"\n  Student : {t['student']}  (ID: {t['id']})")
            print(f"  Major   : {t['major']}  |  Year: {t['year']}")
            print(f"  GPA     : {t['gpa']}")
            print(f"  {'─'*52}")
            print(f"  {'Course ID':<10} {'Title':<35} {'Cr':>3}  {'Grade':>6}")
            print(f"  {'─'*52}")
            for c in t["courses"]:
                grade_str = f"{c['grade']:.1f}" if isinstance(c['grade'], float) else c['grade']
                print(f"  {c['course_id']:<10} {c['title']:<35} {c['credits']:>3}  {grade_str:>6}")
            print(f"  {'─'*52}")
        except ValueError as e:
            error(str(e))
        pause()

    def _enroll_student(self):
        subheader("ENROLL STUDENT IN COURSE")
        student_id = prompt("Student ID")
        course_id  = prompt("Course ID")
        try:
            self.service.enroll_student_in_course(student_id, course_id)
            info("Enrollment successful.")
        except ValueError as e:
            error(str(e))
        pause()

    def _drop_student(self):
        subheader("DROP STUDENT FROM COURSE")
        student_id = prompt("Student ID")
        course_id  = prompt("Course ID")
        try:
            self.service.drop_student_from_course(student_id, course_id)
            info("Student dropped from course.")
        except ValueError as e:
            error(str(e))
        pause()

    def _assign_grade(self):
        subheader("ASSIGN GRADE")
        student_id = prompt("Student ID")
        course_id  = prompt("Course ID")
        grade      = prompt_float("Grade (0–100)", 0.0, 100.0)
        try:
            self.service.assign_grade(student_id, course_id, grade)
            info("Grade assigned.")
        except ValueError as e:
            error(str(e))
        pause()

    # ── Professors menu ────────────────────────────────────────────────────
    def _menu_professors(self):
        while True:
            header("PROFESSORS")
            print("  1. List all professors")
            print("  2. Add professor")
            print("  3. Remove professor")
            print("  4. Search professors")
            print("  5. Assign professor to course")
            print("  0. Back")
            clear_line()
            choice = prompt("Select option")

            if   choice == "1": self._list_professors()
            elif choice == "2": self._add_professor()
            elif choice == "3": self._remove_professor()
            elif choice == "4": self._search_professors()
            elif choice == "5": self._assign_professor_course()
            elif choice == "0": break
            else: warn("Invalid option.")

    def _list_professors(self):
        subheader("ALL PROFESSORS")
        profs = self.service.professors.all_sorted_by_name()
        if not profs:
            warn("No professors registered.")
        else:
            for p in profs:
                print(f"  {p.get_info()}")
        pause()

    def _add_professor(self):
        subheader("ADD PROFESSOR")
        try:
            first  = prompt("First name")
            last   = prompt("Last name")
            email  = prompt("Email")
            age    = prompt_int("Age", 22, 80)
            dept   = prompt("Department")
            title  = prompt("Title (Professor / Associate Professor / Lecturer)")
            prof   = self.service.add_professor(first, last, email, age, dept, title)
            info(f"Professor added: {prof.get_info()}")
        except ValueError as e:
            error(str(e))
        pause()

    def _remove_professor(self):
        subheader("REMOVE PROFESSOR")
        prof_id = prompt("Professor ID")
        try:
            name = self.service.remove_professor(prof_id)
            info(f"Professor '{name}' removed.")
        except ValueError as e:
            error(str(e))
        pause()

    def _search_professors(self):
        subheader("SEARCH PROFESSORS")
        print("  1. By name   2. By department")
        choice = prompt("Filter type")
        results = []
        if choice == "1":
            name = prompt("Name (partial)")
            results = self.service.professors.find_by_name(name)
        elif choice == "2":
            dept = prompt("Department (partial)")
            results = self.service.professors.find_by_department(dept)
        else:
            warn("Invalid choice.")
            pause()
            return
        if not results:
            warn("No professors found.")
        else:
            for p in results:
                print(f"  {p.get_info()}")
        pause()

    def _assign_professor_course(self):
        subheader("ASSIGN PROFESSOR TO COURSE")
        prof_id   = prompt("Professor ID")
        course_id = prompt("Course ID")
        try:
            self.service.assign_professor_to_course(prof_id, course_id)
            info("Assignment successful.")
        except ValueError as e:
            error(str(e))
        pause()

    # ── Courses menu ───────────────────────────────────────────────────────
    def _menu_courses(self):
        while True:
            header("COURSES")
            print("  1. List all courses")
            print("  2. Add course")
            print("  3. Remove course")
            print("  4. Search courses")
            print("  5. Course details (enrolled students)")
            print("  0. Back")
            clear_line()
            choice = prompt("Select option")

            if   choice == "1": self._list_courses()
            elif choice == "2": self._add_course()
            elif choice == "3": self._remove_course()
            elif choice == "4": self._search_courses()
            elif choice == "5": self._course_details()
            elif choice == "0": break
            else: warn("Invalid option.")

    def _list_courses(self):
        subheader("ALL COURSES")
        courses = self.service.courses.all_sorted_by_title()
        if not courses:
            warn("No courses available.")
        else:
            for c in courses:
                print(f"  {c.get_info()}")
        pause()

    def _add_course(self):
        subheader("ADD COURSE")
        try:
            title   = prompt("Course title")
            credits = prompt_int("Credits (1–10)", 1, 10)
            dept    = prompt("Department")
            course  = self.service.add_course(title, credits, dept)
            info(f"Course added: {course.get_info()}")
        except ValueError as e:
            error(str(e))
        pause()

    def _remove_course(self):
        subheader("REMOVE COURSE")
        course_id = prompt("Course ID")
        try:
            title = self.service.remove_course(course_id)
            info(f"Course '{title}' removed.")
        except ValueError as e:
            error(str(e))
        pause()

    def _search_courses(self):
        subheader("SEARCH COURSES")
        print("  1. By title   2. By department")
        choice = prompt("Filter type")
        results = []
        if choice == "1":
            title = prompt("Title (partial)")
            results = self.service.courses.find_by_title(title)
        elif choice == "2":
            dept = prompt("Department (partial)")
            results = self.service.courses.find_by_department(dept)
        else:
            warn("Invalid choice.")
            pause()
            return
        if not results:
            warn("No courses found.")
        else:
            for c in results:
                print(f"  {c.get_info()}")
        pause()

    def _course_details(self):
        subheader("COURSE DETAILS")
        course_id = prompt("Course ID")
        course = self.service.courses.find_by_id(course_id)
        if course is None:
            error("Course not found.")
            pause()
            return
        print(f"\n  {course.get_info()}")
        print(f"  {'─'*52}")
        print(f"  Enrolled students ({len(course.students)}):")
        if not course.students:
            print("  (none)")
        for s in course.students:
            grade = s.grades.get(course_id)
            grade_str = f"{grade:.1f}" if grade is not None else "N/A"
            print(f"    • {s.full_name} (ID: {s.person_id})  Grade: {grade_str}")
        pause()

    # ── Departments menu ───────────────────────────────────────────────────
    def _menu_departments(self):
        while True:
            header("DEPARTMENTS")
            print("  1. List all departments")
            print("  2. Add department")
            print("  3. Remove department")
            print("  4. Search departments")
            print("  0. Back")
            clear_line()
            choice = prompt("Select option")

            if   choice == "1": self._list_departments()
            elif choice == "2": self._add_department()
            elif choice == "3": self._remove_department()
            elif choice == "4": self._search_departments()
            elif choice == "0": break
            else: warn("Invalid option.")

    def _list_departments(self):
        subheader("ALL DEPARTMENTS")
        depts = self.service.departments.all_sorted_by_name()
        if not depts:
            warn("No departments.")
        else:
            for d in depts:
                print(f"  {d.get_info()}")
        pause()

    def _add_department(self):
        subheader("ADD DEPARTMENT")
        try:
            name    = prompt("Department name")
            faculty = prompt("Faculty")
            dept    = self.service.add_department(name, faculty)
            info(f"Department added: {dept.get_info()}")
        except ValueError as e:
            error(str(e))
        pause()

    def _remove_department(self):
        subheader("REMOVE DEPARTMENT")
        dept_id = prompt("Department ID")
        try:
            name = self.service.remove_department(dept_id)
            info(f"Department '{name}' removed.")
        except ValueError as e:
            error(str(e))
        pause()

    def _search_departments(self):
        subheader("SEARCH DEPARTMENTS")
        name = prompt("Name (partial)")
        results = self.service.departments.find_by_name(name)
        if not results:
            warn("No departments found.")
        else:
            for d in results:
                print(f"  {d.get_info()}")
        pause()

    # ── Reports menu ───────────────────────────────────────────────────────
    def _menu_reports(self):
        while True:
            header("REPORTS & STATISTICS")
            print("  1. Top students by GPA")
            print("  2. Course enrollment report")
            print("  3. Department summary")
            print("  4. All persons in system (Polymorphism demo)")
            print("  5. Students sorted by GPA (ascending)")
            print("  0. Back")
            clear_line()
            choice = prompt("Select option")

            if   choice == "1": self._top_students()
            elif choice == "2": self._enrollment_report()
            elif choice == "3": self._dept_summary()
            elif choice == "4": self.service.print_all_persons(); pause()
            elif choice == "5": self._students_by_gpa_asc()
            elif choice == "0": break
            else: warn("Invalid option.")

    def _top_students(self):
        subheader("TOP STUDENTS BY GPA")
        n = prompt_int("How many to show", 1, 50)
        top = self.service.top_students(n)
        if not top:
            warn("No students yet.")
        else:
            for i, s in enumerate(top, 1):
                print(f"  {i:>3}. GPA {s.gpa():>6.2f}  |  {s.full_name}  ({s.major}, Year {s.year})")
        pause()

    def _enrollment_report(self):
        subheader("COURSE ENROLLMENT REPORT")
        report = self.service.course_enrollment_report()
        print(f"  {'ID':<8} {'Title':<35} {'Professor':<22} {'Students':>8}")
        print(f"  {'─'*73}")
        for row in report:
            print(f"  {row['id']:<8} {row['course']:<35} {row['professor']:<22} {row['enrolled']:>8}")
        pause()

    def _dept_summary(self):
        subheader("DEPARTMENT SUMMARY")
        summary = self.service.department_summary()
        print(f"  {'Department':<25} {'Faculty':<20} {'Profs':>6} {'Courses':>8}")
        print(f"  {'─'*59}")
        for row in summary:
            print(f"  {row['dept']:<25} {row['faculty']:<20} {row['professors']:>6} {row['courses']:>8}")
        pause()

    def _students_by_gpa_asc(self):
        subheader("STUDENTS SORTED BY GPA (LOW → HIGH)")
        students = self.service.students.all_sorted_by_gpa(descending=False)
        for s in students:
            print(f"  GPA {s.gpa():>6.2f}  |  {s.full_name}  ({s.major})")
        pause()
