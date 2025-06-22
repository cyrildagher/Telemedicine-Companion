import json

def save_transcript(text: str, output_path: str):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

def save_entities_to_json(data: dict, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)