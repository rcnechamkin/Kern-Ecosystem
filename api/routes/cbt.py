from fastapi import APIRouter, Body, HTTPException
import os
import yaml
from datetime import datetime

router = APIRouter()
CBT_PATH = os.getenv("CBT_PATH", "/home/cody/avrana/filing_cabinet/cbt")

@router.post("/cbt/log")
def log_cbt(entry: dict = Body(...)):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}-cbt.yaml"
    filepath = os.path.join(CBT_PATH, filename)

    try:
        with open(filepath, "w") as f:
            yaml.dump(entry, f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "CBT log saved", "file": filename}
