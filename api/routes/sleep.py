from fastapi import APIRouter, Body, HTTPException
import os
import yaml
from datetime import date

router = APIRouter()
SLEEP_PATH = os.getenv("SLEEP_PATH", "/home/cody/avrana/filing_cabinet/activity")

@router.post("/sleep/today")
def log_sleep(entry: dict = Body(...)):
    today = date.today().isoformat()
    filename = f"{today}_sleep.yaml"
    filepath = os.path.join(SLEEP_PATH, filename)

    try:
        with open(filepath, "w") as f:
            yaml.dump(entry, f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Sleep log saved", "file": filename}
