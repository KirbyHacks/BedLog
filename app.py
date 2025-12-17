from fastapi import FastAPI, HTTPException
from src.main import (
    get_latest_md,
    get_version_md,
    update_cache,
    check_update
)

app = FastAPI(title="BedLog", version="0.2.0")


@app.get("/latest")
def latest():
    return get_latest_md()


@app.get("/version")
def version(version: str):
    result = get_version_md(version)
    if not result:
        raise HTTPException(404, "Version not found")
    return result["md"]


@app.get("/update")
def update():
    return update_cache()


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/check")
def check():
    return check_update()
