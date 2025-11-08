import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os

def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "temp_voice.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)

def listen_with_confirmation(prompt=None):
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            recognizer.pause_threshold = 2.0
            if prompt:
                speak(prompt)
            print("Listening... Please start speaking.")
            import time
            time.sleep(1)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            speak("Sorry, I could not understand. Please try again.")
            continue
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            speak("Sorry, there was a problem with the speech service.")
            continue
        speak(f"You said: {text}. Is this correct? Say yes or no.")
        with sr.Microphone() as source:
            audio_confirm = recognizer.listen(source, timeout=5, phrase_time_limit=3)
        try:
            confirm = recognizer.recognize_google(audio_confirm).lower()
            print(f"Confirmation: {confirm}")
        except Exception:
            speak("Sorry, I did not catch that. Please say yes or no.")
            continue
        if "yes" in confirm:
            return text
        else:
            speak("Let's try again.")

def main():
    command = listen_with_confirmation("How can I help you?")
    if command:
        if "create note" in command.lower():
            note_content = listen_with_confirmation("What would you like the note to say?")
            if note_content:
                with open("notes.txt", "a") as f:
                    f.write(note_content + "\n")
                speak("Note saved.")
            else:
                speak("No note content detected.")
        else:
            speak(f"You said: {command}")

if __name__ == "__main__":
    main()
