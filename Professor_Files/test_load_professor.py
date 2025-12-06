import unittest
from pathlib import Path
import sys
import os
import tempfile

# Add Professor Files directory to path
root_folder = Path(__file__).parent
professor_files_folder = root_folder / "Professor_Files"
sys.path.insert(0, str(professor_files_folder))

from Professor_Files import Professor
from Professor_Files.load_professor import load_professor


class TestLoadProfessor(unittest.TestCase):
    """Test suite for load_professor function"""

    def test_load_professor_success(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            temp_file = f.name
            f.write("STUDENT,900123456,John Doe,Freshman,Computer Science,true\n")
            f.write("PROFESSOR,700123456,Dr. Jane Smith,Mathematics,12345;67890\n")
            f.write("ADMIN,800123456,Admin User\n")

        try:
            prof = load_professor("700123456", temp_file)

            self.assertIsNotNone(prof)
            self.assertEqual(prof.professor_id, "700123456")
            self.assertEqual(prof.full_name, "Dr. Jane Smith")
            self.assertEqual(prof.department, "Mathematics")
            self.assertEqual(prof.assigned_courses, ["12345", "67890"])
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_load_professor_no_courses(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            temp_file = f.name
            f.write("PROFESSOR,700999999,Dr. New Professor,Physics,\n")

        try:
            prof = load_professor("700999999", temp_file)

            self.assertIsNotNone(prof)
            self.assertEqual(prof.professor_id, "700999999")
            self.assertEqual(prof.full_name, "Dr. New Professor")
            self.assertEqual(prof.department, "Physics")
            self.assertEqual(prof.assigned_courses, [])
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_load_professor_not_found(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            temp_file = f.name
            f.write("STUDENT,900123456,John Doe,Freshman,Computer Science,true\n")
            f.write("ADMIN,800123456,Admin User\n")

        try:
            prof = load_professor("700999999", temp_file)
            self.assertIsNone(prof)
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_load_professor_wrong_user_type(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            temp_file = f.name
            f.write("STUDENT,900123456,John Doe,Freshman,Computer Science,true\n")

        try:
            prof = load_professor("900123456", temp_file)
            self.assertIsNone(prof)
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_load_professor_with_special_characters(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            temp_file = f.name
            f.write("PROFESSOR,700123456,Dr. O'Brien PhD,Computer Science,11111\n")

        try:
            prof = load_professor("700123456", temp_file)

            self.assertIsNotNone(prof)
            self.assertEqual(prof.professor_id, "700123456")
            self.assertIn("O'Brien", prof.full_name)
            self.assertEqual(prof.department, "Computer Science")
            self.assertEqual(prof.assigned_courses, ["11111"])
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_load_professor_empty_file(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            temp_file = f.name

        try:
            prof = load_professor("700123456", temp_file)
            self.assertIsNone(prof)
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_load_professor_multiple_courses(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            temp_file = f.name
            f.write("PROFESSOR,700555555,Dr. Multi Course,Engineering,10001;10002;10003;10004\n")

        try:
            prof = load_professor("700555555", temp_file)

            self.assertIsNotNone(prof)
            self.assertEqual(len(prof.assigned_courses), 4)
            self.assertIn("10001", prof.assigned_courses)
            self.assertIn("10004", prof.assigned_courses)
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_load_professor_default_database_path(self):
        # Test default path behavior
        try:
            prof = load_professor("700000000")
            self.assertIsNone(prof)
        except FileNotFoundError:
            pass  # Expected if default file doesn't exist


if __name__ == "__main__":
    unittest.main()
