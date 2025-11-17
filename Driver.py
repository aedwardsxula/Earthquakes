import subprocess
import sys
from pathlib import Path

from Admin_files.load_admin import load_admin
from Admin_files.admin_driver import admin_driver


student_folder = Path(__file__).parent / "Student files"
sys.path.insert(0, str(student_folder))

from Student import Student
from load_student import load_student
from student_driver import student_driver

def main_menu():
    while True:
        print("\n===== MAIN MENU =====")
        print("1. Sign Up")
        print("2. Log In")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            run_java_signup()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

def run_java_signup():
    subprocess.run(["java", "SignUp"])

def login():
    name = input("Enter your name: ").strip()
    user_id = input("Enter your ID: ").strip()
    prefix = user_id[:3]

    if prefix == "900":
        student = load_student(user_id=user_id)
        if student is None or student.full_name.lower() != name.lower():
            print("Name or ID incorrect or student not found.")
            return
        for _ in range(50):
            print("\n")
        print(f"Welcome {student.full_name}!")
        student_driver(student)

    elif prefix == "700":
        print("Welcome Professor!")
        
    elif prefix == "800":
        from Functions import clear_screen

        admin = load_admin(user_id=user_id)
        if admin is None or admin.full_name.lower() != name.lower():
            print("Name or ID incorrect or admin not found.")
            return

        clear_screen()
        print(f"Welcome {admin.full_name}!")
        admin_driver(admin)


    else:
        print("Invalid ID prefix.")

if __name__ == "__main__":
    main_menu()
