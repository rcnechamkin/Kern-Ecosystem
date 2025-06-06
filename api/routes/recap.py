from fastapi import APIRouter, HTTPException
import os
import yaml
from pathlib import Path

router = APIRouter()

RECAP_PATH = os.getenv("RECAP_PATH", "/home/cody/avrana/filing_cabinet/blackbox")

@router.get("/recap/latest")
def get_latest_recap():
    recap_dir = Path(RECAP_PATH)
    if not recap_dir.exists():
        raise HTTPException(status_code=404, detail="Recap directory not found.")

    recap_files = sorted(recap_dir.glob("*.yaml"), reverse=True)
    if not recap_files:
        raise HTTPException(status_code=404, detail="No recap files found.")

    latest_file = recap_files[0]
    with open(latest_file, "r") as f:
        data = yaml.safe_load(f)

    return {"filename": latest_file.name, "recap": data}
