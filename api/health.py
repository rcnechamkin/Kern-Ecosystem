from fastapi import FastAPI, Request, Query
from fastapi.responses import PlainTextResponse
from datetime import datetime
import json
import subprocess
from pathlib import Path

app = FastAPI()

# Paths
SAVE_DIR = Path.home() / "avrana" / "filing_cabinet" / "health" / "raw_exports"
LOG_PATH = Path.home() / "avrana" / "logs" / "health_requests.log"
SECRET_KEY = "letmein"  # Change if needed

SAVE_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def log_request(request: Request, filename: str):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "client_ip": request.client.host,
        "method": request.method,
        "path": str(request.url.path),
        "saved_file": filename,
    }
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

@app.post("/api/health")
async def receive_health_data(request: Request):
    data = await request.json()
    date_str = datetime.now().strftime("HealthAutoExport_%Y-%m-%d_%H-%M.json")
    filepath = SAVE_DIR / date_str

    # Save raw export
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    log_request(request, str(filepath))

    # Try parsing it
    try:
        subprocess.run(
            ["python3", "-m", "filing_cabinet.health.parse_health_export"],
            cwd=Path.home() / "avrana",
            check=True
        )
        return {"status": "success", "file_saved": str(filepath), "parsed": True}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "file_saved": str(filepath), "error": str(e)}

@app.get("/logs")
async def view_logs(key: str = Query("")):
    if key != SECRET_KEY:
        return {"error": "unauthorized"}
    if not LOG_PATH.exists():
        return PlainTextResponse("No logs yet.")
    with open(LOG_PATH, "r") as f:
        return PlainTextResponse(f.read(), media_type="text/plain")
