#!/usr/bin/env python3
"""
Re-extract medical entities for all sessions in the database using the improved extraction logic,
and update the consultations table accordingly.
"""

from src.db_reader import get_session_ids, get_consultation_transcript, get_consultation_by_session
from src.entity_extractor import extract_entities, categorize_entities
import mysql.connector
import json

# DB connection settings (should match your project)
DB_CONFIG = dict(
    host="localhost",
    user="root",
    password="cyril01",
    database="telemed_db",
    auth_plugin="mysql_native_password"
)

def update_structured_data(session_id, structured_data):
    """Update the structured_data fields in the consultations table for a session."""
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    query = """
        UPDATE consultations SET
            patient_age = %s,
            patient_gender = %s,
            symptoms = %s,
            medications = %s,
            procedures = %s,
            instructions = %s,
            diagnosis = %s
        WHERE session_id = %s
    """
    values = (
        structured_data["patient_info"]["age"],
        structured_data["patient_info"]["gender"],
        json.dumps(structured_data.get("symptoms", [])),
        json.dumps(structured_data.get("medications", [])),
        json.dumps(structured_data.get("procedures", [])),
        json.dumps(structured_data.get("instructions", [])),
        json.dumps(structured_data.get("diagnosis", [])),
        session_id
    )
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()

def main():
    session_ids = get_session_ids()
    print(f"Found {len(session_ids)} sessions in the database.")
    for session_id in session_ids:
        print(f"\nProcessing session: {session_id}")
        transcript = get_consultation_transcript(session_id)
        if not transcript or "not available" in transcript.lower():
            print(f"  ⚠️ No transcript found for session {session_id}, skipping.")
            continue

        # Get existing data to preserve patient info
        existing_consultation = get_consultation_by_session(session_id)
        existing_patient_info = {}
        if existing_consultation and "patient_info" in existing_consultation.get("structured_data", {}):
            existing_patient_info = existing_consultation["structured_data"]["patient_info"]

        # Extract and categorize entities from the transcript
        entities = extract_entities(transcript)
        structured_data = categorize_entities(entities)

        # Preserve existing age/gender if new extraction didn't find them
        if not structured_data["patient_info"].get("age") and existing_patient_info.get("age"):
            structured_data["patient_info"]["age"] = existing_patient_info["age"]
            print(f"  -> Preserving existing age: {existing_patient_info['age']}")
        
        if not structured_data["patient_info"].get("gender") and existing_patient_info.get("gender"):
            structured_data["patient_info"]["gender"] = existing_patient_info["gender"]
            print(f"  -> Preserving existing gender: {existing_patient_info['gender']}")

        # Update the database with the new, combined data
        update_structured_data(session_id, structured_data)
        print(f"  ✅ Updated structured data for session {session_id}")
    print("\nAll sessions updated with improved entity extraction!")

if __name__ == "__main__":
    main() 