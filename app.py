from fastapi import FastAPI
import cloudscraper
from src.main import get_recent

app = FastAPI(
    title="BedLog",
    version="0.1.0"
)

@app.get("/latest")
def latest():
    return "Sigma"

@app.get("/history")
def history():
    return get_recent()

@app.get("/health")
def health():
    return {"status": "ok"}
