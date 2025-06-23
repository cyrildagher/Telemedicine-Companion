def extract_entities(text: str) -> list:
    import spacy
    nlp = spacy.load("en_core_sci_sm")
    # Add the UMLS EntityLinker if not already present
    if not nlp.has_pipe("scispacy_linker"):
        import scispacy
        from scispacy.umls_linking import UmlsEntityLinker
        linker = UmlsEntityLinker(resolve_abbreviations=True, name="umls")
        nlp.add_pipe(linker)
    else:
        linker = nlp.get_pipe("scispacy_linker")
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        # Get UMLS concepts and semantic types
        umls_ents = ent._.umls_ents
        if umls_ents:
            # Take the top candidate
            concept_id, score = umls_ents[0]
            concept = linker.umls.cui_to_entity[concept_id]
            semantic_types = concept.types  # List of semantic type codes
            entities.append({
                "text": ent.text,
                "semantic_types": semantic_types,
                "umls_cui": concept_id,
                "canonical_name": concept.canonical_name
            })
        else:
            entities.append({
                "text": ent.text,
                "semantic_types": [],
                "umls_cui": None,
                "canonical_name": None
            })
    return entities


def categorize_entities(entities: list) -> dict:
    # UMLS semantic type codes for each category
    SYMPTOM_TYPES = {"T184"}  # Sign or Symptom
    MEDICATION_TYPES = {"T121", "T200"}  # Pharmacologic Substance, Clinical Drug
    PROCEDURE_TYPES = {"T061"}  # Therapeutic or Preventive Procedure
    DIAGNOSIS_TYPES = {"T047"}  # Disease or Syndrome

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
        text = ent["text"]
        types = set(ent["semantic_types"])
        token = text.lower()

        if SYMPTOM_TYPES & types:
            categorized["symptoms"].append(text)
        elif MEDICATION_TYPES & types:
            categorized["medications"].append(text)
        elif PROCEDURE_TYPES & types:
            categorized["procedures"].append(text)
        elif DIAGNOSIS_TYPES & types:
            categorized["diagnosis"].append(text)
        # Instructions: still use keywords (no good UMLS type)
        elif any(inst in token for inst in ["rest", "follow up", "monitoring", "advised", "hydrated", "take", "prescribed"]):
            categorized["instructions"].append(text)
        elif "year-old" in token:
            categorized["patient_info"]["age"] = token
        elif "female" in token or "male" in token:
            categorized["patient_info"]["gender"] = token
        else:
            categorized["other"].append(text)

    return categorized