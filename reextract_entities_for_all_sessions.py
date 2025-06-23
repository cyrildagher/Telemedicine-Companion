#!/usr/bin/env python3
"""
Re-extract medical entities for all sessions in the database using the improved extraction logic,
and update the consultations table accordingly.
"""

from src.db_reader import get_session_ids, get_consultation_transcript
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
        # Extract and categorize entities
        entities = extract_entities(transcript)
        structured_data = categorize_entities(entities)
        # Optionally, set patient info from DB if available
        # (Otherwise, it will be None or overwritten by extraction)
        update_structured_data(session_id, structured_data)
        print(f"  ✅ Updated structured data for session {session_id}")
    print("\nAll sessions updated with improved entity extraction!")

if __name__ == "__main__":
    main() 