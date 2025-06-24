import os
from fastapi import APIRouter, Request, Query
from fastapi.responses import PlainTextResponse

router = APIRouter()
LOG_PATH = os.path.expanduser("~/avrana/logs/health_requests.log")
SECRET_KEY = "SDCC2001rules"  # Change this to something secret

@router.get("/logs")
async def view_health_logs(key: str = Query("")):
    if key != SECRET_KEY:
        return {"error": "unauthorized"}

    if not os.path.exists(LOG_PATH):
        return PlainTextResponse("No logs yet.")

    with open(LOG_PATH, "r") as f:
        content = f.read()

    return PlainTextResponse(content, media_type="text/plain")
