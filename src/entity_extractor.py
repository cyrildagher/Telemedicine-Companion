def extract_entities(text: str) -> list:
    import spacy
    nlp = spacy.load("en_core_sci_sm")
    doc = nlp(text)
    return [ent.text for ent in doc.ents]