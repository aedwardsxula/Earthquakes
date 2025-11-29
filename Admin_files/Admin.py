class Admin:
    def __init__(self, admin_num, full_name):
        self.admin_num = admin_num
        self.full_name = full_name

    def display_info(self):
        print(f"Admin ID: {self.admin_num}")
        print(f"Name: {self.full_name}")

    def add_to_database(self, database):
        def escape(field):
            s = str(field)
            if ',' in s or '"' in s or '\n' in s:
                s = s.replace('"', '""')
                return f'"{s}"'
            return s
            

        parts = ["ADMIN", self.admin_num, self.full_name]
        record = ",".join(escape(p) for p in parts)

        with open(database, "a", encoding="utf-8") as f:
            f.write(record + "\n")
    
    def create_transcript(self, student_name, courses_list, year, semester, credits):
        csv_path = "Database/Transcripts.csv"
        fieldnames = [
            "Student_Name",
            "Student_ID",
            "Courses_List",
            "Year",
            "Semester",
            "Credits"
        ]

        # Ensure CSV file exists
        csv_file = Path(csv_path)
        file_exists = csv_file.exists()

        # Convert list to string for saving
        courses_str = ", ".join(courses_list)

        # Prepare row data
        row = {
            "Student_Name": student_name,
            "Student_ID": self.ID if hasattr(self, 'ID') else "N/A",
            "Courses_List": courses_str,
            "Year": year,
            "Semester": semester,
            "Credits": credits
        }

        # Write to CSV
        with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerow(row)

        print(f"Transcript saved to {csv_path}")
        
