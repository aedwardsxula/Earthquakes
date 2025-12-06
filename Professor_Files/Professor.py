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

    def assign_course(self, crn, persist=False, courses_dir="Database/courses"):
        """
        Assign a course to this professor.

        Parameters:
        - crn: int or str - the course CRN to assign
        - persist: bool - update matching course file on disk (default False)
        - courses_dir: directory containing course files

        Returns True if assignment succeeded, False otherwise.
        """
        from pathlib import Path
        import shutil

        crn_str = str(crn).strip()

        # Already assigned?
        if crn_str in [str(c).strip() for c in self.assigned_courses]:
            print(f"Course {crn} is already assigned to Professor {self.full_name}.")
            return False

        # If persistence is enabled, update the course file
        if persist:
            courses_path = Path(courses_dir)
            if not courses_path.exists() or not courses_path.is_dir():
                raise FileNotFoundError(f"Courses directory not found: {courses_path}")

            found = False
            for course_file in courses_path.glob("*.txt"):
                try:
                    text = course_file.read_text(encoding="utf-8").splitlines()
                except Exception:
                    continue

                # Extract CRN from file
                file_crn = None
                crn_index = None
                for i, line in enumerate(text):
                    if line.lower().startswith("crn:"):
                        file_crn = line.split(":", 1)[1].strip()
                        crn_index = i
                        break

                if file_crn != crn_str:
                    continue

                # Found a matching file — update professor line
                new_prof_line = f"professor: {self.professor_id}"

                prof_index = None
                for j, line in enumerate(text):
                    if line.lower().startswith("professor:"):
                        prof_index = j
                        break

                # Create backup
                backup_path = course_file.with_suffix(".bak")
                shutil.copy2(course_file, backup_path)

                if prof_index is not None:
                    text[prof_index] = new_prof_line
                else:
                    # Insert professor below credits or CRN
                    insert_at = None
                    for j, line in enumerate(text):
                        if line.lower().startswith("credits:"):
                            insert_at = j + 1
                            break
                    if insert_at is None and crn_index is not None:
                        insert_at = crn_index + 1
                    if insert_at is None:
                        text.append(new_prof_line)
                    else:
                        text.insert(insert_at, new_prof_line)

                course_file.write_text("\n".join(text).rstrip() + "\n", encoding="utf-8")
                found = True
                break

            if not found:
                print(f"CRN {crn} not found in {courses_dir}; no file updated.")
                return False

        # Memory update only
        self.assigned_courses.append(crn_str)
        print(f"Course {crn} assigned to Professor {self.full_name}.")
        return True

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
