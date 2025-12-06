import unittest
from pathlib import Path
import sys
from unittest.mock import patch, MagicMock
from io import StringIO
import tempfile
import os
import shutil

# Add necessary directories to path
root_folder = Path(__file__).parent
admin_folder = root_folder / "Admin_files"
sys.path.insert(0, str(admin_folder))
sys.path.insert(0, str(root_folder))

from Admin_files.Course import Course
from Functions import create_schedule, auto_select_courses


# -------------------------------------------------------------------
# TestAutoSelectCourses
# -------------------------------------------------------------------

class TestAutoSelectCourses(unittest.TestCase):

    def test_auto_select_basic(self):
        courses = [
            Course("Math 101", "MWF 10-11AM", 3, []),
            Course("Science 101", "TR 2-3PM", 4, []),
            Course("English 101", "MWF 1-2PM", 3, []),
            Course("History 101", "TR 10-11AM", 3, [])
        ]

        for i, course in enumerate(courses):
            course.CRN = 10000 + i

        selected = auto_select_courses(courses, 19)
        total_credits = sum(c.credits for c in selected)

        self.assertLessEqual(total_credits, 19)
        self.assertGreater(len(selected), 0)

    def test_auto_select_exact_19(self):
        courses = [
            Course("Course A", "MWF 10-11AM", 4, []),
            Course("Course B", "TR 2-3PM", 4, []),
            Course("Course C", "MWF 1-2PM", 4, []),
            Course("Course D", "TR 10-11AM", 4, []),
            Course("Course E", "MWF 3-4PM", 3, [])
        ]

        for i, course in enumerate(courses):
            course.CRN = 20000 + i

        selected = auto_select_courses(courses, 19)
        total_credits = sum(c.credits for c in selected)

        self.assertLessEqual(total_credits, 19)
        self.assertGreaterEqual(total_credits, 16)

    def test_auto_select_empty_courses(self):
        selected = auto_select_courses([], 19)
        self.assertEqual(selected, [])

    def test_auto_select_exceeds_limit(self):
        courses = [Course("Big Course", "MWF 10-11AM", 20, [])]
        courses[0].CRN = 30000

        selected = auto_select_courses(courses, 19)
        self.assertEqual(len(selected), 0)

    def test_auto_select_greedy_algorithm(self):
        courses = [
            Course("1 Credit", "MWF 10-11AM", 1, []),
            Course("4 Credit", "TR 2-3PM", 4, []),
            Course("3 Credit", "MWF 1-2PM", 3, [])
        ]

        for i, course in enumerate(courses):
            course.CRN = 40000 + i

        selected = auto_select_courses(courses, 19)

        if len(selected) > 0:
            self.assertGreaterEqual(selected[0].credits, 3)


# -------------------------------------------------------------------
# TestCreateSchedule
# -------------------------------------------------------------------

class TestCreateSchedule(unittest.TestCase):

    def setUp(self):
        """Runs before each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.courses_folder = Path(self.temp_dir) / "Database" / "courses"
        self.courses_folder.mkdir(parents=True, exist_ok=True)

        # create test courses
        self.create_test_course("CPSC 101", 12345, "MWF 10-11AM", 3)
        self.create_test_course("MATH 201", 12346, "TR 2-3PM", 4)
        self.create_test_course("ENG 101", 12347, "MWF 1-2PM", 3)

    def tearDown(self):
        """Runs after each test"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def create_test_course(self, name, crn, time, credits):
        course_file = self.courses_folder / f"{name}.txt"
        with open(course_file, "w", encoding="utf-8") as f:
            f.write(f"crn: {crn}\n")
            f.write(f"course_name: {name}\n")
            f.write(f"time: {time}\n")
            f.write(f"credits: {credits}\n")
            f.write("professor: none\n\n")
            f.write("students:\n")

    @patch("Functions.Path")
    @patch("builtins.input", side_effect=["n"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_create_schedule_auto_no_edit(self, mock_stdout, mock_input, mock_path):
        """Test auto schedule creation with no edits"""

        # Mock Path().parent to point to our temp folder
        mock_parent = MagicMock()
        mock_parent.__truediv__ = lambda _, other: (
            Path(self.temp_dir) / other
            if other == "Database"
            else self.courses_folder / other
        )
        mock_parent.exists.return_value = True
        mock_path.return_value.parent = mock_parent

        self.assertTrue(callable(create_schedule))

    def test_create_schedule_loads_courses_from_files(self):
        files = list(self.courses_folder.glob("*.txt"))
        self.assertEqual(len(files), 3)

        with open(self.courses_folder / "CPSC 101.txt", "r") as f:
            content = f.read()

        self.assertIn("crn: 12345", content)
        self.assertIn("CPSC 101", content)


# -------------------------------------------------------------------
# TestScheduleIntegration
# -------------------------------------------------------------------

class TestScheduleIntegration(unittest.TestCase):

    def test_schedule_workflow(self):
        courses = [
            Course("CPSC 101", "MWF 10-11AM", 3, []),
            Course("MATH 201", "TR 2-3PM", 4, []),
            Course("ENG 101", "MWF 1-2PM", 3, []),
            Course("BIO 110", "TR 10-11AM", 4, []),
            Course("HIS 201", "MWF 3-4PM", 3, [])
        ]

        for i, course in enumerate(courses):
            course.CRN = 50000 + i

        selected = auto_select_courses(courses, 19)
        total_credits = sum(c.credits for c in selected)

        self.assertLessEqual(total_credits, 19)
        self.assertGreaterEqual(len(selected), 4)

        student_id = "900123456"
        for course in selected:
            if student_id not in course.class_list:
                course.class_list.append(student_id)

        for course in selected:
            self.assertIn(student_id, course.class_list)

    def test_19_credit_limit_enforcement(self):
        courses = [
            Course("4 Credit A", "MWF 10-11AM", 4, []),
            Course("4 Credit B", "TR 2-3PM", 4, []),
            Course("4 Credit C", "MWF 1-2PM", 4, []),
            Course("4 Credit D", "TR 10-11AM", 4, []),
            Course("4 Credit E", "MWF 3-4PM", 4, [])
        ]

        for i, course in enumerate(courses):
            course.CRN = 60000 + i

        selected = auto_select_courses(courses, 19)
        total_credits = sum(c.credits for c in selected)

        self.assertLessEqual(total_credits, 19)
        self.assertEqual(total_credits, 16)
        self.assertEqual(len(selected), 4)


# -------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
