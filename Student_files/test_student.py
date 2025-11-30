import unittest
import tempfile
import os

from Student_files.Student import Student


class TestStudentMethods(unittest.TestCase):

    # __init__ / normalization tests
    def test_init_with_string_true(self):
        s = Student('100', 'Alice', 'Senior', 'CS', 'Yes')
        self.assertTrue(s.fiscal_clearance)

    def test_init_with_numeric_zero_false(self):
        s = Student('101', 'Bob', 'Junior', 'Math', 0)
        self.assertFalse(s.fiscal_clearance)

    # display_info tests (no stdout capture)
    def test_display_info_returns_none_and_preserves_fields(self):
        s = Student('102', 'Carol', 'Sophomore', 'Eng', True)
        res = s.display_info()
        self.assertIsNone(res)
        self.assertEqual(s.full_name, 'Carol')

    def test_display_info_preserves_major_and_clearance(self):
        s = Student('103', 'Dan', 'Freshman', 'Bio', False)
        s.display_info()
        self.assertEqual(s.major, 'Bio')
        self.assertFalse(s.fiscal_clearance)

    # display_schedule tests
    def test_display_schedule_returns_none(self):
        s = Student('104', 'Eve', 'Senior', 'Chem', True)
        self.assertIsNone(s.display_schedule())

    def test_display_schedule_no_exception(self):
        s = Student('105', 'Frank', 'Senior', 'Hist', True)
        # just ensure calling does not raise
        s.display_schedule()

    # return_clearance_status tests
    def test_return_clearance_status_true(self):
        s = Student('106', 'Gina', 'Senior', 'Art', '1')
        self.assertTrue(s.return_clearance_status())

    def test_return_clearance_status_false(self):
        s = Student('107', 'Hank', 'Senior', 'Phil', '')
        self.assertFalse(s.return_clearance_status())

    # change_major tests
    def test_change_major_updates(self):
        s = Student('108', 'Ivy', 'Junior', 'Math', True)
        s.change_major('Physics')
        self.assertEqual(s.major, 'Physics')

    def test_change_major_overwrites(self):
        s = Student('109', 'Jill', 'Junior', 'Music', True)
        s.change_major('Art')
        self.assertEqual(s.major, 'Art')

    # change_clearance tests
    def test_change_clearance_from_str(self):
        s = Student('110', 'Ken', 'Sophomore', 'CS', False)
        s.change_clearance('yes')
        self.assertTrue(s.fiscal_clearance)

    def test_change_clearance_from_int_zero(self):
        s = Student('111', 'Liam', 'Freshman', 'Econ', True)
        s.change_clearance(0)
        self.assertFalse(s.fiscal_clearance)

    # update_name tests
    def test_update_name_changes(self):
        s = Student('112', 'Moe', 'Senior', 'Phil', True)
        s.update_name('Moses')
        self.assertEqual(s.full_name, 'Moses')

    def test_update_name_overwrites(self):
        s = Student('113', 'Nina', 'Senior', 'Phil', True)
        s.update_name('Nina B')
        self.assertEqual(s.full_name, 'Nina B')

    # update_classification tests
    def test_update_classification_changes(self):
        s = Student('114', 'Omar', 'Junior', 'CS', True)
        s.update_classification('Senior')
        self.assertEqual(s.classification, 'Senior')

    def test_update_classification_overwrites(self):
        s = Student('115', 'Pia', 'Sophomore', 'Math', True)
        s.update_classification('Junior')
        self.assertEqual(s.classification, 'Junior')

    # add_to_database tests
    def test_add_to_database_appends_line(self):
        s = Student('116', 'Quinn', 'Senior', 'CS', True)
        fd, path = tempfile.mkstemp()
        os.close(fd)
        try:
            s.add_to_database(path)
            with open(path, 'r', encoding='utf-8') as f:
                contents = f.read()
            self.assertIn('STUDENT', contents)
            self.assertIn('Quinn', contents)
        finally:
            os.remove(path)

    def test_add_to_database_escapes_commas_and_quotes(self):
        s = Student('117', 'Roe, "Quoted"', 'Senior', 'CS', False)
        fd, path = tempfile.mkstemp()
        os.close(fd)
        try:
            s.add_to_database(path)
            with open(path, 'r', encoding='utf-8') as f:
                line = f.readline()
            # ensure that a quoted comma is escaped by quoting the field
            self.assertIn('"', line)
            self.assertIn('Roe', line)
        finally:
            os.remove(path)
    
    def test_view_previous_schedules_no_file(self):
        s = Student('118', 'Sam', 'Senior', 'CS', True)
        # Should not raise even if file does not exist
        s.view_previous_schedules(2023, 'Fall')

