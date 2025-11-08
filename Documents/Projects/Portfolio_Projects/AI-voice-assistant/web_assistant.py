
from flask import Flask, render_template, request, jsonify
import os
import speech_recognition as sr
from werkzeug.utils import secure_filename
from pydub import AudioSegment

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    import traceback
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    audio_file = request.files['audio']
    filename = secure_filename(audio_file.filename)
    temp_dir = 'temp'
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, filename)
    audio_file.save(temp_path)
    file_size = os.path.getsize(temp_path)
    print(f"[DEBUG] Received file: {filename}, size: {file_size} bytes")
    # Convert to wav if not already
    wav_path = temp_path
    conversion_error = None
    # Always treat as webm/ogg and convert to wav
    wav_path = temp_path + '.wav'
    try:
        print(f"[DEBUG] Attempting to convert {temp_path} to WAV using pydub...")
        audio = AudioSegment.from_file(temp_path, format='webm')
        audio.export(wav_path, format='wav')
        print(f"[DEBUG] Converted {filename} to WAV: {wav_path}")
    except Exception as e:
        conversion_error = traceback.format_exc()
        print(f"[ERROR] Audio conversion failed: {conversion_error}")
        os.remove(temp_path)
        return jsonify({'error': 'Audio conversion failed', 'details': str(e), 'trace': conversion_error}), 500
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(wav_path) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        print(f"[DEBUG] Transcription result: {text}")
    except Exception as e:
        print(f"[ERROR] Transcription failed: {e}")
        # Clean up temp files
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if wav_path != temp_path and os.path.exists(wav_path):
            os.remove(wav_path)
        return jsonify({'text': '', 'error': 'Transcription failed. Try again.'}), 200
    # Clean up temp files
    if os.path.exists(temp_path):
        os.remove(temp_path)
    if wav_path != temp_path and os.path.exists(wav_path):
        os.remove(wav_path)
    return jsonify({'text': text})



if __name__ == '__main__':
    app.run(debug=True)
