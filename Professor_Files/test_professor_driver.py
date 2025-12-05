import unittest
from pathlib import Path
import sys
from unittest.mock import patch
from io import StringIO

# Add necessary directories to path
root_folder = Path(__file__).parent
professor_files_folder = root_folder / "Professor_Files"
admin_folder = root_folder / "Admin_files"
sys.path.insert(0, str(professor_files_folder))
sys.path.insert(0, str(admin_folder))
sys.path.insert(0, str(root_folder))

from Professor import Professor
from Admin_files.Course import Course
from professor_driver import professor_driver


class TestProfessorDriver(unittest.TestCase):
    """Test suite for professor_driver function"""

    def setUp(self):
        """Setup fixtures before each test"""
        self.professor = Professor("700123456", "Dr. Test Professor",
                                  "Computer Science", ["12345", "67890"])

        # Create test courses
        self.course1 = Course("CPSC 101", "MWF 10-11AM", 3,
                              ["900111111", "900222222"])
        self.course1.CRN = 12345
        Course.courses_by_crn["12345"] = self.course1

        self.course2 = Course("CPSC 201", "TR 2-3:30PM", 3, ["900333333"])
        self.course2.CRN = 67890
        Course.courses_by_crn["67890"] = self.course2

    def tearDown(self):
        """Cleanup after each test"""
        Course.courses_by_crn.clear()
        Course.crns_list.clear()

    @patch('builtins.input', side_effect=['5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_exit_menu(self, mock_stdout, mock_input):
        professor_driver(self.professor)
        output = mock_stdout.getvalue()
        self.assertIn("PROFESSOR MENU", output)

    @patch('builtins.input', side_effect=['1', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_view_assigned_courses(self, mock_stdout, mock_input):
        professor_driver(self.professor)
        output = mock_stdout.getvalue()
        self.assertIn("Dr. Test Professor's Assigned Courses", output)
        self.assertIn("CPSC 101", output)
        self.assertIn("CPSC 201", output)
        self.assertIn("12345", output)
        self.assertIn("67890", output)

    @patch('builtins.input', side_effect=['1', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_view_assigned_courses_empty(self, mock_stdout, mock_input):
        empty_prof = Professor("700999999", "Dr. Empty", "Mathematics")
        professor_driver(empty_prof)
        output = mock_stdout.getvalue()
        self.assertIn("No courses assigned", output)

    @patch('builtins.input', side_effect=['2', '12345', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_see_enrolled_students(self, mock_stdout, mock_input):
        professor_driver(self.professor)
        output = mock_stdout.getvalue()
        self.assertIn("CPSC 101", output)
        self.assertIn("900111111", output)
        self.assertIn("900222222", output)
        self.assertIn("Enrolled Students (2)", output)

    @patch('builtins.input', side_effect=['2', '99999', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_see_students_not_assigned_course(self, mock_stdout, mock_input):
        professor_driver(self.professor)
        output = mock_stdout.getvalue()
        self.assertIn("not assigned to you", output)

    @patch('builtins.input', side_effect=['2', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_see_students_no_courses(self, mock_stdout, mock_input):
        empty_prof = Professor("700999999", "Dr. Empty", "Mathematics")
        professor_driver(empty_prof)
        output = mock_stdout.getvalue()
        self.assertIn("You have no assigned courses", output)

    @patch('builtins.input', side_effect=['3', '12345', 'MWF 1-2PM', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_change_course_time(self, mock_stdout, mock_input):
        professor_driver(self.professor)
        output = mock_stdout.getvalue()
        self.assertIn("Current Time: MWF 10-11AM", output)
        self.assertIn("Course time updated to: MWF 1-2PM", output)
        self.assertEqual(self.course1.time, "MWF 1-2PM")

    @patch('builtins.input', side_effect=['3', '99999', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_change_time_not_assigned_course(self, mock_stdout, mock_input):
        professor_driver(self.professor)
        output = mock_stdout.getvalue()
        self.assertIn("not assigned to you", output)

    @patch('builtins.input', side_effect=['3', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_change_time_no_courses(self, mock_stdout, mock_input):
        empty_prof = Professor("700999999", "Dr. Empty", "Mathematics")
        professor_driver(empty_prof)
        output = mock_stdout.getvalue()
        self.assertIn("You have no assigned courses", output)

    @patch('builtins.input', side_effect=['4', '12345', '900111111', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_drop_student_from_course(self, mock_stdout, mock_input):
        initial_count = len(self.course1.class_list)
        professor_driver(self.professor)
        output = mock_stdout.getvalue()
        self.assertIn("Student 900111111 dropped from CPSC 101", output)
        self.assertEqual(len(self.course1.class_list), initial_count - 1)
        self.assertNotIn("900111111", self.course1.class_list)

    @patch('builtins.input', side_effect=['4', '12345', '900999999', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_drop_student_not_in_course(self, mock_stdout, mock_input):
        professor_driver(self.professor)
        output = mock_stdout.getvalue()
        self.assertIn("Student 900999999 not found in this course", output)

    @patch('builtins.input', side_effect=['4', '99999', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_drop_student_not_assigned_course(self, mock_stdout, mock_input):
        professor_driver(self.professor)
        output = mock_stdout.getvalue()
        self.assertIn("not assigned to you", output)

    @patch('builtins.input', side_effect=['4', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_drop_student_no_courses(self, mock_stdout, mock_input):
        empty_prof = Professor("700999999", "Dr. Empty", "Mathematics")
        professor_driver(empty_prof)
        output = mock_stdout.getvalue()
        self.assertIn("You have no assigned courses", output)

    @patch('builtins.input', side_effect=['99', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_menu_choice(self, mock_stdout, mock_input):
        professor_driver(self.professor)
        output = mock_stdout.getvalue()
        self.assertIn("Invalid choice", output)


if __name__ == "__main__":
    unittest.main()
