import fileinput
import os

# 🧠 Rewrite targets: old → new import paths
rewrite_map = {
    "filing_cabinet.utils": "filing_cabinet.utils",
    "filing_cabinet.journals": "filing_cabinet.journals",
    "filing_cabinet.journals": "filing_cabinet.journals",
    "filing_cabinet.journals": "filing_cabinet.journals",
    "filing_cabinet.media": "filing_cabinet.media"
}

# 🔍 Walk through all .py files recursively
for root, _, files in os.walk("."):
    for name in files:
        if name.endswith(".py"):
            path = os.path.join(root, name)
            try:
                with fileinput.FileInput(path, inplace=True, encoding="utf-8") as file:
                    for line in file:
                        for old, new in rewrite_map.items():
                            line = line.replace(old, new)
                        print(line, end="")
            except UnicodeDecodeError:
                print(f"⚠️ Skipping non-UTF-8 file: {path}")
