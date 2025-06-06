from fastapi import APIRouter, HTTPException
from datetime import date, timedelta
import os
import yaml

router = APIRouter()

SCHEDULE_PATH = os.getenv("SCHEDULE_PATH", "/home/cody/avrana/filing_cabinet/schedule")

@router.get("/schedule/week")
def get_week_schedule():
    today = date.today()
    filenames = [(today + timedelta(days=i)).isoformat() + ".yaml" for i in range(7)]
    schedules = []

    for name in filenames:
        filepath = os.path.join(SCHEDULE_PATH, name)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                data = yaml.safe_load(f)
                schedules.append({"date": name[:-5], "schedule": data})
        else:
            schedules.append({"date": name[:-5], "schedule": None})

    return {"week_schedule": schedules}
