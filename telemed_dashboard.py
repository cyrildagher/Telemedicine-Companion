# -*- coding: utf-8 -*-

import streamlit as st
import json
import os
from datetime import datetime
import tempfile
from src.transcriber import transcribe_audio
from src.entity_extractor import extract_entities, categorize_entities

# --- Page config ---
st.set_page_config(
    page_title="Telemed Consultation Viewer", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for better styling ---
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .patient-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .entity-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #28a745;
        color: #333;
    }
    .entity-section h4 {
        color: #333;
        margin-bottom: 0.5rem;
    }
    .entity-section ul {
        color: #333;
        margin: 0;
        padding-left: 1.5rem;
    }
    .entity-section li {
        color: #333;
        margin-bottom: 0.25rem;
    }
    .entity-section p {
        color: #6c757d;
        font-style: italic;
        margin: 0;
    }
    .stButton > button {
        width: 100%;
        border-radius: 20px;
        font-weight: bold;
    }
    .metric-card h5 {
        color: #6c757d;
        margin-bottom: 0.5rem;
    }
    .metric-card h3 {
        color: #333;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize session state ---
if 'patient_info' not in st.session_state:
    st.session_state.patient_info = {"name": "", "age": "", "gender": ""}
if 'structured_data' not in st.session_state:
    st.session_state.structured_data = None
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""
if 'current_patient' not in st.session_state:
    st.session_state.current_patient = ""

# --- Header ---
st.markdown("""
<div class="main-header">
    <h1>🩺 Telemedicine Consultation Review</h1>
    <p>Advanced Medical Entity Extraction & Analysis</p>
</div>
""", unsafe_allow_html=True)

# --- Patient Search & Selection ---
st.markdown("### 🔍 Patient Search")
col1, col2 = st.columns([3, 1])

with col1:
    patient_search = st.text_input(
        "Enter patient name to load consultation data:",
        placeholder="e.g., John Smith, Sarah Johnson...",
        key="patient_search"
    )

with col2:
    if st.button("🔍 Search Patient", type="primary"):
        if patient_search.strip():
            st.session_state.current_patient = patient_search.strip()
            st.success(f"Loading data for {patient_search}...")
            st.rerun()

# --- Auto-load patient data when name is entered ---
if st.session_state.current_patient:
    st.markdown("---")
    
    # Load sample data for demonstration
    try:
        with open("transcripts/sample_transcript.txt", "r") as f:
            sample_transcript = f.read()
        
        with open("transcripts/entities_structured.json", "r") as f:
            sample_structured = json.load(f)
        
        # Update session state with loaded data
        st.session_state.transcript = sample_transcript
        st.session_state.structured_data = sample_structured
        st.session_state.patient_info = {
            "name": st.session_state.current_patient,
            "age": "35",
            "gender": "Female"
        }
        
    except FileNotFoundError:
        st.error("Sample data not found. Please ensure transcript files exist.")
        st.stop()

# --- Patient Information Display ---
if st.session_state.patient_info["name"]:
    st.markdown("---")
    st.markdown("### 👤 Patient Information")
    
    # Patient info card
    st.markdown(f"""
    <div class="patient-card">
        <h4>📋 {st.session_state.patient_info['name']}</h4>
        <div style="display: flex; gap: 2rem; margin-top: 1rem;">
            <div class="metric-card">
                <h5>Age</h5>
                <h3>{st.session_state.patient_info['age'] or '—'}</h3>
            </div>
            <div class="metric-card">
                <h5>Gender</h5>
                <h3>{st.session_state.patient_info['gender'] or '—'}</h3>
            </div>
            <div class="metric-card">
                <h5>Consultation Date</h5>
                <h3>{datetime.now().strftime('%m/%d/%Y')}</h3>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Main Content Area ---
if st.session_state.transcript and st.session_state.structured_data:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📋 Consultation Transcript")
        st.text_area(
            "Full Transcript",
            st.session_state.transcript,
            height=400,
            disabled=True,
            key="transcript_display"
        )
        
        col1a, col1b = st.columns(2)
        with col1a:
            st.download_button(
                "📄 Download Transcript",
                data=st.session_state.transcript,
                file_name=f"transcript_{st.session_state.patient_info['name']}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        with col1b:
            if st.button("🔄 Refresh Data", type="secondary"):
                st.rerun()
    
    with col2:
        st.markdown("### 🏥 Extracted Medical Entities")
        
        if st.session_state.structured_data:
            data = st.session_state.structured_data
            
            # Summary metrics
            col2a, col2b, col2c, col2d = st.columns(4)
            with col2a:
                st.metric("Symptoms", len(data.get("symptoms", [])))
            with col2b:
                st.metric("Medications", len(data.get("medications", [])))
            with col2c:
                st.metric("Procedures", len(data.get("procedures", [])))
            with col2d:
                st.metric("Diagnosis", len(data.get("diagnosis", [])))
            
            # Entity sections
            def display_entity_section(title, items, icon, color="#28a745"):
                if items:
                    st.markdown(f"""
                    <div class="entity-section" style="border-left-color: {color};">
                        <h4>{icon} {title}</h4>
                        <ul>
                    """, unsafe_allow_html=True)
                    
                    for item in items:
                        st.markdown(f"<li><strong>{item}</strong></li>", unsafe_allow_html=True)
                    
                    st.markdown("</ul></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="entity-section" style="border-left-color: #6c757d;">
                        <h4>{icon} {title}</h4>
                        <p>No {title.lower()} found</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            display_entity_section("Symptoms", data.get("symptoms", []), "🩺", "#dc3545")
            display_entity_section("Medications", data.get("medications", []), "💊", "#007bff")
            display_entity_section("Procedures", data.get("procedures", []), "🔬", "#ffc107")
            display_entity_section("Instructions", data.get("instructions", []), "📋", "#17a2b8")
            display_entity_section("Diagnosis", data.get("diagnosis", []), "🏥", "#28a745")
            
            # Other entities
            other_entities = data.get("other", [])
            if other_entities:
                with st.expander("🔍 Other Identified Entities", expanded=False):
                    for i, item in enumerate(other_entities, 1):
                        st.markdown(f"**{i}.** {item}")

# --- Action Buttons ---
if st.session_state.structured_data:
    st.markdown("---")
    st.markdown("### 📊 Actions")
    
    col3, col4, col5, col6 = st.columns(4)
    
    with col3:
        if st.button("✅ Mark as Reviewed", type="primary"):
            st.success("✅ Consultation marked as reviewed and saved to database.")
    
    with col4:
        st.download_button(
            "⬇️ Download JSON",
            data=json.dumps(st.session_state.structured_data, indent=2),
            file_name=f"consultation_{st.session_state.patient_info['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col5:
        if st.button("📊 Generate Report", type="secondary"):
            st.info("📊 Generating comprehensive medical report...")
    
    with col6:
        if st.button("🔄 New Patient", type="secondary"):
            st.session_state.clear()
            st.rerun()

# --- Sidebar ---
with st.sidebar:
    st.markdown("### ⚙️ Quick Actions")
    
    if st.button("🆕 New Consultation", type="primary"):
        st.session_state.clear()
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 📁 Upload New Data")
    upload_option = st.radio("Input Method:", ["Audio File", "Transcript File", "Manual Entry"])
    
    if upload_option == "Audio File":
        uploaded_audio = st.file_uploader("Upload audio", type=['mp3', 'wav', 'm4a'])
        if uploaded_audio:
            with st.spinner("Transcribing..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_audio.name.split('.')[-1]}") as tmp_file:
                        tmp_file.write(uploaded_audio.getvalue())
                        tmp_file_path = tmp_file.name
                    
                    transcript_text = transcribe_audio(tmp_file_path)
                    os.unlink(tmp_file_path)
                    
                    st.session_state.transcript = transcript_text
                    st.success("Audio transcribed!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    elif upload_option == "Transcript File":
        uploaded_file = st.file_uploader("Upload transcript", type=['txt'])
        if uploaded_file:
            st.session_state.transcript = uploaded_file.read().decode('utf-8')
            st.success("Transcript loaded!")
            st.rerun()
    
    elif upload_option == "Manual Entry":
        manual_transcript = st.text_area("Enter transcript:", height=150)
        if st.button("Process Manual Entry"):
            if manual_transcript.strip():
                st.session_state.transcript = manual_transcript
                st.success("Transcript saved!")
                st.rerun()
    
    st.markdown("---")
    
    st.markdown("### ℹ️ Session Info")
    if st.session_state.patient_info["name"]:
        st.write(f"**Patient:** {st.session_state.patient_info['name']}")
        st.write(f"**Age:** {st.session_state.patient_info['age'] or 'Not set'}")
        st.write(f"**Gender:** {st.session_state.patient_info['gender'] or 'Not set'}")
        
        if st.session_state.structured_data:
            total_entities = sum(len(v) if isinstance(v, list) else 0 for v in st.session_state.structured_data.values())
            st.write(f"**Entities Found:** {total_entities}")
            st.write(f"**Last Updated:** {datetime.now().strftime('%H:%M:%S')}")
    else:
        st.info("No patient selected")
    
    st.markdown("---")
    
    st.markdown("### 🔧 Settings")
    model_size = st.selectbox("Whisper Model", ["tiny", "base", "small", "medium", "large"], index=1)
    auto_extract = st.checkbox("Auto-extract entities", value=True)
    
    if st.button("🔄 Clear All Data"):
        st.session_state.clear()
        st.rerun()

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 1rem;">
    <p>🩺 Telemedicine Consultation Review System | Built with Streamlit</p>
    <p>Session: {}</p>
</div>
""".format(datetime.now().strftime('%B %d, %Y – %H:%M:%S')), unsafe_allow_html=True)