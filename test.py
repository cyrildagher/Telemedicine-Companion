from src.transcriber import transcribe_audio
from src.entity_extractor import extract_entities
from src.utils import save_transcript

AUDIO_PATH = "audio_samples/consultation1.wav"
TRANSCRIPT_PATH = "transcripts/sample_transcript.txt"

text = transcribe_audio(AUDIO_PATH)
print("\n--- Transcript ---\n", text)

save_transcript(text, TRANSCRIPT_PATH)

entities = extract_entities(text)
print("\n--- Extracted Entities ---")
for e in entities:
    print(e)