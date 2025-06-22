import json

data = {
    "patient_info": {"age": "45", "gender": "female"},
    "symptoms": ["fatigue", "joint pain", "low-grade fever"],
    "medications": ["methotrexate"],
    "procedures": ["chest x-ray", "laboratory tests"],
    "instructions": ["follow up in two weeks", "monitoring"],
    "diagnosis": ["early-stage rheumatoid arthritis"]
}

with open("transcripts/entities_structured.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)