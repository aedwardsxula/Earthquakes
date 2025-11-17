import sys
from pathlib import Path

root_folder = Path(__file__).parent.parent
sys.path.insert(0, str(root_folder))

from Functions import clear_screen

def admin_driver(admin):
    while True:
        print("\n===== ADMIN MENU =====")
        print("1. Create Course")
        print("2. View Student Schedule")
        print("3. View Admin Info")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            clear_screen()
            print("Creating course")

        elif choice == "2":
            clear_screen()
            print("Student schedule")

        elif choice == "3":
            clear_screen()
            admin.display_info()

        elif choice == "4":
            break

        else:
            print("Invalid choice. Try again.")
