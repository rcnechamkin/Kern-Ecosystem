from fastapi import APIRouter, Body, HTTPException
import os
import yaml
from datetime import date

router = APIRouter()
ACTIVITY_PATH = os.getenv("ACTIVITY_PATH", "/home/cody/avrana/filing_cabinet/activity")

@router.post("/activity/log")
def log_activity(entry: dict = Body(...)):
    today = date.today().isoformat()
    filename = f"{today}.yaml"
    filepath = os.path.join(ACTIVITY_PATH, filename)

    try:
        with open(filepath, "w") as f:
            yaml.dump(entry, f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Activity log saved", "file": filename}
