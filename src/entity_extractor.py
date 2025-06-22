def extract_entities(text: str) -> list:
    import spacy
    nlp = spacy.load("en_core_sci_sm")
    doc = nlp(text)
    return [ent.text for ent in doc.ents]


def categorize_entities(entities: list) -> dict:
    categorized = {
        "patient_info": {"age": None, "gender": None},
        "symptoms": [],
        "medications": [],
        "procedures": [],
        "instructions": [],
        "diagnosis": [],
        "other": []
    }

    for ent in entities:
        token = ent.lower()

        if any(sym in token for sym in ["fever", "cough", "pain", "fatigue", "discomfort", "shortness"]):
            categorized["symptoms"].append(ent)
        elif any(med in token for med in ["azithromycin", "methotrexate", "milligram", "paracetamol"]):
            categorized["medications"].append(ent)
        elif "x-ray" in token or "test" in token or "scan" in token:
            categorized["procedures"].append(ent)
        elif any(inst in token for inst in ["rest", "follow up", "monitoring", "advised"]):
            categorized["instructions"].append(ent)
        elif "rheumatoid arthritis" in token or "diagnosis" in token:
            categorized["diagnosis"].append(ent)
        elif "year-old" in token:
            categorized["patient_info"]["age"] = token
        elif "female" in token or "male" in token:
            categorized["patient_info"]["gender"] = token
        else:
            categorized["other"].append(ent)

    return categorized