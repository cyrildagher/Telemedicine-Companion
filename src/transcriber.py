import os
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin" 

def transcribe_audio(file_path: str, model_size="base") -> str:
    import whisper
    model = whisper.load_model(model_size)
    result = model.transcribe(file_path)
    return result["text"]