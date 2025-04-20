# Speech-to-Text Tool with Translation

A versatile speech-to-text application with multilingual translation capabilities, now featuring a modern Gradio web interface.

## Overview

This tool allows users to convert speech to text from multiple sources (audio files, video files, microphone recordings, and text documents) and translate the transcribed text into various Indian languages. The application features a user-friendly Gradio web interface that makes the tool accessible and easy to use.

## Features

- 🎤 **Multiple Input Types:**
  - Audio files
  - Video files (extracts audio automatically)
  - Document files (PDF, DOCX)
  - Microphone recording

- 🌍 **Multilingual Support:**
  - Transcription in 12 languages including English (US & UK), Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Punjabi, Malayalam, Kannada, and Urdu
  - Translation into 11 languages including English, Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Punjabi, Malayalam, Kannada, and Urdu

- ⚙️ **Process Handling:**
  - Automatic chunking of large audio files
  - Progress tracking with detailed logs
  - PDF export of translated text

- 💻 **User Interface:**
  - Modern, responsive Gradio web interface
  - Conditional input components based on selected input type
  - Comprehensive output displays

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/speech-to-text-translation.git
cd speech-to-text-translation
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Dependencies

- SpeechRecognition
- googletrans
- python-docx
- PyPDF2
- pydub
- fpdf
- gradio

## Usage

Run the application:
```bash
python app.py
```

The application will start a local web server, typically at http://127.0.0.1:7860/, which you can access through your web browser.

### Using the Application

1. **Select Input Type**:
   - Choose between Audio, Video, Document, or Microphone

2. **Upload or Record**:
   - For Audio/Video/Document: Upload the file
   - For Microphone: Click to record your voice

3. **Choose Languages**:
   - Select the transcription language (source language)
   - Select the translation language (target language)

4. **Process**:
   - Click "Process Input" to start transcription
   - View the transcript and processing logs
   - View the translated text and download the PDF if needed

## Implementation Details

The application is built with modular components:

- 🔊 **Audio Processing**: Uses `pydub` for audio manipulation and chunking
- 🗣️ **Speech Recognition**: Utilizes Google's Speech Recognition API through `SpeechRecognition`
- 🔄 **Translation**: Implements `googletrans` for multilingual translation
- 📄 **Document Processing**: Handles PDF and DOCX files using `PyPDF2` and `python-docx`
- 🖥️ **User Interface**: Built with `gradio` for a modern web-based experience

## Project Structure

```
.
├── app.py                  # Main application file
├── transcripts/            # Directory for storing transcripts and audio chunks
│   ├── transcript.txt      # Latest transcript
│   ├── translated_output.pdf # Latest translated PDF
│   └── ...                 # Temporary audio chunks
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## Recent Updates

- 🆕 Migrated from Tkinter to Gradio for a more modern, web-based user interface
- 👁️ Added conditional visibility for input components based on selected input type
- 🛠️ Improved error handling and user feedback through detailed logs
- 📑 Enhanced PDF export functionality for translated text

## Future Improvements

- Add support for more languages
- Implement batch processing for multiple files
- Add options for different speech recognition engines
- Provide more advanced audio processing options
- Support for real-time transcription and translation

## Contact
Gmail - aryankaminwar@gmail.com 

## Acknowledgments

- Google Speech Recognition API for speech recognition capabilities
- Gradio for the modern web interface framework
