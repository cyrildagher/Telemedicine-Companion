import mysql.connector
import json
from datetime import datetime

def store_consultation(data, session_id="consult_001"):
    connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="cyril01",
    database="telemed_db",
    auth_plugin="mysql_native_password"  # this is to explicitly tell the connector to use that plugin to asvoid the issue of not supporting the current module 
)

    cursor = connection.cursor()

    query = """
        INSERT INTO consultations (
            session_id, timestamp,
            patient_age, patient_gender,
            symptoms, medications, procedures, instructions, diagnosis
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        session_id,
        datetime.utcnow(),
        data["patient_info"]["age"],
        data["patient_info"]["gender"],
        json.dumps(data.get("symptoms", [])),
        json.dumps(data.get("medications", [])),
        json.dumps(data.get("procedures", [])),
        json.dumps(data.get("instructions", [])),
        json.dumps(data.get("diagnosis", [])),
    )

    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()

def store_transcript(session_id, transcript_text):
    """Store transcript text in the database"""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="cyril01",
        database="telemed_db",
        auth_plugin="mysql_native_password"
    )

    cursor = connection.cursor()

    # First, create transcripts table if it doesn't exist
    create_table_query = """
        CREATE TABLE IF NOT EXISTS transcripts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            session_id VARCHAR(50) NOT NULL,
            transcript TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY unique_session_transcript (session_id)
        )
    """
    cursor.execute(create_table_query)

    # Insert or update transcript
    query = """
        INSERT INTO transcripts (session_id, transcript) 
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE 
            transcript = VALUES(transcript),
            created_at = CURRENT_TIMESTAMP
    """

    values = (session_id, transcript_text)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()

def store_consultation_with_transcript(data, transcript_text, session_id="consult_001"):
    """Store both consultation data and transcript"""
    # Store consultation data
    store_consultation(data, session_id)
    
    # Store transcript
    store_transcript(session_id, transcript_text)