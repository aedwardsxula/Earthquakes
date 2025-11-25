from Admin_files.Course import Course
from pathlib import Path
import sys

student_folder = Path(__file__).parent / "Student files"
sys.path.insert(0, str(student_folder))

from load_student import load_student

def clear_screen():
    for _ in range(50):
        print("\n")

def admin_input_course():
    course_name = input("Enter course name: ")
    time = input("Enter course time (e.g., MWF 10-11AM): ")
    credits = input("Enter course credits: ")
    
    try:
        credits = int(credits)
    except ValueError:
        print("Invalid credits input. Defaulting to 3 credits.")
        credits = 3
    
    class_list = []
    return Course(course_name, time, credits, class_list)

def create_student_schedule(student_900):
    schedule_list = []
    student_schedule_dict ={student_900: schedule_list}
    return student_schedule_dict

def manage_fiscal_clearance():
    student_900 = input("Enter student 900 number: ").strip()
    
    student = load_student(student_900)
    
    if student is None:
        print(f"Student with ID {student_900} not found.")
        return
    
    print(f"\nStudent: {student.full_name}")
    current_status = student.return_clearance_status()
    print(f"Current Fiscal Clearance Status: {'Cleared' if current_status else 'Not Cleared'}")
    
    change = input("\nWould you like to change the status? (y/n): ").lower()
    
    if change != 'y':
        print("No changes made. Returning to menu.")
        return
    
    new_status = not current_status
    student.change_clearance(new_status)
    
    print(f"\nNew Fiscal Clearance Status: {'Cleared' if new_status else 'Not Cleared'}")
    
    save = input("\nWould you like to save this change? (y/n): ").lower()
    
    if save != 'y':
        print("Changes not saved. Returning to menu.")
        return
    
    update_student_in_database(student)
    print("Changes saved successfully!")

def update_student_in_database(student):
    base_folder = Path(__file__).parent
    database = base_folder / "Database" / "Accounts.txt"
    
    with open(database, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    with open(database, "w", encoding="utf-8") as f:
        for line in lines:
            if line.strip():
                parts = [p.strip().strip('"') for p in line.split(",")]
                if parts[0] == "STUDENT" and parts[1] == student.student_num:
                    f.write(f"STUDENT,{student.student_num},{student.full_name},{student.classification},{student.major},{'true' if student.fiscal_clearance else 'false'}\n")
                else:
                    f.write(line)
            else:
                f.write(line)