import sys
from pathlib import Path

admin_folder = Path(__file__).parent
sys.path.insert(0, str(admin_folder))

from Admin import Admin

from pathlib import Path

def load_admin(user_id, database=None):
    if database is None:
        base_folder = Path(__file__).parent.parent
        database = base_folder / "Database" / "Accounts.txt"

    with open(database, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = [p.strip().strip('"') for p in line.split(",")]

            if parts[0] == "ADMIN" and parts[1] == user_id:
                return Admin(
                    admin_num=parts[1],
                    full_name=parts[2]
                )

    return None
