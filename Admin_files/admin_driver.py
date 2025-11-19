import sys
from pathlib import Path
from Admin_files.Course import Course

root_folder = Path(__file__).parent.parent
sys.path.insert(0, str(root_folder))

from Functions import clear_screen
from Functions import admin_input_course
from Functions import create_student_schedule

def admin_driver(admin):
    all_students_schedules = []
    while True:
        print("\n===== ADMIN MENU =====")
        print("1. Create Course")
        print("2. View Student Schedule")
        print("3. View Admin Info")
        print("4. Create Student Schedule")
        print("5. Edit Student Schedule")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            clear_screen()
            print("Creating course")
            course1 = admin_input_course()
            course1.print_course_details()
            course1.save_to_txt()
            print("Course saved.")


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
            new_schedule = create_student_schedule(student_900)
            all_students_schedules.append(new_schedule)
            create_new = input("Do you want to create another student schedule? (y/n): ").lower()
            
            while create_new != 'n':
                student_900 = input("Enter student 900 number: ")
                new_schedule = create_student_schedule(student_900)
                all_students_schedules.append(new_schedule)
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
            break

        else:
            print("Invalid choice. Try again.")
