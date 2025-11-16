
class Student:
    def __init__(self,student_num, full_name, classification, major, fiscal_clearance):
        self.student_num = student_num
        self.full_name = full_name
        self.classification = classification
        # normalize fiscal_clearance into a boolean
        if isinstance(fiscal_clearance, bool):
            fc = fiscal_clearance
        elif isinstance(fiscal_clearance, str):
            v = fiscal_clearance.strip().lower()
            fc = v in ('true', 't', 'yes', 'y', '1')
        else:
            try:
                fc = bool(int(fiscal_clearance))
            except Exception:
                fc = bool(fiscal_clearance)
        self.fiscal_clearance = fc
        self.major = major
    
    def display_info(self):
        print(f"Student Number: {self.student_num}")
        print(f"Name: {self.full_name}")
        print(f"Classification: {self.classification}")
        print(f"Fiscally Cleared: {'Yes' if self.fiscal_clearance else 'No'}")
        print(f"Major: {self.major}")
    
    def return_clearance_status(self):
        return bool(self.fiscal_clearance)
    
    def change_major(self, new_major):
        self.major = new_major  

    def change_clearance(self, new_status):
        if isinstance(new_status, bool):
            self.fiscal_clearance = new_status
        elif isinstance(new_status, str):
            v = new_status.strip().lower()
            self.fiscal_clearance = v in ('true', 't', 'yes', 'y', '1')
        else:
            try:
                self.fiscal_clearance = bool(int(new_status))
            except Exception:
                self.fiscal_clearance = bool(new_status)
    
    def update_name(self, new_full_name):
        self.full_name = new_full_name
    
    def update_classification(self, new_classification):
        self.classification = new_classification 

    def add_to_database(self, database):
        """
        Input should look like: student_object.add_to_database('Database/Accounts.txt')
        
        """

        def escape(field):
            s = str(field)
            if ',' in s or '"' in s or '\n' in s:
                s = s.replace('"', '""')
                return f'"{s}"'
            return s

        parts = ["STUDENT",self.student_num, self.full_name, self.classification, self.major, 'true' if self.fiscal_clearance else 'false']
        record = ','.join(escape(p) for p in parts)

        with open(database, 'a', encoding='utf-8') as f:
            f.write(record + '\n')

          
    

