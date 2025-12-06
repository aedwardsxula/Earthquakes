import sys
from pathlib import Path

root_folder = Path(__file__).parent.parent
sys.path.insert(0, str(root_folder))

admin_folder = Path(__file__).parent.parent / "Admin_files"
sys.path.insert(0, str(admin_folder))

from Course import Course
from Functions import clear_screen

def professor_driver(professor):
    while True:
        print("\n===== PROFESSOR MENU =====")
        print("1. View Assigned Courses")
        print("2. See Enrolled Students")
        print("3. Change Course Time")
        print("4. Drop Student from Course")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            clear_screen()
            print(f"\n{professor.full_name}'s Assigned Courses:")
            if professor.assigned_courses:
                for crn in professor.assigned_courses:
                    # Look up course details from Course registry
                    if crn in Course.courses_by_crn:
                        course = Course.courses_by_crn[crn]
                        print(f"\nCRN: {course.CRN}")
                        print(f"Course Name: {course.course_name}")
                        print(f"Time: {course.time}")
                        print(f"Enrolled Students: {len(course.class_list)}")
                    else:
                        print(f"\nCRN: {crn} (Course details not loaded)")
            else:
                print("No courses assigned.")

        elif choice == "2":
            clear_screen()
            if not professor.assigned_courses:
                print("You have no assigned courses.")
                continue
            crn = input("Enter CRN of course to view students: ").strip()
            
            if crn not in professor.assigned_courses:
                print(f"CRN {crn} is not assigned to you.")
                continue
            
            if crn in Course.courses_by_crn:
                course = Course.courses_by_crn[crn]
                print(f"\nCourse: {course.course_name}")
                print(f"CRN: {course.CRN}")
                print(f"Time: {course.time}")
                print(f"\nEnrolled Students ({len(course.class_list)}):")
                if course.class_list:
                    for i, student in enumerate(course.class_list, 1):
                        print(f"{i}. {student}")
                else:
                    print("No students enrolled.")
            else:
                print(f"Course with CRN {crn} not found in system.")

        elif choice == "3":
            clear_screen()
            if not professor.assigned_courses:
                print("You have no assigned courses.")
                continue
            
            crn = input("Enter CRN of course to change time: ").strip()
            
            if crn not in professor.assigned_courses:
                print(f"CRN {crn} is not assigned to you.")
                continue
            
            if crn in Course.courses_by_crn:
                course = Course.courses_by_crn[crn]
                print(f"\nCourse: {course.course_name}")
                print(f"Current Time: {course.time}")
                
                new_time = input("Enter new time (e.g., MWF 10-11AM): ").strip()
                course.change_time(new_time)
                print(f"Course time updated to: {new_time}")
                
                # Save changes to course file
                course.save_to_txt()
                print("Changes saved.")
            else:
                print(f"Course with CRN {crn} not found in system.")

        elif choice == "4":
            clear_screen()
            if not professor.assigned_courses:
                print("You have no assigned courses.")
                continue
            
            crn = input("Enter CRN of course: ").strip()
            
            if crn not in professor.assigned_courses:
                print(f"CRN {crn} is not assigned to you.")
                continue
            
            if crn in Course.courses_by_crn:
                course = Course.courses_by_crn[crn]
                print(f"\nCourse: {course.course_name}")
                print(f"Enrolled Students: {len(course.class_list)}")
                
                if not course.class_list:
                    print("No students enrolled in this course.")
                    continue
                for i, student in enumerate(course.class_list, 1):
                    print(f"{i}. {student}")
                
                student_id = input("\nEnter student ID to drop: ").strip()
                
                if student_id in course.class_list:
                    course.class_list.remove(student_id)
                    print(f"Student {student_id} dropped from {course.course_name}.")
                    
                    # Save changes to course file
                    course.save_to_txt()
                    print("Changes saved.")
                else:
                    print(f"Student {student_id} not found in this course.")
            else:
                print(f"Course with CRN {crn} not found in system.")

        elif choice == "5":
            break

        else:
            print("Invalid choice. Try again.")