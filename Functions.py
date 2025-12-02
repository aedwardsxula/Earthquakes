from Admin_files.Course import Course
from pathlib import Path
import sys

student_folder = Path(__file__).parent / "Student files"
sys.path.insert(0, str(student_folder))

from Student_files.load_student import load_student

def clear_screen():
    for _ in range(3):
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


def create_schedule(student_900):
    import os
    
    base_folder = Path(__file__).parent
    courses_folder = base_folder / "Database" / "courses"
    accounts_file = base_folder / "Database" / "Accounts.txt"

    # Build a quick map of professor_id -> professor_name from Accounts.txt
    professor_map = {}
    if accounts_file.exists():
        try:
            with open(accounts_file, 'r', encoding='utf-8') as af:
                for line in af:
                    line = line.strip()
                    if not line:
                        continue
                    parts = [p.strip().strip('"') for p in line.split(',')]
                    if parts and parts[0].upper() in ("PROF", "PROFESSOR") and len(parts) > 2:
                        pid = parts[1]
                        pname = parts[2]
                        professor_map[pid] = pname
        except Exception:
            # if reading accounts fails, continue without professor names
            professor_map = {}
    
    available_courses = []
    
    # Read all course files from the courses folder
    if courses_folder.exists():
        for course_file in os.listdir(courses_folder):
            if course_file.endswith('.txt'):
                course_path = courses_folder / course_file
                
                # Read course details from file
                with open(course_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                    crn = None
                    course_name = None
                    time = "TBA"
                    credits = 3
                    students = []
                    professor_id = None
                    professor_name = None
                    
                    # Parse the file
                    reading_students = False
                    for line in lines:
                        line = line.strip()
                        
                        if line.startswith("crn:"):
                            crn = line.split(":", 1)[1].strip()
                        elif line.startswith("course_name:"):
                            course_name = line.split(":", 1)[1].strip()
                        elif line.startswith("time:"):
                            time = line.split(":", 1)[1].strip()
                        elif line.startswith("credits:"):
                            credits_str = line.split(":", 1)[1].strip()
                            credits = int(credits_str) if credits_str.isdigit() else 3
                        elif line.startswith("professor:"):
                            prof_val = line.split(":", 1)[1].strip()
                            if prof_val and prof_val.lower() != 'none':
                                professor_id = prof_val
                                professor_name = professor_map.get(prof_val)
                        elif line.startswith("students:"):
                            reading_students = True
                        elif reading_students and line and line != "professor: none":
                            students.append(line)
                    
                    # Create Course object if we have valid data
                    if crn and course_name:
                        course = Course(course_name, time, credits, students)
                        course.CRN = int(crn)
                        # attach professor metadata to course instance for display
                        course.professor_id = professor_id
                        course.professor_name = professor_name
                        available_courses.append(course)
    
    if not available_courses:
        print("No courses available in the database.")
        return []
    
    # AUTOMATICALLY create initial schedule
    print(f"\n=== Auto-generating Schedule for Student {student_900} ===")
    selected_courses = auto_select_courses(available_courses, 19)
    
    # Add student to all selected courses
    for course in selected_courses:
        if student_900 not in course.class_list:
            course.class_list.append(student_900)
    
    # Display the auto-generated schedule
    print("\n===== AUTO-GENERATED SCHEDULE =====")
    total_credits = sum(c.credits for c in selected_courses)
    for course in selected_courses:
        prof_display = f"Prof: {course.professor_name}" if getattr(course, 'professor_name', None) else (f"Prof ID: {course.professor_id}" if getattr(course, 'professor_id', None) else "Prof: none")
        print(f"- {course.course_name} ({course.credits} credits) - {course.time} [CRN: {course.CRN}] - {prof_display}")
    print(f"\nTotal Credits: {total_credits}/19")
    
    # Ask if they want to edit
    edit_choice = input("\nWould you like to edit this schedule? (y/n): ").strip().lower()
    
    if edit_choice != 'y':
        print("\nSchedule accepted!")
        return selected_courses
    
    # Now allow editing
    print("\n=== Edit Schedule ===")
    print("\nAvailable courses:")
    for i, course in enumerate(available_courses, 1):
        in_schedule = "✓" if course in selected_courses else " "
        prof_display = f"Prof: {course.professor_name}" if getattr(course, 'professor_name', None) else (f"Prof ID: {course.professor_id}" if getattr(course, 'professor_id', None) else "Prof: none")
        print(f"{in_schedule} {i}. {course.course_name} ({course.credits} credits) - {course.time} [CRN: {course.CRN}] - {prof_display}")
    
    while True:
        print(f"\nCurrent Credits: {total_credits}/19")
        choice = input("\nAdd course number, 'remove' + number to remove, or 'done': ").strip().lower()
        
        if choice == 'done':
            break
        
        if choice.startswith('remove '):
            remove_num = choice.split()[1]
            if remove_num.isdigit():
                course_index = int(remove_num) - 1
                if 0 <= course_index < len(available_courses):
                    course_to_remove = available_courses[course_index]
                    if course_to_remove in selected_courses:
                        selected_courses.remove(course_to_remove)
                        total_credits -= course_to_remove.credits
                        if student_900 in course_to_remove.class_list:
                            course_to_remove.class_list.remove(student_900)
                        print(f"✓ Removed: {course_to_remove.course_name}")
                    else:
                        print("That course is not in the schedule.")
                else:
                    print("Invalid course number.")
        
        elif choice.isdigit():
            course_index = int(choice) - 1
            if 0 <= course_index < len(available_courses):
                selected_course = available_courses[course_index]
                
                if selected_course in selected_courses:
                    print("That course is already in the schedule.")
                elif total_credits + selected_course.credits <= 19:
                    selected_courses.append(selected_course)
                    total_credits += selected_course.credits
                    if student_900 not in selected_course.class_list:
                        selected_course.class_list.append(student_900)
                    print(f"✓ Added: {selected_course.course_name} ({selected_course.credits} credits)")
                else:
                    print(f"✗ Cannot add {selected_course.course_name} - would exceed 19 credits")
            else:
                print("Invalid course number.")
        else:
            print("Invalid input.")
    
    # Display final schedule
    print("\n===== FINAL SCHEDULE =====")
    total_credits = 0
    for course in selected_courses:
        prof_display = f"Prof: {course.professor_name}" if getattr(course, 'professor_name', None) else (f"Prof ID: {course.professor_id}" if getattr(course, 'professor_id', None) else "Prof: none")
        print(f"- {course.course_name} ({course.credits} credits) - {course.time} [CRN: {course.CRN}] - {prof_display}")
        total_credits += course.credits
    print(f"\nTotal Credits: {total_credits}")
    
    return selected_courses

def auto_select_courses(available_courses, max_credits=19):
    
    sorted_courses = sorted(available_courses, key=lambda c: c.credits, reverse=True)
    
    selected = []
    total_credits = 0
    
    for course in sorted_courses:
        if total_credits + course.credits <= max_credits:
            selected.append(course)
            total_credits += course.credits
            
        if total_credits == max_credits:
            break
    
    return selected