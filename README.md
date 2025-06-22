# 🩺 Telemedicine Companion Extractor

An open-source, offline Python system that transcribes teleconsultation audio and extracts structured clinical notes—including symptoms, medications, diagnoses, and follow-up instructions—using modern AI tools.

---

## 🚀 Project Goals

- Reduce clinical documentation burden in telemedicine
- Convert audio consultations into structured, editable notes
- Use only free and open-source tools (no API costs, no cloud)

---

## 🧱 Tech Stack

| Component         | Tool                |
|------------------|---------------------|
| STT (Transcription) | [Whisper](https://github.com/openai/whisper) |
| NLP Engine        | spaCy + scispaCy    |
| Database          | MariaDB / MySQL     |
| UI (Optional)     | Streamlit           |
| Audio Processing  | ffmpeg, pydub       |
| Language          | Python 3.10+        |

---

## 🛠 Features

- Offline speech-to-text transcription using Whisper
- Medical entity extraction (symptoms, meds, diagnoses)
- Structured output in JSON and SQL-ready format
- Modular, backend-first design for expandability
- Lightweight UI for data visualization (optional)

---

## 📂 Project Structure
