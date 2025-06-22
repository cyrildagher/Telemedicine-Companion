import os
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"
from pydub import AudioSegment
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
from pydub.utils import which
print("FFmpeg found at:", which("ffmpeg"))

import numpy as np
import whisper

# Hardwire ffmpeg path
ffmpeg_path = which("ffmpeg") or r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.converter = ffmpeg_path
os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)
# Load audio with pydub
audio = AudioSegment.from_file("audio_samples/consultation1.wav")
samples = np.array(audio.get_array_of_samples()).astype(np.float32) / 32768.0

# If stereo, convert to mono
if audio.channels > 1:
    samples = samples.reshape((-1, audio.channels)).mean(axis=1)

# Whisper expects 30 seconds of audio at 16000Hz
samples = whisper.pad_or_trim(samples)
mel = whisper.log_mel_spectrogram(samples).to("cpu")

# Load model and decode
model = whisper.load_model("small")
options = whisper.DecodingOptions(language="en", fp16=False)
result = whisper.decode(model, mel, options)

# Print the transcript
print(result.text)

# Save transcript to file
with open("transcripts/sample_transcript.txt", "w", encoding="utf-8") as f:
    f.write(result.text)