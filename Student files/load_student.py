from Student import Student

def load_student(user_id, database="../Database/Accounts.txt"):
    with open(database, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = [p.strip().strip('"') for p in line.split(",")]
            if parts[0] == "STUDENT" and parts[1] == user_id:
                return Student(
                    student_num=parts[1],
                    full_name=parts[2],
                    classification=parts[3],
                    major=parts[4],
                    fiscal_clearance=parts[5]
                )
    return None
