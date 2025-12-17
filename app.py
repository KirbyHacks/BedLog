from fastapi import FastAPI
import cloudscraper
from src.main import get_recent, get_latest_md

app = FastAPI(
    title="BedLog",
    version="0.1.0"
)

@app.get("/latest")
def latest():
    return {"result": get_latest_md()}

@app.get("/history")
def history():
    return get_recent()

@app.get("/health")
def health():
    return {"status": "ok"}
