import subprocess
from Student import Student

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
    # Runs: java SignUp
    subprocess.run(["java", "SignUp"])


def login():
    print("\n=== LOGIN ===")
    name = input("Enter your name: ")
    user_id = input("Enter your ID: ")

    prefix = user_id[:3]

    if prefix == "900":
        #This is where the student files would go 
        #Make sure to read Trello
        print(f"Welcome Student!")

    elif prefix == "700":
        #This is where the Professor files would go 
        #Make sure to read Trello
        print(f"Welcome Professor!")

    elif prefix == "800":
        #This is where the Admin files would go 
        #Make sure to read Trello
        print(f"Welcome Admin!")

    else:
        print("Invalid ID prefix.")


if __name__ == "__main__":
    main_menu()
