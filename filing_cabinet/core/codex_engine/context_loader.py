import yaml
from pathlib import Path

# === Load codex.yaml and return structured modules ===
def load_codex(codex_path: Path = Path("filing_cabinet/core/codex.yaml")) -> dict:
    with codex_path.open("r", encoding="utf-8") as file:
        codex_data = yaml.safe_load(file)
    return codex_data

# === Load all referenced module files ===
def load_context_modules(codex: dict) -> dict:
    modules = codex.get("modules", {})
    loaded_modules = {}

    for key, module_info in modules.items():
        file_path = Path(module_info["file"])
        if not file_path.exists():
            print(f"[Codex] Warning: File not found for module '{key}': {file_path}")
            continue

        try:
            if file_path.suffix == ".yaml":
                with file_path.open("r", encoding="utf-8") as f:
                    loaded_modules[key] = yaml.safe_load(f)
            elif file_path.suffix in {".md", ".txt"}:
                with file_path.open("r", encoding="utf-8") as f:
                    loaded_modules[key] = f.read()
            else:
                print(f"[Codex] Unsupported file type for module '{key}': {file_path.suffix}")
        except Exception as e:
            print(f"[Codex] Failed to load module '{key}': {e}")

    return loaded_modules

# === Combined loader for convenience ===
def get_codex_context(codex_path: Path = Path("filing_cabinet/core/codex.yaml")) -> dict:
    codex = load_codex(codex_path)
    return load_context_modules(codex)
