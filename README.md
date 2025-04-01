##Speech-to-Text and Translation Tool

Overview

This project is a powerful and user-friendly GUI-based speech-to-text and translation tool that enables users to transcribe and translate audio from multiple sources. The tool is designed to handle real-time speech, audio files, video files, and even documents containing text. With its intuitive interface, users can seamlessly convert spoken words into written text and translate them into various languages, making it useful for students, professionals, and researchers.

Key Features

Speech-to-Text Conversion

Converts spoken words from different input sources into accurate text.

Supports live transcription from a microphone.

Processes pre-recorded audio files and extracts text.

Extracts and transcribes audio from video files.

Multilingual Support

Provides transcription support for multiple Indian languages and English.

Allows translation of transcribed text into different languages for better accessibility.

Document Processing

Extracts text from .docx (Microsoft Word) and .pdf files for easy content digitization.

Supports different document formats, making it helpful for students and researchers.

Advanced Audio Processing

Segments long-duration audio files into smaller, manageable chunks for better accuracy.

Works with different audio formats such as .wav, .mp3, .ogg, and .flac.

Automatically removes background noise and enhances clarity.

Text Translation

Converts transcribed text into multiple languages for broader accessibility.

Uses reliable translation services for improved accuracy.

Save and Export Options

Allows users to save transcriptions and translations as .txt or .pdf files.

Facilitates easy sharing and documentation.

User-Friendly Interface

Built using Tkinter to provide a simple yet effective GUI.

Designed for ease of use with clear buttons and options.

Technologies Used

Python: Core programming language for implementation.

Tkinter: GUI framework for creating the user interface.

SpeechRecognition: Converts speech into text.

Googletrans: Enables text translation into multiple languages.

PyPDF2: Extracts text from .pdf documents.

python-docx: Extracts text from .docx files.

pydub: Handles audio file processing and segmentation.

FPDF: Generates .pdf files for exported transcriptions.

Installation Guide

1. Clone the Repository

git clone https://github.com/yourusername/speech-to-text-tool.git
cd speech-to-text-tool

2. Install Required Dependencies

pip install -r requirements.txt

How to Use

Run the Application

python main.py

Choose an Input Source:

Microphone (for live speech input)

Audio File (upload .wav, .mp3, .ogg, .flac files)

Video File (extracts audio from .mp4 files)

Document (processes .pdf and .docx files)

Select Transcription Language

Process the Input to convert speech into text.

Translate the Text (Optional) into a chosen language.

Save the Output as .txt or .pdf for later use.

Supported Languages

Transcription

English (US, UK)

Hindi

Tamil

Telugu

Bengali

Marathi

Gujarati

Punjabi

Malayalam

Kannada

Urdu

Translation

Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Punjabi, Malayalam, Kannada, Urdu, English

File Processing Capabilities

Audio Files: Supports .wav, .mp3, .ogg, and .flac formats.

Video Files: Extracts audio from .mp4 and processes it for transcription.

Document Files: Extracts text from .pdf and .docx files.

Future Enhancements

Real-Time Transcription: Support for live speech-to-text in meetings.

Cloud-Based Processing: Faster and more efficient transcription through cloud computing.

AI-Powered Language Models: Improve accuracy using advanced machine learning techniques.

Mobile Application: Expanding the tool to mobile devices for on-the-go use
