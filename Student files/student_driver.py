def student_driver(student):
    while True:
        print("\n===== STUDENT MENU =====")
        print("1. View Info")
        print("2. Change Major")
        print("3. Check Fiscal Clearance")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            student.display_info()
        elif choice == "2":
            new_major = input("Enter new major: ")
            student.change_major(new_major)
            print("Major updated!")
        elif choice == "3":
            print("Fiscal Clearance:", student.return_clearance_status())
        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")
