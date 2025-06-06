from fastapi import APIRouter, HTTPException
from datetime import date
import os
import yaml

router = APIRouter()

FILING_CABINET_PATH = os.getenv("FILING_CABINET_PATH", "/home/cody/avrana/filing_cabinet/moods")

@router.get("/moods/today")
def get_today_mood():
    today = date.today().isoformat()
    filename = f"{today}.yaml"
    filepath = os.path.join(FILING_CABINET_PATH, filename)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Mood log for today not found.")

    with open(filepath, "r") as f:
        data = yaml.safe_load(f)

    return {"date": today, "mood_log": data}
