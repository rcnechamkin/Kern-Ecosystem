from pathlib import Path
import subprocess
import time

RAW_DIR = Path.home() / "avrana" / "filing_cabinet" / "health" / "raw_exports"
PROCESSED_FILE = Path.home() / ".last_health_export.txt"

def get_latest_file():
    files = list(RAW_DIR.glob("HealthAutoExport_*.json"))
    return max(files, key=lambda f: f.stat().st_mtime, default=None)

def already_processed(f):
    return PROCESSED_FILE.read_text().strip() == str(f) if PROCESSED_FILE.exists() else False

def update_processed(f):
    PROCESSED_FILE.write_text(str(f))

def run_parser():
    subprocess.run([
        "python3", "-m", "filing_cabinet.health.parse_health_export"
    ])

def main():
    latest = get_latest_file()
    if latest and not already_processed(latest):
        print(f"New file found: {latest.name}")
        run_parser()
        update_processed(latest)
    else:
        print("No new health export to process.")

if __name__ == "__main__":
    main()
