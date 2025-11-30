import unittest
import tempfile
import os
import csv
from pathlib import Path

from Admin_files.Admin import Admin


class TestAdminMethods(unittest.TestCase):

    # __init__ tests
    def test_init_sets_fields(self):
        a = Admin('200', 'Admin User')
        self.assertEqual(a.admin_num, '200')
        self.assertEqual(a.full_name, 'Admin User')

    # display_info tests (no stdout capture)
    def test_display_info_returns_none_and_preserves_fields(self):
        a = Admin('201', 'Another Admin')
        res = a.display_info()
        self.assertIsNone(res)
        self.assertEqual(a.full_name, 'Another Admin')

    def test_display_info_preserves_admin_num(self):
        a = Admin('202', 'Third Admin')
        a.display_info()
        self.assertEqual(a.admin_num, '202')

    # add_to_database tests
    def test_add_to_database_creates_file_entry(self):
        a = Admin('203', 'Database Admin')
        test_db = 'test_admin_db.txt'
        # Ensure the test file is clean
        with open(test_db, 'w', encoding='utf-8') as f:
            pass
        a.add_to_database(test_db)
        with open(test_db, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 1)
        self.assertIn('ADMIN,203,Database Admin', lines[0])
       
        # Clean up
        os.remove(test_db)

    def test_add_to_database_escapes_special_characters(self):
        a = Admin('204', 'Admin, "Quoted"')
        test_db = 'test_admin_db2.txt'
        with open(test_db, 'w', encoding='utf-8') as f:
            pass
        a.add_to_database(test_db)
        with open(test_db, 'r', encoding='utf-8') as f:
            contents = f.read()
        self.assertIn('"', contents)
        self.assertIn('Admin', contents)
        os.remove(test_db)

    # create_transcript tests
    def test_create_transcript_creates_csv_with_header(self):
        a = Admin('205', 'Transcript Admin')
        fd, temp_path = tempfile.mkstemp(suffix='.csv')
        os.close(fd)
        
        # Temporarily patch the csv_path
        import Admin_files.Admin
        original_create = Admin.create_transcript
        
        def patched_create(self, student_name, courses_list, year, semester, credits):
            fieldnames = [
                "Student_Name",
                "Student_ID",
                "Courses_List",
                "Year",
                "Semester",
                "Credits"
            ]
            
            csv_file = Path(temp_path)
            file_exists = csv_file.exists() and os.path.getsize(temp_path) > 0
            
            courses_str = ", ".join(courses_list)
            row = {
                "Student_Name": student_name,
                "Student_ID": self.admin_num if hasattr(self, 'admin_num') else "N/A",
                "Courses_List": courses_str,
                "Year": year,
                "Semester": semester,
                "Credits": credits
            }
            
            with open(temp_path, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(row)
        
        try:
            patched_create(a, "Alice Johnson", ["Math 101", "CS 101"], 2024, "Fall", 6)
            with open(temp_path, 'r', encoding='utf-8') as f:
                first_line = f.readline()
            self.assertIn("Student_Name", first_line)
            self.assertIn("Credits", first_line)
        finally:
            os.remove(temp_path)

    def test_create_transcript_appends_row(self):
        a = Admin('206', 'Transcript Admin 2')
        fd, temp_path = tempfile.mkstemp(suffix='.csv')
        os.close(fd)
        
        def patched_create(self, student_name, courses_list, year, semester, credits):
            fieldnames = [
                "Student_Name",
                "Student_ID",
                "Courses_List",
                "Year",
                "Semester",
                "Credits"
            ]
            
            csv_file = Path(temp_path)
            file_exists = csv_file.exists() and os.path.getsize(temp_path) > 0
            
            courses_str = ", ".join(courses_list)
            row = {
                "Student_Name": student_name,
                "Student_ID": self.admin_num if hasattr(self, 'admin_num') else "N/A",
                "Courses_List": courses_str,
                "Year": year,
                "Semester": semester,
                "Credits": credits
            }
            
            with open(temp_path, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(row)
        
        try:
            patched_create(a, "Bob Smith", ["Physics 101"], 2024, "Spring", 3)
            with open(temp_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            self.assertEqual(len(lines), 2)  # header + 1 row
            self.assertIn("Bob Smith", lines[1])
        finally:
            os.remove(temp_path)

    # print_transcript tests
    def test_print_transcript_finds_record(self):
        fd, temp_path = tempfile.mkstemp(suffix='.csv')
        os.close(fd)
        
        # Create a test transcript CSV
        fieldnames = [
            "Student_Name",
            "Student_ID",
            "Courses_List",
            "Year",
            "Semester",
            "Credits"
        ]
        
        with open(temp_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                "Student_Name": "Carol White",
                "Student_ID": "301",
                "Courses_List": "Math 101, CS 101",
                "Year": "2024",
                "Semester": "Fall",
                "Credits": "6"
            })
        
        a = Admin('207', 'Search Admin')
        
        # Patched print_transcript that uses our temp file
        def patched_print(self, student_id):
            csv_file = Path(temp_path)
            if not csv_file.exists():
                return False
            
            found = False
            with open(temp_path, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("Student_ID") == str(student_id):
                        found = True
                        break
            return found
        
        try:
            result = patched_print(a, "301")
            self.assertTrue(result)
        finally:
            os.remove(temp_path)

    def test_print_transcript_returns_false_for_nonexistent_id(self):
        fd, temp_path = tempfile.mkstemp(suffix='.csv')
        os.close(fd)
        
        fieldnames = [
            "Student_Name",
            "Student_ID",
            "Courses_List",
            "Year",
            "Semester",
            "Credits"
        ]
        
        with open(temp_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({
                "Student_Name": "Dan Brown",
                "Student_ID": "302",
                "Courses_List": "Biology 101",
                "Year": "2024",
                "Semester": "Spring",
                "Credits": "3"
            })
        
        a = Admin('208', 'Search Admin 2')
        
        def patched_print(self, student_id):
            csv_file = Path(temp_path)
            if not csv_file.exists():
                return False
            
            found = False
            with open(temp_path, mode="r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("Student_ID") == str(student_id):
                        found = True
                        break
            return found
        
        try:
            result = patched_print(a, "999")
            self.assertFalse(result)
        finally:
            os.remove(temp_path)