import sys
from pathlib import Path

root_folder = Path(__file__).parent.parent
sys.path.insert(0, str(root_folder))

from Functions import clear_screen

def student_driver(student):
    while True:
        print("\n===== STUDENT MENU =====")
        print("1. View Info")
        print("2. Change Major")
        print("3. Check Fiscal Clearance")
        print("4. View Schdule")
        print("5. View Previous Schedule(s)")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            clear_screen()
            print(f"Displaying {student.full_name} Information")
            student.display_info()
        elif choice == "2":
            clear_screen()
            new_major = input("Enter new major: ")
            student.change_major(new_major)
            print("Major updated!")
        elif choice == "3":
            clear_screen()
            print("Fiscal Clearance:", student.return_clearance_status())
        elif choice == "4":
            clear_screen()
            print("View Schdule:", student.display_schedule())
        elif choice == "5":
            clear_screen()
            choice_schedule = input("Would you like to view a previous schedule? (yes/no): ").strip().lower()
            while choice_schedule == 'yes':
                year = input("Enter year of schedule to view (e.g., 2023): ")
                term = input("Enter term of schedule to view (e.g., Fall, Spring): ")
                print(f"Viewing previous schedule for {year} {term}:")
                student.view_previous_schedules(year, term)
                choice_schedule = input("Would you like to view another previous schedule? (yes/no): ").strip().lower()
            else:
                print("Returning to main menu.")
                choice = input("Enter choice: ")
        elif choice == "6":
            break
        else:
            print("Invalid choice. Try again.")
