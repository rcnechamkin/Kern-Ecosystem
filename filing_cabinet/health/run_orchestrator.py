import os
import yaml
from pathlib import Path
from datetime import datetime
from parsers.apple_workouts import parse_apple_workouts

RUNS_DIR = Path(__file__).parent / "runs"
RUNS_DIR.mkdir(exist_ok=True)

def save_yaml(path, data):
    class NoAliasDumper(yaml.SafeDumper):
        def ignore_aliases(self, data):
            return True

    with open(path, "w") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, Dumper=NoAliasDumper)

def run_orchestrator(filepath):
    if not Path(filepath).exists():
        return {"error": f"File not found: {filepath}"}

    try:
        import json
        with open(filepath, "r") as f:
            data = json.load(f)
    except Exception as e:
        return {"error": f"Failed to load JSON: {e}"}

    result = parse_apple_workouts(data)
    if not result:
        return {"note": "No valid run data found in file."}

    run_date = result.get("date", datetime.now().strftime("%Y-%m-%d"))
    filename = f"Run_{run_date}.yaml"
    result["tags"] = ["run", "fitness"]

    save_path = RUNS_DIR / filename
    save_yaml(save_path, {"run": result})

    return {"saved": str(save_path), "summary": result}
