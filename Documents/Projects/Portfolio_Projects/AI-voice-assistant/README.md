# AI-Powered Voice Notes Workspace

A modern, AI-powered voice note-taking application with rich text editing capabilities and intelligent features.

## 🚀 Features

### 📝 Rich Text Editing
- **Quill.js Integration**: Professional rich text editor with formatting tools
- **Bold, Italic, Underline**: Standard text formatting options
- **Lists & Headers**: Bullet points, numbered lists, and heading styles
- **Color Options**: Text and background color customization

### 🎤 Voice & Audio
- **Live Transcription**: Real-time speech-to-text conversion
- **Voice Commands**: Hands-free navigation and control
- **Audio Recording**: Record and transcribe audio notes
- **Multi-browser Support**: Works with Chrome, Edge (optimized for Chrome)

### 🗂️ Note Management
- **Three-Column Layout**: Joplin/OneNote-style interface
- **Smart Search**: Search by title, content, or both with highlighting
- **Trash System**: Soft delete with restore capability
- **Auto-save**: Automatic saving of notes as you type

### 📤 Export Options
- **PDF Export**: Generate professional PDF documents
- **Word Export**: Export as RTF/Word-compatible files
- **Email Integration**: Send notes via email directly

### 🎯 Advanced Features
- **Keyboard Shortcuts**: Efficient navigation and control
- **Symbol Quick Insert**: Fast access to common punctuation
- **Date Filtering**: Filter notes by creation date
- **Responsive Design**: Works on desktop and mobile devices

## 🛠️ Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Rich Text Editor**: Quill.js (Snow theme)
- **Voice Recognition**: Web Speech API
- **Audio Processing**: Vosk (offline transcription fallback)
- **Backend**: Python Flask
- **Export Libraries**: html2pdf.js, html-docx.js
- **Storage**: LocalStorage for client-side note persistence

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Modern web browser (Chrome recommended)
- Microphone access for voice features

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ashwin-rajakannan/AI-powered-voice-notes-workspace.git
   cd AI-powered-voice-notes-workspace
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python web_assistant.py
   ```

5. **Open in browser**
   Navigate to `http://127.0.0.1:5000`

## 🎮 Usage Guide

### Voice Commands
- **"new note"** - Create a new note
- **"search [title]"** - Search for notes by title
- **"next note"** / **"previous note"** - Navigate between notes
- **"start recording"** / **"stop recording"** - Audio recording
- **"start live"** - Begin live transcription
- **"stop live"** - End live transcription (hands-free!)

### Keyboard Shortcuts
- **Ctrl+Alt+N** - New note
- **Ctrl+F** - Search notes
- **Ctrl+↑/↓** - Previous/Next note
- **Ctrl+R** - Start/Stop recording
- **Ctrl+Alt+T** - Start/Stop Live Transcribe

### Tips for Best Results
- Use Google Chrome for optimal performance
- Wear earphones and keep mic close to your mouth
- Speak clearly and avoid background noise
- Record at least 2-3 seconds of audio
- Check microphone permissions

## 🏗️ Architecture

```
├── templates/
│   └── index.html          # Main UI with Quill editor integration
├── static/
│   ├── quill.min.js        # Rich text editor library
│   ├── quill.snow.css      # Editor styling
│   ├── html2pdf.bundle.min.js  # PDF export
│   └── html-docx.js        # Word export
├── models/
│   └── vosk/              # Offline speech recognition model
├── web_assistant.py        # Flask backend server
├── main.py                # Alternative entry point
└── requirements.txt        # Python dependencies
```

## 🌐 Browser Compatibility

| Feature | Chrome | Edge | Firefox | Safari |
|---------|--------|------|---------|--------|
| Rich Text Editing | ✅ | ✅ | ✅ | ✅ |
| Voice Commands | ✅ | ✅ | ❌ | ❌ |
| Live Transcribe | ✅ | ✅ | ❌ | ❌ |
| Audio Recording | ✅ | ✅ | ✅ | ✅ |
| Export Features | ✅ | ✅ | ✅ | ✅ |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 👨‍💻 Author

**Ashwin Rajakannan**
- GitHub: [@ashwin-rajakannan](https://github.com/ashwin-rajakannan)

## 🙏 Acknowledgments

- [Quill.js](https://quilljs.com/) - Rich text editor
- [Vosk](https://alphacephei.com/vosk/) - Open-source speech recognition
- [html2pdf.js](https://github.com/eKoopmans/html2pdf.js) - Client-side PDF generation
- Web Speech API - Browser-based speech recognition

---

⭐ **Star this repository if you find it helpful!**
