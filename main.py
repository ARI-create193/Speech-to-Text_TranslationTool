import os
import speech_recognition as sr
from googletrans import Translator
from docx import Document
import PyPDF2
from pydub import AudioSegment, silence
from fpdf import FPDF
import gradio as gr

# Directory for storing transcripts
output_dir = "transcripts"
os.makedirs(output_dir, exist_ok=True)

# Supported languages for transcription
languages = {
    "English (US)": "en-US",
    "English (UK)": "en-GB",
    "Hindi": "hi-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Bengali": "bn-IN",
    "Marathi": "mr-IN",
    "Gujarati": "gu-IN",
    "Punjabi": "pa-IN",
    "Malayalam": "ml-IN",
    "Kannada": "kn-IN",
    "Urdu": "ur-IN",
}

# Supported languages for translation
translation_languages = {
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Bengali": "bn",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Malayalam": "ml",
    "Kannada": "kn",
    "Urdu": "ur",
    "English": "en",
}

def split_audio(audio_path, chunk_length_ms=60000):
    """Splits audio into smaller chunks to handle longer files."""
    audio = AudioSegment.from_file(audio_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks

def audio_to_text(audio_path, language_code):
    """Converts large audio to text by processing it in chunks."""
    recognizer = sr.Recognizer()
    try:
        chunks = split_audio(audio_path)
        processing_log = f"Audio split into {len(chunks)} chunks for processing...\n"
        full_transcript = ""
        
        for i, chunk in enumerate(chunks):
            chunk_path = os.path.join(output_dir, f"chunk_{i}.wav")
            chunk.export(chunk_path, format="wav")
            
            with sr.AudioFile(chunk_path) as source:
                processing_log += f"Processing chunk {i + 1}...\n"
                audio = recognizer.record(source)
            
            try:
                chunk_text = recognizer.recognize_google(audio, language=language_code)
                full_transcript += chunk_text + " "
                processing_log += f"Chunk {i + 1} transcription complete.\n"
            except sr.UnknownValueError:
                processing_log += f"Chunk {i + 1}: Could not understand audio.\n"
            except sr.RequestError:
                processing_log += "Speech Recognition service unavailable.\n"
        
        return full_transcript.strip(), processing_log
    except Exception as e:
        return f"Error: {str(e)}", f"Error occurred: {str(e)}"

def process_microphone_input(audio_path, language_code):
    """Processes speech input from the microphone."""
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            processing_log = "Processing your speech...\n"
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language=language_code)
            return text, processing_log + "Speech recognition complete."
    except sr.UnknownValueError:
        return "Could not understand audio.", "Speech recognition failed: Could not understand audio."
    except sr.RequestError:
        return "Speech Recognition service unavailable.", "Speech recognition failed: Service unavailable."
    except Exception as e:
        return f"Error: {str(e)}", f"Error occurred: {str(e)}"

def translate_text(text, target_language):
    """Translates text into the specified language using googletrans."""
    translator = Translator()
    try:
        translated = translator.translate(text, dest=target_language).text
        return translated, "Translation complete."
    except Exception as e:
        return f"Translation failed: {str(e)}", f"Error in translation: {str(e)}"

def read_docx(file_path):
    """Reads text from a Word document."""
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def read_pdf(file_path):
    """Reads text from a PDF file."""
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_audio_from_video(video_path, audio_path):
    """Extracts audio from a video file and saves it as a WAV file."""
    try:
        # Using pydub to extract audio from the video file
        audio = AudioSegment.from_file(video_path)
        audio.export(audio_path, format="wav")
        return f"Audio extracted and saved to {audio_path}"
    except Exception as e:
        return f"An error occurred while extracting audio: {e}"

def save_as_pdf(text):
    """Saves the text as a PDF file."""
    if not text:
        return None, "No text available to save."
        
    file_path = os.path.join(output_dir, "translated_output.pdf")
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, text)
        pdf.output(file_path)
        return file_path, f"Text saved as PDF: {file_path}"
    except Exception as e:
        return None, f"Failed to save PDF: {str(e)}"

