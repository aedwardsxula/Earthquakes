import random 

class Course: 
    crns_dict = {}
    def __init__(self, course_name, time, class_list):
        self.course_name = course_name
        CRN = random.randint(10000, 99999)
        self.CRN = CRN
        if self.CRN not in Course.crns_dict:
            Course.crns_dict[self.CRN] = self
        else:
            while self.CRN in Course.crns_dict.keys():
                CRN = random.randint(10000, 99999)
            Course.crns_dict[self.CRN] = Course(course_name, time, class_list)
        self.time = time
        self.class_list = class_list

    def print_course_details(self):
        print(f"Course Name: {self.course_name}")
        print(f"Course ID: {self.course_id}")
        print(f"Time: {self.time}")
        print("Class List:")
        for student in self.class_list:
            print(f"- {student}")
    
    def access_course(self, CRN):
        if CRN in Course.crns_dict.keys():
            return Course.crns_dict[CRN]
        else:
            return "Not a valid CRN."
    
    def change_time(self, new_time):
        self.time = new_time
    
    def access_crns(self):
        for crn in Course.crns_dict.keys():
            print(crn)
            
    def access_course_crn(self, find_course_name):
        for crn, course in Course.crns_dict.items():
            if course.course_name == find_course_name:
                return crn
        return "Course name not found, can not retrieve CRN."

    def change_course_name(self, new_name):
        self.course_name = new_name
    
    
