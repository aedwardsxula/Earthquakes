import sys
from pathlib import Path

# Ensure the folder containing this module is on sys.path so local imports (Professor)
# resolve correctly when this file is executed via dynamic import.
professor_folder = Path(__file__).parent
sys.path.insert(0, str(professor_folder))

from Professor import Professor

def load_professor(user_id, database=None):
    if database is None:
        base_folder = Path(__file__).parent.parent
        database = base_folder / "Database" / "Accounts.txt"

    with open(database, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = [p.strip().strip('"') for p in line.split(",")]

            # Accept either 'PROF' or 'PROFESSOR' as the account type in Accounts.txt
            if parts and parts[0].upper() in ("PROF", "PROFESSOR") and len(parts) > 1 and parts[1] == user_id:
                # Format: PROFESSOR,professor_id,full_name,department,courses
                # courses are separated by ';'
                department = parts[3] if len(parts) > 3 else ""
                assigned_courses = []
                if len(parts) > 4 and parts[4]:
                    assigned_courses = parts[4].split(';')
                
                return Professor(
                    professor_id=parts[1],
                    full_name=parts[2],
                    department=department,
                    assigned_courses=assigned_courses
                )

    return None