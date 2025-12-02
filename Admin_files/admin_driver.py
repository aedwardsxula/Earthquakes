import sys
from pathlib import Path
from Course import Course

root_folder = Path(__file__).parent.parent
sys.path.insert(0, str(root_folder))

from Functions import clear_screen
from Functions import admin_input_course
from Functions import create_student_schedule
from Functions import create_schedule
from Functions import manage_fiscal_clearance

def admin_driver(admin):
    all_students_schedules = []
    while True:
        print("\nWelcome to the Admin Portal!! Please Choose an Action from the Menu! ")
        print("\n===== ADMIN MENU =====")
        print("1. Create Course")
        print("2. View Student Schedule")
        print("3. View Admin Info")
        print("4. Create Student Schedule")
        print("5. Edit Student Schedule")
        print("6. View student fiscal clearance status")
        print("7. Create Transcript")
        print("8. View Transcript")
        print("9. Assign Professor to Existing Course")
        print("10. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            clear_screen()
            print("Creating course")
            course = admin_input_course()
            course.print_course_details()
            course.save_to_txt()
            print("Course saved.")

            # Prompt to optionally assign a professor to the newly created course
            prof_id = input("Enter professor 700 number to assign this course (or press Enter to skip): ").strip()
            if prof_id:
                # Dynamically load the professor loader to avoid import path issues
                from pathlib import Path
                import importlib.util

                prof_module_path = Path(__file__).parent.parent / "Professor Files" / "load_professor.py"
                spec = importlib.util.spec_from_file_location("load_professor", prof_module_path)
                load_prof_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(load_prof_module)

                prof = load_prof_module.load_professor(prof_id)
                if prof is None:
                    print(f"Professor with id {prof_id} not found in Accounts.txt. No assignment made.")
                else:
                    success = prof.assign_course(str(course.CRN))
                    if success:
                        print(f"Professor {prof.full_name} (ID {prof.professor_id}) assigned to {course.course_name}.")
                    else:
                        print("Assignment not made (already assigned or file not found).")

        elif choice == "2":
            clear_screen()
            print("Student schedule")
            student_900 = input("Enter student 900 number: ")
            for schedule in all_students_schedules:
                if student_900 in schedule.keys():
                    print(f"Schedule for student {student_900}:")
                    for course in schedule[student_900]:
                        course.print_course_details()
                    break
            else:
                print(f"No schedule found for student {student_900}.")    
            

        elif choice == "3":
            clear_screen()
            admin.display_info()

        elif choice == "4":
            clear_screen()
            print("Create Student Schedule")
            student_900 = input("Enter student 900 number: ")
            new_schedule = create_schedule(student_900)
            all_students_schedules.append({student_900: new_schedule})
            create_new = input("Do you want to create another student schedule? (y/n): ").lower()
            
            while create_new != 'n':
                student_900 = input("Enter student 900 number: ")
                new_schedule = create_schedule(student_900)
                all_students_schedules.append({student_900: new_schedule})
                create_new = input("Do you want to create another student schedule? (y/n): ").lower()

        
        elif choice == "5":
            clear_screen()
            course_action = (input("Add or Remove course from schedule? (a/r): ")).lower()
            if course_action == 'a':
                student_900 = input("Enter student 900 number: ")
                course_to_add = admin_input_course()
                for schedule in all_students_schedules:
                    if student_900 in schedule.keys():
                        course_to_add.add_course_on_student_schedule(schedule[student_900], student_900)
                        print(f"Course {course_to_add.course_name} added to student {student_900}'s schedule.")
                        break
                else:
                    print(f"No schedule found for student {student_900}.")
            elif course_action == 'r':
                student_900 = input("Enter student 900 number: ")
                course_crn_to_remove = input("Enter course crn to remove: ")
                for schedule in all_students_schedules:
                    if student_900 in schedule.keys():
                        for course in schedule[student_900]:
                            if str(course.CRN) == course_crn_to_remove:
                                course.remove_course_from_student_schedule(student_900, schedule[student_900])
                                print(f"Course {course.course_name} removed from student {student_900}'s schedule.")
                                break
                        else:
                            print(f"Course with CRN {course_crn_to_remove} not found in student {student_900}'s schedule.")
                        break
                else:
                    print(f"No schedule found for student {student_900}.")
                    
        elif choice == "6":
            clear_screen()
            manage_fiscal_clearance()

        elif choice == "7":
            clear_screen()
            print("Create Transcript")
            student_name = input("Enter student name: ")
            courses_input = input("Enter courses (comma separated): ")
            courses_list = [course.strip() for course in courses_input.split(",")]
            year = input("Enter year: ")
            semester = input("Enter semester: ")
            credits = input("Enter total credits: ")
            admin.create_transcript(student_name, courses_list, year, semester, credits)

        elif choice == "8":
            clear_screen()
            print("View Transcript")
            student_id = input("Enter student ID to view transcript: ")
            admin.print_transcript(student_id)

        elif choice == "9":
            clear_screen()
            print("Assign Professor to Existing Course")
            crn = input("Enter CRN of the course to assign: ").strip()
            if not crn:
                print("No CRN entered. Returning to menu.")
                continue

            prof_id = input("Enter professor 700 number to assign: ").strip()
            if not prof_id:
                print("No professor id entered. Returning to menu.")
                continue

            # Dynamically load the professor loader and attempt assignment
            from pathlib import Path
            import importlib.util

            prof_module_path = Path(__file__).parent.parent / "Professor Files" / "load_professor.py"
            spec = importlib.util.spec_from_file_location("load_professor", prof_module_path)
            load_prof_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load_prof_module)

            prof = load_prof_module.load_professor(prof_id)
            if prof is None:
                print(f"Professor with id {prof_id} not found in Accounts.txt. No assignment made.")
            else:
                success = prof.assign_course(crn)
                if success:
                    print(f"Professor {prof.full_name} (ID {prof.professor_id}) assigned to CRN {crn}.")
                else:
                    print("Assignment not made (already assigned or matching course file not found).")

        elif choice == "10":
            break

        else:
            print("Invalid choice. Try again.")