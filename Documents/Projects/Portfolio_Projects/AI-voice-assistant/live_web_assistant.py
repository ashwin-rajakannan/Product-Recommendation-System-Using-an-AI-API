
import eventlet
import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('live_index.html')

@socketio.on('audio_chunk')
def handle_audio_chunk(data):
    import base64
    try:
        audio_bytes = base64.b64decode(data['chunk'].split(',')[1])
        fmt = data.get('format', 'ogg')
        if 'ogg' in fmt:
            audio = AudioSegment.from_file(BytesIO(audio_bytes), format='ogg')
        else:
            audio = AudioSegment.from_file(BytesIO(audio_bytes), format='webm')
        wav_io = BytesIO()
        audio.export(wav_io, format='wav')
        wav_io.seek(0)
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        emit('transcription', {'text': text})
    except Exception as e:
        emit('transcription', {'text': '', 'error': str(e)})

if __name__ == '__main__':
    socketio.run(app, debug=True)
