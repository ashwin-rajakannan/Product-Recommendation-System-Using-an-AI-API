#!/usr/bin/env python3
"""
Demo script for AI-Powered Voice Notes Workspace
Shows key features and capabilities of the application
"""

import os
import sys
import time
import webbrowser
from pathlib import Path

def print_banner():
    """Display application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║              AI-Powered Voice Notes Workspace               ║
    ║                     Interactive Demo                         ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_features():
    """Display key features"""
    features = """
    🎯 Key Features:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    🎤 Voice Recognition      │ Real-time speech-to-text conversion
    📝 Rich Text Editor       │ Professional Quill.js integration
    🗣️  Voice Commands        │ Hands-free navigation and control
    📱 Modern UI              │ Three-column Joplin/OneNote layout
    🔍 Smart Search           │ Content search with highlighting
    🗑️  Trash System          │ Soft delete with restore capability
    📄 Export Options         │ PDF, Word, and Email export
    ⌨️  Keyboard Shortcuts    │ Power user productivity features
    🔄 Auto-Save             │ Automatic note persistence
    🌐 Browser Support        │ Chrome, Edge optimized
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """
    print(features)

def print_commands():
    """Display available voice commands"""
    commands = """
    🎙️  Voice Commands:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    "new note"                │ Create a new note
    "search [query]"          │ Search notes by content
    "next note"               │ Navigate to next note
    "previous note"           │ Navigate to previous note
    "start recording"         │ Begin audio recording
    "stop recording"          │ End audio recording
    "start live"              │ Begin live transcription
    "stop live"               │ End live transcription (hands-free!)
    "export pdf"              │ Export current note as PDF
    "export word"             │ Export current note as Word
    "clear all"               │ Clear all content
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """
    print(commands)

def print_shortcuts():
    """Display keyboard shortcuts"""
    shortcuts = """
    ⌨️  Keyboard Shortcuts:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    Ctrl+Alt+N               │ Create new note
    Ctrl+F                   │ Search notes
    Ctrl+↑ / Ctrl+↓          │ Navigate between notes
    Ctrl+R                   │ Start/Stop recording
    Ctrl+Alt+T               │ Toggle Live Transcribe
    Ctrl+E                   │ Open export dropdown
    Ctrl+Z                   │ Undo (in editor)
    Ctrl+Y                   │ Redo (in editor)
    Ctrl+B                   │ Bold text
    Ctrl+I                   │ Italic text
    Ctrl+U                   │ Underline text
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """
    print(shortcuts)

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import speech_recognition
        import vosk
        print("✅ All dependencies are installed and ready!")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def start_demo():
    """Start the demo application"""
    print("\n🚀 Starting AI-Powered Voice Notes Workspace...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Check if web_assistant.py exists
    if not os.path.exists('web_assistant.py'):
        print("❌ web_assistant.py not found. Please run from project root directory.")
        return False
    
    print("\n📱 Application will open in your default browser...")
    print("🌐 URL: http://127.0.0.1:5000")
    print("\n💡 Tips for best experience:")
    print("   • Use Google Chrome for optimal performance")
    print("   • Allow microphone permissions when prompted")
    print("   • Speak clearly and avoid background noise")
    print("   • Try the voice commands listed above")
    
    # Open browser after a delay
    time.sleep(2)
    webbrowser.open('http://127.0.0.1:5000')
    
    # Start the Flask application
    print("\n🔄 Launching Flask server...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    os.system('python web_assistant.py')

def main():
    """Main demo function"""
    print_banner()
    
    if not check_dependencies():
        return
    
    print_features()
    print_commands()
    print_shortcuts()
    
    print("\n🎯 Demo Options:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("1. 🌟 Launch Full Application (Recommended)")
    print("2. 🎙️  Live Transcription Mode")
    print("3. 💻 CLI Mode (Terminal-based)")
    print("4. ℹ️  Show Help Documentation")
    print("5. 🚪 Exit")
    
    while True:
        try:
            choice = input("\n👉 Select option (1-5): ").strip()
            
            if choice == '1':
                start_demo()
                break
            elif choice == '2':
                print("\n🎙️  Starting Live Transcription Mode...")
                webbrowser.open('http://127.0.0.1:5000/live')
                os.system('python live_web_assistant.py')
                break
            elif choice == '3':
                print("\n💻 Starting CLI Mode...")
                os.system('python main.py')
                break
            elif choice == '4':
                print("\n📖 Opening GitHub Repository...")
                webbrowser.open('https://github.com/ashwin-rajakannan/AI-powered-voice-notes-workspace')
                continue
            elif choice == '5':
                print("\n👋 Thank you for trying AI-Powered Voice Notes Workspace!")
                print("⭐ Star the repository if you found it helpful!")
                break
            else:
                print("❌ Invalid option. Please select 1-5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()