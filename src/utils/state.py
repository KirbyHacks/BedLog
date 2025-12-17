import json
from pathlib import Path

STATE_FILE = Path("data/state.json")

def load_state():
    if not STATE_FILE.exists():
        return {"latest_version": None}

    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_state(version: str):
    STATE_FILE.parent.mkdir(exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"latest_version": version}, f)
