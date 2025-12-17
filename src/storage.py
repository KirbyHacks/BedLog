import json
from pathlib import Path

DB_PATH = Path("data.json")

def load_db():
    if not DB_PATH.exists():
        return {}
    return json.loads(DB_PATH.read_text(encoding="utf-8"))

def save_db(data: dict):
    DB_PATH.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
