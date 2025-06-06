from fastapi import APIRouter, Body, HTTPException
import os
import yaml
from datetime import date

router = APIRouter()
HABIT_PATH = os.getenv("HABIT_PATH", "/home/cody/avrana/filing_cabinet/habits")

@router.post("/habits/today")
def log_habits(entry: dict = Body(...)):
    today = date.today().isoformat()
    filename = f"{today}.yaml"
    filepath = os.path.join(HABIT_PATH, filename)

    try:
        with open(filepath, "w") as f:
            yaml.dump(entry, f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Habit log saved", "file": filename}
