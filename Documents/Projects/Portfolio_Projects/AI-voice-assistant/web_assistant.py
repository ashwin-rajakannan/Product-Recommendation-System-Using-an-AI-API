from flask import Flask, render_template, request, jsonify
import os
import sys
import zipfile
import requests
import speech_recognition as sr
from werkzeug.utils import secure_filename
from pydub import AudioSegment
import wave
import json
import io

app = Flask(__name__)

# --- Vosk Streaming Transcription Endpoint ---
@app.route('/transcribe_vosk', methods=['POST'])
def transcribe_vosk():
    if vosk_model is None:
        return jsonify({'error': 'Vosk model not available'}), 500
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    audio_file = request.files['audio']
    audio_bytes = audio_file.read()
    # Assume audio is WAV PCM 16kHz mono (frontend must send this format)
    wf = wave.open(io.BytesIO(audio_bytes), 'rb')
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        return jsonify({'error': 'Audio must be WAV PCM 16kHz mono'}), 400
    from vosk import KaldiRecognizer
    rec = KaldiRecognizer(vosk_model, 16000)
    words = []
    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part = json.loads(rec.Result())
            if 'result' in part:
                words.extend(part['result'])
            results.append(part.get('text', ''))
    final = json.loads(rec.FinalResult())
    if 'result' in final:
        words.extend(final['result'])
    results.append(final.get('text', ''))
    transcript = ' '.join([r for r in results if r])
    # words: list of dicts with 'word' and 'conf' keys
    return jsonify({'text': transcript, 'words': words})

# --- Vosk Model Setup ---
VOSK_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'vosk', 'vosk-model-small-en-us-0.15')
VOSK_MODEL_URL = 'https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip'
VOSK_MODEL_ZIP = os.path.join(os.path.dirname(__file__), 'models', 'vosk', 'vosk-model-small-en-us-0.15.zip')

def download_and_extract_vosk_model():
    if not os.path.exists(VOSK_MODEL_PATH):
        print('Vosk model not found. Downloading...')
        os.makedirs(os.path.dirname(VOSK_MODEL_PATH), exist_ok=True)
        with requests.get(VOSK_MODEL_URL, stream=True) as r:
            r.raise_for_status()
            with open(VOSK_MODEL_ZIP, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print('Download complete. Extracting...')
        with zipfile.ZipFile(VOSK_MODEL_ZIP, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(VOSK_MODEL_PATH))
        print('Extraction complete.')
        os.remove(VOSK_MODEL_ZIP)
    else:
        print('Vosk model already present.')

try:
    from vosk import Model
    download_and_extract_vosk_model()
    vosk_model = Model(VOSK_MODEL_PATH)
    print('Vosk model loaded successfully.')
except Exception as e:
    print('Error loading Vosk model:', e)
    vosk_model = None

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
    # Auto-detect format and convert to wav
    wav_path = temp_path + '.wav'
    try:
        print(f"[DEBUG] Attempting to convert {temp_path} to WAV (auto-detecting format)...")
        # Let pydub/ffmpeg auto-detect the format instead of hardcoding 'webm'
        audio = AudioSegment.from_file(temp_path)
        audio.export(wav_path, format='wav')
        print(f"[DEBUG] Converted {filename} to WAV: {wav_path}")
    except Exception as e:
        conversion_error = traceback.format_exc()
        print(f"[ERROR] Audio conversion failed: {conversion_error}")
        os.remove(temp_path)
        return jsonify({'error': 'Audio conversion failed', 'details': str(e), 'trace': conversion_error}), 500
    recognizer = sr.Recognizer()
    text = ""
    
    # Try Google Speech Recognition first
    try:
        with sr.AudioFile(wav_path) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        print(f"[DEBUG] Google transcription result: {text}")
    except Exception as e:
        print(f"[ERROR] Google transcription failed: {e}")
        
        # Fallback to Vosk if available
        if vosk_model is not None:
            print("[DEBUG] Trying Vosk fallback...")
            try:
                from vosk import KaldiRecognizer
                import wave
                
                # Open WAV file for Vosk
                wf = wave.open(wav_path, 'rb')
                if wf.getnchannels() == 1 and wf.getsampwidth() == 2 and wf.getframerate() == 16000:
                    # File is already in correct format for Vosk
                    rec = KaldiRecognizer(vosk_model, 16000)
                    results = []
                    
                    while True:
                        data = wf.readframes(4000)
                        if len(data) == 0:
                            break
                        if rec.AcceptWaveform(data):
                            part = json.loads(rec.Result())
                            results.append(part.get('text', ''))
                    
                    final = json.loads(rec.FinalResult())
                    results.append(final.get('text', ''))
                    text = ' '.join([r for r in results if r])
                    wf.close()
                    print(f"[DEBUG] Vosk transcription result: {text}")
                else:
                    # Need to resample for Vosk
                    wf.close()
                    print("[DEBUG] Resampling audio to 16kHz mono for Vosk...")
                    audio = AudioSegment.from_wav(wav_path)
                    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
                    vosk_wav_path = wav_path + '_vosk.wav'
                    audio.export(vosk_wav_path, format='wav')
                    
                    wf = wave.open(vosk_wav_path, 'rb')
                    rec = KaldiRecognizer(vosk_model, 16000)
                    results = []
                    
                    while True:
                        data = wf.readframes(4000)
                        if len(data) == 0:
                            break
                        if rec.AcceptWaveform(data):
                            part = json.loads(rec.Result())
                            results.append(part.get('text', ''))
                    
                    final = json.loads(rec.FinalResult())
                    results.append(final.get('text', ''))
                    text = ' '.join([r for r in results if r])
                    wf.close()
                    
                    # Clean up Vosk temp file
                    if os.path.exists(vosk_wav_path):
                        os.remove(vosk_wav_path)
                    print(f"[DEBUG] Vosk transcription result: {text}")
                    
            except Exception as vosk_error:
                print(f"[ERROR] Vosk transcription also failed: {vosk_error}")
                # Clean up temp files
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                if wav_path != temp_path and os.path.exists(wav_path):
                    os.remove(wav_path)
                return jsonify({'text': '', 'error': 'Both Google and offline transcription failed. Try again.'}), 200
        else:
            # No Vosk available, return error
            if os.path.exists(temp_path):
                os.remove(temp_path)
            if wav_path != temp_path and os.path.exists(wav_path):
                os.remove(wav_path)
            return jsonify({'text': '', 'error': 'Transcription failed. Try again.'}), 200
    
    # Return empty result if no text was transcribed
    if not text.strip():
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if wav_path != temp_path and os.path.exists(wav_path):
            os.remove(wav_path)
        return jsonify({'text': '', 'error': 'No speech detected. Try again.'}), 200
    # Clean up temp files
    if os.path.exists(temp_path):
        os.remove(temp_path)
    if wav_path != temp_path and os.path.exists(wav_path):
        os.remove(wav_path)
    return jsonify({'text': text})



if __name__ == '__main__':
    app.run(debug=True)
