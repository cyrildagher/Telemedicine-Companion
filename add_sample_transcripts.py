#!/usr/bin/env python3
"""
Script to add sample transcripts to the database for testing the telemedicine dashboard
"""

from src.db_writer import store_transcript
from src.db_reader import get_session_ids

def add_sample_transcripts():
    """Add sample transcripts for existing sessions"""
    
    # Sample transcript text
    sample_transcript = """Doctor: Good morning, how are you feeling today?

Patient: I've been having this persistent dry cough for about a week now, and some chest discomfort.

Doctor: I see. Any fever or other symptoms?

Patient: No fever, but I do feel a bit short of breath sometimes, especially when I'm active.

Doctor: Have you been taking any medications for this?

Patient: No, I haven't taken anything yet. I wanted to see you first.

Doctor: That's good. Let me listen to your chest and check your oxygen levels.

[Physical examination performed]

Doctor: Your oxygen saturation is good at 98%. I can hear some mild congestion in your chest. I'd like to order a chest x-ray to rule out any underlying issues.

Patient: That sounds good. What about treatment?

Doctor: I'll prescribe azithromycin 500mg once daily for 5 days. Also, make sure to get plenty of rest and stay hydrated. Follow up with me in a week if your symptoms don't improve or if they get worse.

Patient: Thank you, doctor. I'll make sure to take the medication as prescribed.

Doctor: You're welcome. Take care and get well soon."""

    # Get existing session IDs
    session_ids = get_session_ids()
    
    if not session_ids:
        print("❌ No sessions found in database. Please add consultation data first.")
        return False
    
    print(f"📋 Found {len(session_ids)} sessions in database")
    
    # Add sample transcript for each session
    for session_id in session_ids:
        try:
            # Create a slightly modified transcript for each session
            session_transcript = f"Session {session_id} - {sample_transcript}"
            
            store_transcript(session_id, session_transcript)
            print(f"✅ Added transcript for session: {session_id}")
            
        except Exception as e:
            print(f"❌ Error adding transcript for {session_id}: {e}")
    
    print("\n🎉 Sample transcripts added successfully!")
    print("You can now run the dashboard and transcripts should load properly.")
    return True

if __name__ == "__main__":
    print("📝 Adding Sample Transcripts to Database...")
    print("=" * 50)
    add_sample_transcripts() 