# Process functions for Gradio
def process_input(input_type, input_file, transcription_lang, translation_lang):
    transcript = ""
    processing_log = ""
    translated_text = ""
    translation_log = ""
    pdf_path = None
    pdf_log = ""
    
    if input_type == "Microphone" and input_file is not None:
        language_code = languages.get(transcription_lang, "en-US")
        transcript, processing_log = process_microphone_input(input_file, language_code)
    elif input_type == "Audio" and input_file is not None:
        language_code = languages.get(transcription_lang, "en-US")
        transcript, processing_log = audio_to_text(input_file, language_code)
    elif input_type == "Video" and input_file is not None:
        audio_path = os.path.join(output_dir, "temp_audio.wav")
        processing_log = extract_audio_from_video(input_file, audio_path)
        language_code = languages.get(transcription_lang, "en-US")
        transcript_result, transcript_log = audio_to_text(audio_path, language_code)
        transcript = transcript_result
        processing_log += "\n" + transcript_log
    elif input_type == "Document" and input_file is not None:
        if input_file.endswith(".docx"):
            transcript = read_docx(input_file)
            processing_log = "Document processed successfully."
        elif input_file.endswith(".pdf"):
            transcript = read_pdf(input_file)
            processing_log = "Document processed successfully."
        else:
            processing_log = "Unsupported document format."
    else:
        processing_log = "Please provide a valid input file."
    
    # Save transcript
    if transcript:
        output_file = os.path.join(output_dir, "transcript.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(transcript)
        processing_log += f"\nTranscript saved to {output_file}"
    
    # Translate if there's transcript content
    if transcript:
        target_code = translation_languages.get(translation_lang, "en")
        translated_text, translation_log = translate_text(transcript, target_code)
    
    # Save PDF if translation is available
    if translated_text:
        pdf_path, pdf_log = save_as_pdf(translated_text)
    
    return transcript, processing_log, translated_text, translation_log, pdf_path, pdf_log

# Gradio Interface
def run_app():
    with gr.Blocks(title="Speech-to-Text Tool with Translation") as app:
        gr.Markdown("# Speech-to-Text Tool with Translation")
        
        with gr.Row():
            with gr.Column(scale=1):
                # Input section
                input_type = gr.Radio(
                    ["Audio", "Video", "Document", "Microphone"], 
                    label="Input Type", 
                    value="Audio"
                )
                
                # Conditional components based on input type
                with gr.Group():
                    audio_input = gr.Audio(label="Audio File", type="filepath")
                    video_input = gr.Video(label="Video File", format="mp4")
                    document_input = gr.File(label="Document File")
                    microphone_input = gr.Audio(label="Microphone Input", source="microphone", type="filepath")
                
                transcription_lang = gr.Dropdown(
                    list(languages.keys()), 
                    label="Transcription Language", 
                    value="English (US)"
                )
                
                translation_lang = gr.Dropdown(
                    list(translation_languages.keys()), 
                    label="Translation Language", 
                    value="Hindi"
                )
                
                process_button = gr.Button("Process Input")
                
            with gr.Column(scale=2):
                # Output section
                transcript_output = gr.Textbox(label="Transcript", lines=8)
                processing_log = gr.Textbox(label="Processing Log", lines=5)
                
                translated_output = gr.Textbox(label="Translated Text", lines=8)
                translation_log = gr.Textbox(label="Translation Log", lines=2)
                
                pdf_output = gr.File(label="PDF Output")
                pdf_log = gr.Textbox(label="PDF Generation Log", lines=2)
        
        # Dynamic visibility based on input type
        def update_visibility(input_type):
            return {
                audio_input: input_type == "Audio",
                video_input: input_type == "Video",
                document_input: input_type == "Document",
                microphone_input: input_type == "Microphone"
            }
        
        input_type.change(fn=update_visibility, inputs=input_type, outputs=[
            audio_input, video_input, document_input, microphone_input
        ])
        
        def get_input_file(input_type, audio_file, video_file, document_file, mic_file):
            if input_type == "Audio" and audio_file:
                return audio_file
            elif input_type == "Video" and video_file:
                return video_file
            elif input_type == "Document" and document_file:
                return document_file
            elif input_type == "Microphone" and mic_file:
                return mic_file
            return None
        
        process_button.click(
            fn=lambda t, a, v, d, m, tl, trl: process_input(
                t, 
                get_input_file(t, a, v, d, m),
                tl,
                trl
            ),
            inputs=[
                input_type, 
                audio_input, 
                video_input, 
                document_input, 
                microphone_input,
                transcription_lang,
                translation_lang
            ],
            outputs=[
                transcript_output, 
                processing_log,
                translated_output,
                translation_log,
                pdf_output,
                pdf_log
            ]
        )
    
    app.launch()

if __name__ == "__main__":
    run_app()
