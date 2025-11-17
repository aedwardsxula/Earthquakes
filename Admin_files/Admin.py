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
