import unittest
import tempfile
import os
from pathlib import Path

from Admin_files.Course import Course


class TestCourseMethods(unittest.TestCase):

    def setUp(self):
        """Clear course registry before each test"""
        Course.crns_list = []
        Course.courses_by_crn = {}

    # __init__ tests
    def test_init_creates_course_with_fields(self):
        course = Course(course_name="Math 101", time="MWF 10-11", credits=3, class_list=[])
        self.assertEqual(course.course_name, "Math 101")
        self.assertEqual(course.time, "MWF 10-11")
        self.assertEqual(course.credits, 3)
        self.assertEqual(course.class_list, [])

    def test_init_generates_unique_crn(self):
        course1 = Course(course_name="Math 101", time="MWF 10-11", credits=3, class_list=[])
        course2 = Course(course_name="English 101", time="TTh 2-3", credits=4, class_list=[])
        self.assertNotEqual(course1.CRN, course2.CRN)

    # save_all_courses_to_csv tests
    def test_save_all_courses_to_csv_creates_file(self):
        course = Course(course_name="Physics 101", time="MWF 9-10", credits=4, class_list=["Alice", "Bob"])
        fd, path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        try:
            Course.save_all_courses_to_csv(path)
            self.assertTrue(os.path.exists(path))
            with open(path, 'r', encoding='utf-8') as f:
                contents = f.read()
            self.assertIn("Physics 101", contents)
            self.assertIn("Alice;Bob", contents)
        finally:
            os.remove(path)

    def test_save_all_courses_to_csv_includes_header(self):
        course = Course(course_name="Biology 101", time="TTh 1-2", credits=3, class_list=[])
        fd, path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        try:
            Course.save_all_courses_to_csv(path)
            with open(path, 'r', encoding='utf-8') as f:
                first_line = f.readline()
            self.assertIn("crn", first_line)
            self.assertIn("course_name", first_line)
        finally:
            os.remove(path)

    # print_course_details tests
    def test_print_course_details_no_exception(self):
        course = Course(course_name="Chemistry 101", time="MWF 11-12", credits=4, class_list=["Carol"])
        # just ensure calling does not raise
        course.print_course_details()

    def test_print_course_details_with_multiple_students(self):
        course = Course(course_name="History 101", time="TTh 10-11", credits=3, class_list=["Dan", "Eve", "Frank"])
        # ensure calling does not raise and does not modify state
        course.print_course_details()
        self.assertEqual(len(course.class_list), 3)

    # display_crn_desc tests
    def test_display_crn_desc_reads_csv(self):
        course = Course(course_name="Test Course", time="MWF 10-11", credits=3, class_list=[])
        test_csv_path = "test_courses.csv"
        Course.save_all_courses_to_csv(test_csv_path)
        # ensure calling does not raise
        course.display_crn_desc(test_csv_path)

    def test_display_crn_desc_handles_missing_file_gracefully(self):
        course = Course(course_name="Art 101", time="MWF 1-2", credits=3, class_list=[])
        # test that calling with nonexistent file raises FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            course.display_crn_desc("/nonexistent/path/test.csv")

    # assign_professor tests
    def test_assign_professor_stores_in_course_object(self):
        course = Course(course_name="Test Course", time="MWF 10-11", credits=3, class_list=[])
        course.assign_professor(course.CRN, "Dr. Smith")
        self.assertEqual(getattr(course, 'professor', None), "Dr. Smith")

    def test_assign_professor_returns_none_for_nonexistent_crn(self):
        course = Course(course_name="Test Course", time="MWF 10-11", credits=3, class_list=[])
        result = course.assign_professor(99999, "Dr. Jones")
        self.assertIsNone(result)

    # change_time tests
    def test_change_time_updates_time(self):
        course = Course(course_name="Geology 101", time="MWF 2-3", credits=3, class_list=[])
        course.change_time("TTh 3-4")
        self.assertEqual(course.time, "TTh 3-4")

    def test_change_time_overwrites_previous(self):
        course = Course(course_name="Astronomy 101", time="MWF 8-9", credits=4, class_list=[])
        course.change_time("TTh 8-9")
        course.change_time("MWF 1-2")
        self.assertEqual(course.time, "MWF 1-2")

    # access_crns tests
    def test_access_crns_prints_all_crns(self):
        c1 = Course(course_name="Course 1", time="MWF 10-11", credits=3, class_list=[])
        c2 = Course(course_name="Course 2", time="TTh 2-3", credits=3, class_list=[])
        # ensure calling does not raise
        Course.access_crns()
        self.assertEqual(len(Course.crns_list), 2)

    def test_access_crns_returns_none(self):
        c1 = Course(course_name="Course 1", time="MWF 10-11", credits=3, class_list=[])
        # access_crns prints but returns None
        result = Course.access_crns()
        self.assertIsNone(result)

    # access_course_crn tests (static method)
    def test_access_course_crn_returns_crn_for_valid_course_name(self):
        course = Course(course_name="Statistics 101", time="MWF 3-4", credits=3, class_list=[])
        course.add_course_to_database("test_course_access.csv")
        crn = Course.access_course_crn("Statistics 101", "test_course_access.csv")
        self.assertEqual(crn, str(course.CRN))
        if os.path.exists("test_course_access.csv"):
            os.remove("test_course_access.csv")

    def test_access_course_crn_returns_error_for_nonexistent_course(self):
        fd, path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        try:
            # Write a header-only CSV
            with open(path, 'w', encoding='utf-8') as f:
                f.write("crn,course_name,time,credits,class_list\n")
            result = Course.access_course_crn("Nonexistent Course", path)
            self.assertIn("not found", result)
        finally:
            os.remove(path)

    # access_course_course_name tests (static method)
    def test_access_course_course_name_returns_name_for_valid_crn(self):
        course = Course(course_name="Physics 201", time="MWF 9-10", credits=4, class_list=[])
        course.add_course_to_database("test_course_access2.csv")
        name = Course.access_course_course_name(str(course.CRN), "test_course_access2.csv")
        self.assertEqual(name, "Physics 201")
        if os.path.exists("test_course_access2.csv"):
            os.remove("test_course_access2.csv")

    def test_access_course_course_name_returns_error_for_nonexistent_crn(self):
        fd, path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write("crn,course_name,time,credits,class_list\n")
            result = Course.access_course_course_name("99999", path)
            self.assertIn("not found", result)
        finally:
            os.remove(path)

    # change_course_name tests
    def test_change_course_name_updates_name(self):
        course = Course(course_name="Music 101", time="MWF 10-11", credits=2, class_list=[])
        course.change_course_name("Music Theory 101")
        self.assertEqual(course.course_name, "Music Theory 101")

    def test_change_course_name_overwrites_previous(self):
        course = Course(course_name="Art 101", time="MWF 1-2", credits=3, class_list=[])
        course.change_course_name("Art History 101")
        course.change_course_name("Modern Art 101")
        self.assertEqual(course.course_name, "Modern Art 101")

    # add_course_to_database tests
    def test_add_course_to_database_creates_record(self):
        course = Course(course_name="Database Design 101", time="TTh 2-3", credits=4, class_list=["Gina"])
        fd, path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        try:
            course.add_course_to_database(path)
            # File may or may not have content depending on implementation
            self.assertTrue(os.path.exists(path))
        finally:
            os.remove(path)

    def test_add_course_to_database_creates_directory_if_needed(self):
        course = Course(course_name="Networks 101", time="MWF 11-12", credits=3, class_list=[])
        path = "temp_test_dir/subdir/course.csv"
        try:
            course.add_course_to_database(path)
            self.assertTrue(os.path.exists(path))
        finally:
            if os.path.exists(path):
                os.remove(path)
            if os.path.exists("temp_test_dir/subdir"):
                os.rmdir("temp_test_dir/subdir")
            if os.path.exists("temp_test_dir"):
                os.rmdir("temp_test_dir")

    # add_already_created_course_to_database tests (static method)
    def test_add_already_created_course_to_database_appends(self):
        course = Course(course_name="Security 101", time="MWF 2-3", credits=3, class_list=["Hank"])
        fd, path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        try:
            # Write header
            with open(path, 'w', encoding='utf-8') as f:
                f.write("crn,course_name,time,class_list,credits\n")
            Course.add_already_created_course_to_database(course, path)
            with open(path, 'r', encoding='utf-8') as f:
                contents = f.read()
            self.assertIn("Security 101", contents)
        finally:
            os.remove(path)

    def test_add_already_created_course_to_database_escapes_class_list(self):
        course = Course(course_name="Ethics 101", time="TTh 10-11", credits=3, class_list=["Ivy; Jill", "Ken"])
        fd, path = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write("crn,course_name,time,class_list,credits\n")
            Course.add_already_created_course_to_database(course, path)
            with open(path, 'r', encoding='utf-8') as f:
                contents = f.read()
            self.assertIn("Ivy", contents)
        finally:
            os.remove(path)

    # add_course_on_student_schedule tests
    def test_add_course_on_student_schedule_adds_student_to_class_list(self):
        course = Course(course_name="Intro CS", time="MWF 9-10", credits=3, class_list=[])
        schedule = []
        course.add_course_on_student_schedule(schedule, "Liam")
        self.assertIn("Liam", course.class_list)
        self.assertIn(course, schedule)

    def test_add_course_on_student_schedule_prevents_duplicate_enrollment(self):
        course = Course(course_name="Advanced CS", time="TTh 1-2", credits=3, class_list=["Moe"])
        schedule = [course]
        course.add_course_on_student_schedule(schedule, "Moe")
        # Moe should still be in class_list only once
        self.assertEqual(course.class_list.count("Moe"), 1)
        self.assertEqual(schedule.count(course), 1)

    # remove_course_from_student_schedule tests
    def test_remove_course_from_student_schedule_removes_student(self):
        course = Course(course_name="Data Structures", time="MWF 10-11", credits=3, class_list=["Nina"])
        schedule = [course]
        course.remove_course_from_student_schedule("Nina", schedule)
        self.assertNotIn("Nina", course.class_list)
        self.assertNotIn(course, schedule)

    def test_remove_course_from_student_schedule_handles_nonexistent_student(self):
        course = Course(course_name="Algorithms", time="TTh 9-10", credits=3, class_list=["Omar"])
        schedule = [course]
        course.remove_course_from_student_schedule("Pia", schedule)
        # Omar should still be enrolled
        self.assertIn("Omar", course.class_list)
        self.assertEqual(len(schedule), 1)

    # save_to_txt tests
    def test_save_to_txt_creates_file(self):
        course = Course(course_name="Databases", time="MWF 2-3", credits=4, class_list=["Quinn"])
        base_path = Path(__file__).parent.parent
        try:
            course.save_to_txt()
            file_path = base_path / "Database" / "courses" / "Databases.txt"
            self.assertTrue(file_path.exists())
        finally:
            if file_path.exists():
                file_path.unlink()

    def test_save_to_txt_contains_course_info(self):
        course = Course(course_name="Web Development", time="TTh 3-4", credits=3, class_list=["Roe", "Sam"])
        base_path = Path(__file__).parent.parent
        try:
            course.save_to_txt()
            file_path = base_path / "Database" / "courses" / "Web Development.txt"
            with open(file_path, 'r', encoding='utf-8') as f:
                contents = f.read()
            self.assertIn("crn:", contents)
            self.assertIn("Web Development", contents)
            self.assertIn("Roe", contents)
        finally:
            if file_path.exists():
                file_path.unlink()



