from fastapi import APIRouter, HTTPException, Body
from datetime import datetime
import os
import yaml

router = APIRouter()

JOURNAL_PATH = os.getenv("JOURNAL_PATH", "/home/cody/avrana/filing_cabinet/journals")

@router.post("/journal")
def post_journal_entry(entry: dict = Body(...)):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}.yaml"
    filepath = os.path.join(JOURNAL_PATH, filename)

    try:
        with open(filepath, "w") as f:
            yaml.dump(entry, f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save journal entry: {e}")

    return {"message": "Journal entry saved.", "file": filename}
