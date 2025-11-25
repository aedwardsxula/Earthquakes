import pytest
from pathlib import Path
import sys
import os
import tempfile

# Add Professor Files directory to path to import Professor
root_folder = Path(__file__).parent
professor_files_folder = root_folder / "Professor Files"
sys.path.insert(0, str(professor_files_folder))

from Professor import Professor


class TestProfessor:
    """Test suite for Professor class"""

    def test_professor_initialization(self):
        """Test that a professor is initialized correctly"""
        prof = Professor("700123456", "Dr. John Smith", "Computer Science")
        assert prof.professor_id == "700123456"
        assert prof.full_name == "Dr. John Smith"
        assert prof.department == "Computer Science"
        assert prof.assigned_courses == []

    def test_professor_initialization_with_courses(self):
        """Test professor initialization with pre-assigned courses"""
        courses = ["12345", "67890"]
        prof = Professor("700123456", "Dr. Jane Doe", "Mathematics", courses)
        assert prof.assigned_courses == ["12345", "67890"]
    def test_assign_course(self):
        """Test assigning a course to a professor"""
        prof = Professor("700123456", "Dr. John Smith", "Computer Science")
        result = prof.assign_course("12345")
        assert result == True
        assert "12345" in prof.assigned_courses
        assert len(prof.assigned_courses) == 1

    def test_assign_duplicate_course(self):
        """Test that assigning a duplicate course returns False"""
        prof = Professor("700123456", "Dr. John Smith", "Computer Science")
        prof.assign_course("12345")
        result = prof.assign_course("12345")
        assert result == False
        assert len(prof.assigned_courses) == 1

    def test_remove_course(self):
        """Test removing a course from professor"""
        prof = Professor("700123456", "Dr. John Smith", "Computer Science", ["12345", "67890"])
        result = prof.remove_course("12345")
        assert result == True
        assert "12345" not in prof.assigned_courses
        assert len(prof.assigned_courses) == 1

    def test_remove_nonexistent_course(self):
        """Test removing a course that doesn't exist"""
        prof = Professor("700123456", "Dr. John Smith", "Computer Science", ["12345"])
        result = prof.remove_course("99999")
        assert result == False
        assert len(prof.assigned_courses) == 1

    def test_display_info(self, capsys):
        """Test that display_info prints correct information"""
        prof = Professor("700123456", "Dr. John Smith", "Computer Science", ["12345", "67890"])
        prof.display_info()
        captured = capsys.readouterr()
        assert "Professor ID: 700123456" in captured.out
        assert "Full Name: Dr. John Smith" in captured.out
        assert "Department: Computer Science" in captured.out
        assert "12345" in captured.out
        assert "67890" in captured.out

    def test_add_to_database(self):
        """Test adding professor to database file"""
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_file = f.name

        try:
            prof = Professor("700123456", "Dr. John Smith", "Computer Science", ["12345", "67890"])
            prof.add_to_database(temp_file)

            # Read the file and verify content
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            assert "PROFESSOR" in content
            assert "700123456" in content
            assert "Dr. John Smith" in content
            assert "Computer Science" in content
            assert "12345;67890" in content

        finally:
            # Clean up temporary file
            if os.path.exists(temp_file):
                os.remove(temp_file)
    def test_add_to_database_no_courses(self):
        """Test adding professor with no courses to database"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_file = f.name

        try:
            prof = Professor("700123456", "Dr. John Smith", "Computer Science")
            prof.add_to_database(temp_file)

            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            assert "PROFESSOR" in content
            assert "700123456" in content
            # Should have empty string for courses
            parts = content.split(',')
            assert len(parts) == 5  # PROFESSOR, id, name, dept, courses(empty)

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_add_to_database_special_characters(self):
        """Test adding professor with special characters in name"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_file = f.name

        try:
            prof = Professor("700123456", "Dr. O'Brien, PhD", "Computer Science")
            prof.add_to_database(temp_file)

            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            assert "PROFESSOR" in content
            assert "Dr. O'Brien, PhD" in content or '"Dr. O\'Brien, PhD"' in content

        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def test_multiple_course_operations(self):
        """Test multiple assign and remove operations"""
        prof = Professor("700123456", "Dr. John Smith", "Computer Science")
        
        prof.assign_course("11111")
        prof.assign_course("22222")
        prof.assign_course("33333")
        assert len(prof.assigned_courses) == 3
        
        prof.remove_course("22222")
        assert len(prof.assigned_courses) == 2
        assert "22222" not in prof.assigned_courses
        assert "11111" in prof.assigned_courses
        assert "33333" in prof.assigned_courses


if __name__ == "__main__":
    pytest.main([__file__, "-v"])