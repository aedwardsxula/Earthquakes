import unittest
from pathlib import Path
import sys
import os
import tempfile
import io
from contextlib import redirect_stdout

# Add Professor Files directory to path to import Professor
root_folder = Path(__file__).parent
professor_files_folder = root_folder / "Professor_Files"
sys.path.insert(0, str(professor_files_folder))

from Professor_Files.Professor import Professor


class TestProfessor(unittest.TestCase):
    """Test suite for Professor class"""

    def test_professor_initialization(self):
        prof = Professor("700123456", "Dr. John Smith", "Computer Science")
        self.assertEqual(prof.professor_id, "700123456")
        self.assertEqual(prof.full_name, "Dr. John Smith")
        self.assertEqual(prof.department, "Computer Science")
        self.assertEqual(prof.assigned_courses, [])

    def test_professor_initialization_with_courses(self):
        courses = ["12345", "67890"]
        prof = Professor("700123456", "Dr. Jane Doe", "Mathematics", courses)
        self.assertEqual(prof.assigned_courses, ["12345", "67890"])

    def test_assign_course(self):
        prof = Professor("700123456", "Dr. John Smith", "Computer Science")
        result = prof.assign_course("12345")
        self.assertTrue(result)
        self.assertIn("12345", prof.assigned_courses)
        self.assertEqual(len(prof.assigned_courses), 1)

    def test_assign_duplicate_course(self):
        prof = Professor("700123456", "Dr. John Smith", "Computer Science")
        prof.assign_course("12345")
        result = prof.assign_course("12345")
        self.assertFalse(result)
        self.assertEqual(len(prof.assigned_courses), 1)

    def test_remove_course(self):
        prof = Professor("700123456", "Dr. John Smith", "Computer Science", ["12345", "67890"])
        result = prof.remove_course("12345")
        self.assertTrue(result)
        self.assertNotIn("12345", prof.assigned_courses)
        self.assertEqual(len(prof.assigned_courses), 1)

    def test_remove_nonexistent_course(self):
        prof = Professor("700123456", "Dr. John Smith", "Computer Science", ["12345"])
        result = prof.remove_course("99999")
        self.assertFalse(result)
        self.assertEqual(len(prof.assigned_courses), 1)

    def test_display_info(self):
        """Test stdout capture instead of pytest capsys"""
        prof = Professor("700123456", "Dr. John Smith", "Computer Science", ["12345", "67890"])

        buf = io.StringIO()
        with redirect_stdout(buf):
            prof.display_info()

        output = buf.getvalue()

        self.assertIn("Professor ID: 700123456", output)
        self.assertIn("Full Name: Dr. John Smith", output)
        self.assertIn("Department: Computer Science", output)
        self.assertIn("12345", output)
        self.assertIn("67890", output)

    def test_add_to_database(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_file = f.name

        try:
            prof = Professor("700123456", "Dr. John Smith", "Computer Science", ["12345", "67890"])
            prof.add_to_database(temp_file)

            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            self.assertIn("PROFESSOR", content)
            self.assertIn("700123456", content)
            self.assertIn("Dr. John Smith", content)
            self.assertIn("Computer Science", content)
            self.assertIn("12345;67890", content)

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_add_to_database_no_courses(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_file = f.name

        try:
            prof = Professor("700123456", "Dr. John Smith", "Computer Science")
            prof.add_to_database(temp_file)

            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            self.assertIn("PROFESSOR", content)
            self.assertIn("700123456", content)

            parts = content.split(',')
            self.assertEqual(len(parts), 5)

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_add_to_database_special_characters(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_file = f.name

        try:
            prof = Professor("700123456", "Dr. O'Brien, PhD", "Computer Science")
            prof.add_to_database(temp_file)

            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            self.assertIn("PROFESSOR", content)
            # Allow both quoted and unquoted depending on implementation
            self.assertTrue(
                "Dr. O'Brien, PhD" in content or '"Dr. O\'Brien, PhD"' in content
            )

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_multiple_course_operations(self):
        prof = Professor("700123456", "Dr. John Smith", "Computer Science")

        prof.assign_course("11111")
        prof.assign_course("22222")
        prof.assign_course("33333")
        self.assertEqual(len(prof.assigned_courses), 3)

        prof.remove_course("22222")
        self.assertEqual(len(prof.assigned_courses), 2)
        self.assertNotIn("22222", prof.assigned_courses)
        self.assertIn("11111", prof.assigned_courses)
        self.assertIn("33333", prof.assigned_courses)


if __name__ == "__main__":
    unittest.main()
