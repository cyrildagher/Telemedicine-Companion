import mysql.connector
import json
from datetime import datetime

def get_db_connection():
    """Create and return a database connection"""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="cyril01",
        database="telemed_db",
        auth_plugin="mysql_native_password"
    )

def get_session_ids():
    """Fetch all distinct session_ids from the consultations table"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        query = "SELECT DISTINCT session_id FROM consultations ORDER BY session_id"
        cursor.execute(query)
        
        session_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.close()
        connection.close()
        
        return session_ids
    except Exception as e:
        print(f"Error fetching session IDs: {e}")
        return []

def get_consultation_by_session(session_id):
    """Fetch consultation data for a specific session_id"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        query = """
            SELECT 
                session_id,
                timestamp,
                patient_age,
                patient_gender,
                symptoms,
                medications,
                procedures,
                instructions,
                diagnosis
            FROM consultations 
            WHERE session_id = %s
            ORDER BY timestamp DESC
            LIMIT 1
        """
        
        cursor.execute(query, (session_id,))
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if result:
            # Convert JSON strings back to lists
            structured_data = {
                "patient_info": {
                    "age": result["patient_age"],
                    "gender": result["patient_gender"]
                },
                "symptoms": json.loads(result["symptoms"]) if result["symptoms"] else [],
                "medications": json.loads(result["medications"]) if result["medications"] else [],
                "procedures": json.loads(result["procedures"]) if result["procedures"] else [],
                "instructions": json.loads(result["instructions"]) if result["instructions"] else [],
                "diagnosis": json.loads(result["diagnosis"]) if result["diagnosis"] else [],
                "other": []
            }
            
            return {
                "session_id": result["session_id"],
                "timestamp": result["timestamp"],
                "structured_data": structured_data
            }
        
        return None
        
    except Exception as e:
        print(f"Error fetching consultation data: {e}")
        return None

def get_consultation_transcript(session_id):
    """Fetch transcript for a specific session_id (if stored separately)"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Check if there's a transcripts table
        query = "SELECT transcript FROM transcripts WHERE session_id = %s"
        cursor.execute(query, (session_id,))
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if result:
            return result[0]
        
        # If no transcript table, return a placeholder
        return f"Transcript for session {session_id} - [Transcript data not available in database]"
        
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return f"Transcript for session {session_id} - [Error loading transcript]"

def get_session_summary(session_id):
    """Get a summary of the session including patient info and entity counts"""
    try:
        consultation = get_consultation_by_session(session_id)
        if consultation:
            data = consultation["structured_data"]
            return {
                "session_id": session_id,
                "timestamp": consultation["timestamp"],
                "patient_age": data["patient_info"]["age"],
                "patient_gender": data["patient_info"]["gender"],
                "symptoms_count": len(data["symptoms"]),
                "medications_count": len(data["medications"]),
                "procedures_count": len(data["procedures"]),
                "diagnosis_count": len(data["diagnosis"])
            }
        return None
    except Exception as e:
        print(f"Error getting session summary: {e}")
        return None 