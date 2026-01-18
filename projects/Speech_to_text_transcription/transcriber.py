import speech_recognition as sr

def transcribe_from_file(audio_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        print("Listening to file...")
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        print("\nTranscription:")
        print(text)
    except sr.UnknownValueError:
        print("Sorry — audio not clear.")
    except sr.RequestError:
        print("API unavailable — check internet.")


def transcribe_from_microphone():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak now... 🎤")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("\nYou said:")
        print(text)
    except sr.UnknownValueError:
        print("Could not understand.")
    except sr.RequestError:
        print("Check your internet connection.")


if __name__ == "__main__":
    print("""
1️⃣ Transcribe from audio file
2️⃣ Transcribe using microphone
""")

    choice = input("Choose option (1 or 2): ")

    if choice == "1":
        path = input("Enter audio file path (wav/mp3): ")
        transcribe_from_file(path)

    elif choice == "2":
        transcribe_from_microphone()

    else:
        print("Invalid option.")
