import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
from utils import auto_punctuate
from audio_recorder_streamlit import audio_recorder
import tempfile
import os


st.set_page_config(page_title="Speech-to-Text App", layout="centered")
st.title("🗣️ Speech-to-Text Transcription (Multi-Language)")


st.write("Record or upload audio and convert speech to text — supports multiple languages.")


# ---------------- LANGUAGE SELECT ----------------
languages = {
    "English (US)": "en-US",
    "Hindi": "hi-IN",
    "Marathi": "mr-IN",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "German": "de-DE",
    "Tamil": "ta-IN",
    "Telugu": "te-IN"
}

language_choice = st.selectbox("Select Language", list(languages.keys()))
language_code = languages[language_choice]


# ---------------- AUDIO INPUT ----------------
st.subheader("🎙️ Record or Upload Audio")

# Microphone
audio_bytes = audio_recorder(text="Click to record")

# File upload
uploaded_file = st.file_uploader("Or upload audio (wav/mp3)", type=["wav", "mp3"])

temp_path = None


# Handle microphone recording
if audio_bytes:
    st.info("Processing microphone recording…")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        temp.write(audio_bytes)
        temp_path = temp.name

# Handle uploaded file
elif uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        if uploaded_file.name.endswith(".mp3"):
            audio = AudioSegment.from_mp3(uploaded_file)
            audio.export(temp.name, format="wav")
        else:
            temp.write(uploaded_file.read())
        temp_path = temp.name
else:
    st.info("Upload a file or use microphone to start.")


# ---------------- SPEECH RECOGNITION ----------------
if temp_path:

    recognizer = sr.Recognizer()

    with sr.AudioFile(temp_path) as source:
        st.info("Listening…")
        audio_data = recognizer.record(source)

    try:
        st.info("Transcribing… please wait")
        text = recognizer.recognize_google(audio_data, language=language_code)

        formatted = auto_punctuate(text)

        st.success("Transcription complete!")
        st.write("### 📝 Output")
        st.text_area("", formatted, height=220)

        st.download_button(
            "Download as TXT",
            formatted,
            file_name="transcription.txt"
        )

    except sr.UnknownValueError:
        st.error("Audio unclear — could not understand.")
    except sr.RequestError:
        st.error("Network/API issue — check internet.")
    finally:
        os.remove(temp_path)
