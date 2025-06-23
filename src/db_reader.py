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
        
        # First, try to check if there's a transcripts table
        cursor.execute("SHOW TABLES LIKE 'transcripts'")
        transcripts_table_exists = cursor.fetchone()
        
        if transcripts_table_exists:
            # If transcripts table exists, try to get transcript
            query = "SELECT transcript FROM transcripts WHERE session_id = %s"
            cursor.execute(query, (session_id,))
            result = cursor.fetchone()
            
            if result:
                cursor.close()
                connection.close()
                return result[0]
        
        cursor.close()
        connection.close()
        
        # If no transcript table or no transcript found, try to load from sample file
        try:
            with open("transcripts/sample_transcript.txt", "r") as f:
                sample_transcript = f.read()
            return f"Sample transcript for session {session_id}:\n\n{sample_transcript}"
        except FileNotFoundError:
            # If no sample file, return a placeholder transcript
            return f"""Consultation Transcript for Session {session_id}

[Transcript data not available in database]

This is a placeholder transcript for session {session_id}. 
In a real implementation, the actual consultation transcript would be stored here.

Patient consultation details have been extracted and are available in the medical entities section."""
        
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return f"""Consultation Transcript for Session {session_id}

[Error loading transcript: {str(e)}]

Please check the database connection and transcript storage configuration."""

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

def search_sessions_by_patient(patient_search):
    """Search sessions by patient information (age, gender, or session_id)"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Search in session_id, patient_age, or patient_gender
        query = """
            SELECT DISTINCT session_id, timestamp, patient_age, patient_gender
            FROM consultations 
            WHERE session_id LIKE %s 
               OR patient_age LIKE %s 
               OR patient_gender LIKE %s
            ORDER BY timestamp DESC
        """
        
        search_term = f"%{patient_search}%"
        cursor.execute(query, (search_term, search_term, search_term))
        results = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return results
        
    except Exception as e:
        print(f"Error searching sessions: {e}")
        return []

def get_all_session_summaries():
    """Get summaries of all sessions for search functionality"""
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
                diagnosis
            FROM consultations 
            ORDER BY timestamp DESC
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        summaries = []
        for result in results:
            # Count entities
            symptoms_count = len(json.loads(result["symptoms"])) if result["symptoms"] else 0
            medications_count = len(json.loads(result["medications"])) if result["medications"] else 0
            procedures_count = len(json.loads(result["procedures"])) if result["procedures"] else 0
            diagnosis_count = len(json.loads(result["diagnosis"])) if result["diagnosis"] else 0
            
            summaries.append({
                "session_id": result["session_id"],
                "timestamp": result["timestamp"],
                "patient_age": result["patient_age"],
                "patient_gender": result["patient_gender"],
                "symptoms_count": symptoms_count,
                "medications_count": medications_count,
                "procedures_count": procedures_count,
                "diagnosis_count": diagnosis_count
            })
        
        cursor.close()
        connection.close()
        
        return summaries
        
    except Exception as e:
        print(f"Error getting session summaries: {e}")
        return [] 