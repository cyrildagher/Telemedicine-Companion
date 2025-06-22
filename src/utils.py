def save_transcript(text: str, output_path: str):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)