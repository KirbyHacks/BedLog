import json
from pathlib import Path

CACHE_FILE = Path("cache.json")

def load_cache():
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text())
    return {}

def save_cache(data):
    CACHE_FILE.write_text(json.dumps(data, indent=2))
