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
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            clear_screen()
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
            break
        else:
            print("Invalid choice. Try again.")
