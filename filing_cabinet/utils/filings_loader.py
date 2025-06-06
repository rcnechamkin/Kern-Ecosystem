import os
import yaml

def load_yaml_files_from_folder(folder_path):
    memory_data = []

    if not os.path.exists(folder_path):
        print(f"[FilingLoader] Folder not found: {folder_path}")
        return memory_data

    for filename in os.listdir(folder_path):
        if filename.endswith((".yaml", ".yml")):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                try:
                    data = yaml.safe_load(file)
                    memory_data.append(data)
                except yaml.YAMLError as e:
                    print(f"[FilingLoader] YAML error in {filename}: {e}")

    return memory_data
