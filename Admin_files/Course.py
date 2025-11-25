import random
import csv
import os
from pathlib import Path


class Course: 
    crns_list = []
    # registry mapping CRN (string) -> Course instance
    courses_by_crn = {}
    def __init__(self, course_name, time, credits, class_list):
        self.course_name = course_name
        CRN = random.randint(10000, 99999)
        if CRN not in Course.crns_list:
            Course.crns_list.append(CRN)
            self.CRN = CRN
        else:
            while CRN in Course.crns_list:
                CRN = random.randint(10000, 99999)
            Course.crns_list.append(CRN)
            self.CRN = CRN
        # register this instance for class-level operations
        Course.courses_by_crn[str(self.CRN)] = self
        self.time = time
        self.credits = credits
        self.class_list = class_list
    
    @classmethod
    def save_all_courses_to_csv(cls, csv_path):
        fieldnames = ['crn', 'course_name', 'time', 'credits', 'class_list']

        with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for course in cls.courses_by_crn.values():
                writer.writerow({
                    "crn": course.CRN,
                    "course_name": course.course_name,
                    "time": course.time,
                    "credits": course.credits,
                    "class_list": ";".join(course.class_list),
                })

    def print_course_details(self):
        print(f"Course Name: {self.course_name}")
        print(f"Course CRN: {self.CRN}")
        print(f"Credits: {self.credits}")
        print(f"Time: {self.time}")
        print("Class List:")
        for student in self.class_list:
            print(f"- {student}")

    def display_crn_desc(self, csv_path):
        crns = []

        with open(csv_path, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                if "crn" in row and row["crn"].isdigit():
                    crns.append(int(row["crn"]))

        crns.sort(reverse=True)

        for i in range(1, len(crns) + 1):
            print(f"{i}. {crns[i -1]}")

    
    def change_time(self, new_time):
        self.time = new_time
    
    def access_crns(self):
        for crn in Course.crns_list:
            print(crn)
    
    @staticmethod        
    def access_course_crn(find_course_name, csv_path):
        with open(csv_path, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                if row["course_name"] == find_course_name:
                    return row["crn"]
        
        return "Course name not found, can not retrieve CRN."
    
    @staticmethod
    def access_course_course_name(crn, csv_path):
        with open(csv_path, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                if row["crn"] == crn:
                    return row["course_name"]
        
        return "CRN not found for the given course name."
    
    def change_course_name(self, new_name):
        self.course_name = new_name

    def add_course_to_database(self,csv_path):
        """
         csv_path should be `Database/Courses.csv`.
        """

        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        fieldnames = ['crn', 'course_name', 'time', 'class_list']

        class_list_str = ''
        if self.class_list:
            class_list_str = ';'.join(str(x) for x in self.class_list)

        row = {
            'crn': str(self.CRN),
            'course_name': self.course_name,
            'time': self.time if self.time is not None else '',
            'credits': str(self.credits) if self.credits is not None else '',
            'class_list': class_list_str,
        }
    @staticmethod
    def add_already_created_course_to_database(course_obj, csv_path):
        with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
            fieldnames = ["crn", "course_name", "time", "class_list"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writerow({
                "crn": course_obj.CRN,
                "course_name": course_obj.course_name,
                "time": course_obj.time,
                "credits": course_obj.credits,
                "class_list": ";".join(course_obj.class_list),
            })
    
    #Scheduling Functions
    def add_course_on_student_schedule(self, schedule_list, student_name):
        if student_name not in self.class_list:
            self.class_list.append(student_name)    
            schedule_list.append(self)
        else:
            print(f"Student {student_name} is already enrolled in this course.")
    
    def remove_course_from_student_schedule(self, student_name, schedule_list):
        if student_name in self.class_list:
            schedule_list.remove(self)
            self.class_list.remove(student_name)    
        else:
            print(f"Student {student_name} is not enrolled in this course.")
    
    def save_to_txt(self):
        base = Path(__file__).parent.parent
        folder = base / "Database" / "courses"
        folder.mkdir(parents=True, exist_ok=True)

        file_path = folder / f"{self.course_name}.txt"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"crn: {self.CRN}\n")
            f.write(f"credits: {self.credits}\n")
            f.write(f"course_name: {self.course_name}\n")
            f.write(f"time: {self.time}\n")
            f.write("professor: none\n\n")
            f.write("students:\n")
            for s in self.class_list:
                f.write(f"{s}\n")


    