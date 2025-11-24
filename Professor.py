class Professor:
    def __init__(self, professor_id, full_name, department, assigned_courses=None):
        self.professor_id = professor_id
        self.full_name = full_name
        self.department = department
        self.assigned_courses = assigned_courses if assigned_courses is not None else []

    def display_info(self):
        print(f"Professor ID: {self.professor_id}")
        print(f"Full Name: {self.full_name}")
        print(f"Department: {self.department}")
        print("Assigned Courses:")
        for course in self.assigned_courses:
            print(f" - {course}")

    def assign_course(self, crn):
        if crn not in self.assigned_courses:
            self.assigned_courses.append(crn)
            print(f"Course {crn} assigned to Professor {self.full_name}.")
            return True
        else:
            print(f"Course {crn} is already assigned to Professor {self.full_name}.")
        return False

    def remove_course(self, crn):
        if crn in self.assigned_courses:
            self.assigned_courses.remove(crn)
            print(f"Course {crn} removed from Professor {self.full_name}.")
            return True
        return False
    
    def add_to_database(self, database):
        
        def escape(field):
            s = str(field)
            if ',' in s or '"' in s or '\n' in s:
                s = s.replace('"', '""')
                return f'"{s}"'
            return s

        courses_str = ';'.join(self.assigned_courses) if self.assigned_courses else ''
        
        parts = ["PROFESSOR", self.professor_id, self.full_name, self.department, courses_str]
        record = ",".join(escape(p) for p in parts)

        with open(database, "a", encoding="utf-8") as f:
            f.write(record + "\n")
    