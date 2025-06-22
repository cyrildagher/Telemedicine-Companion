from src.transcriber import transcribe_audio
from src.entity_extractor import extract_entities, categorize_entities
from src.utils import save_transcript, save_entities_to_json
from src.db_writer import store_consultation

AUDIO_PATH = "audio_samples/consultation1.wav"
TRANSCRIPT_PATH = "transcripts/sample_transcript.txt"
ENTITY_JSON_PATH = "transcripts/entities_structured.json"

# Transcribe
text = transcribe_audio(AUDIO_PATH)
print("\n--- Transcript ---\n", text)

# Save transcript
save_transcript(text, TRANSCRIPT_PATH)

# Extract and categorize entities
entities = extract_entities(text)
categorized = categorize_entities(entities)

# Print categorized results (optional)
import json
print("\n--- Categorized Entities ---")
print(json.dumps(categorized, indent=2))

# Save categorized entities to JSON
save_entities_to_json(categorized, ENTITY_JSON_PATH)

# Store in database
store_consultation(categorized, session_id="consult_002")