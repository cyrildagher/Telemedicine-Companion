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