import os
import tkinter as tk
from tkinter import filedialog, messagebox
import speech_recognition as sr
from googletrans import Translator
from docx import Document
import PyPDF2
from pydub import AudioSegment, silence
from fpdf import FPDF

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
        text_display.insert(tk.END, f"Audio split into {len(chunks)} chunks for processing...\n")
        full_transcript = ""
        
        for i, chunk in enumerate(chunks):
            chunk_path = os.path.join(output_dir, f"chunk_{i}.wav")
            chunk.export(chunk_path, format="wav")
            
            with sr.AudioFile(chunk_path) as source:
                text_display.insert(tk.END, f"Processing chunk {i + 1}...\n")
                audio = recognizer.record(source)
            
            try:
                chunk_text = recognizer.recognize_google(audio, language=language_code)
                full_transcript += chunk_text + " "
                text_display.insert(tk.END, f"Chunk {i + 1} transcription complete.\n")
            except sr.UnknownValueError:
                text_display.insert(tk.END, f"Chunk {i + 1}: Could not understand audio.\n")
            except sr.RequestError:
                text_display.insert(tk.END, "Speech Recognition service unavailable.\n")
        
        return full_transcript.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def process_microphone_input(language_code):
    """Processes speech input from the microphone."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        text_display.insert(tk.END, "Listening... Speak now!\n")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text_display.insert(tk.END, "Processing your speech...\n")  # Provide feedback
            return recognizer.recognize_google(audio, language=language_code)
        except sr.UnknownValueError:
            return "Could not understand audio."
        except sr.RequestError:
            return "Speech Recognition service unavailable."
        except Exception as e:
            return f"Error: {str(e)}"

def translate_text(text, target_language):
    """Translates text into the specified language using googletrans."""
    translator = Translator()
    try:
        return translator.translate(text, dest=target_language).text
    except Exception as e:
        return f"Translation failed: {str(e)}"

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
        audio = AudioSegment.from_file(video_path, format="mp4")  # specify format if needed
        audio.export(audio_path, format="wav")
        print(f"Audio extracted and saved to {audio_path}")
    except Exception as e:
        print(f"An error occurred while extracting audio: {e}")

def save_as_pdf():
    """Saves the translated text as a PDF file."""
    translated_text = translated_text_display.get(1.0, tk.END).strip()
    if not translated_text:
        messagebox.showerror("Error", "No translated text available to save.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", ".pdf"), ("All files", ".*")]
    )
    if file_path:
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, translated_text)
            pdf.output(file_path)
            messagebox.showinfo("Success", f"Translated text saved as PDF: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF: {str(e)}")

# GUI Implementation
def run_app():
    global text_display, translated_text_display
    def browse_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            input_path_entry.delete(0, tk.END)
            input_path_entry.insert(0, file_path)

    def process_input():
        input_type = input_type_var.get().lower()
        input_path = input_path_entry.get().strip()
        transcript = ""
        
        if input_type == "microphone":
            language = lang_var.get()
            language_code = languages.get(language, "en-US")
            transcript = process_microphone_input(language_code)
        elif input_type in ["audio", "video"]:
            if not input_path:
                messagebox.showerror("Error", "Please provide a valid file path.")
                return
            if input_type == "audio":
                audio_path = input_path
            elif input_type == "video":
                audio_path = os.path.join(output_dir, "temp_audio.wav")
                extract_audio_from_video(input_path, audio_path)
            language = lang_var.get()
            language_code = languages.get(language, "en-US")
            transcript = audio_to_text(audio_path, language_code)
        elif input_type == "document":
            if not input_path or not os.path.exists(input_path):
                messagebox.showerror("Error", "Invalid file path for document.")
                return
            if input_path.endswith(".docx"):
                transcript = read_docx(input_path)
            elif input_path.endswith(".pdf"):
                transcript = read_pdf(input_path)
            else:
                messagebox.showerror("Error", "Unsupported document format.")
                return
        else:
            messagebox.showerror("Error", "Invalid input type selected.")
            return

        text_display.insert(tk.END, f"Transcript: {transcript}\n")
        save_transcript(transcript)

    def translate_output():
        output_text = text_display.get(1.0, tk.END).strip()
        if not output_text:
            messagebox.showerror("Error", "No output available to translate.")
            return
        target_language = translate_var.get()  # Use translate_var here
        target_code = translation_languages.get(target_language, "en")
        translated_text = translate_text(output_text, target_code)
        translated_text_display.insert(tk.END, f"\nTranslated Text: {translated_text}\n")

    def save_transcript(transcript):
        output_file = os.path.join(output_dir, "transcript.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(transcript)
        text_display.insert(tk.END, f"Transcript saved to {output_file}\n")
        messagebox.showinfo("Success", "Transcript saved successfully!")

    root = tk.Tk()
    root.title("Speech-to-Text Tool with Translation")
    root.geometry("750x800")
    root.configure(bg="#F5F5F5")

    header_font = ("Poppins", 20, "bold")
    label_font = ("Roboto", 14)
    button_font = ("Poppins", 14, "bold")

    # Header
    header = tk.Label(root, text="Speech-to-Text Tool with Translation", font=header_font, bg="#2C3E50", fg="white", pady=15)
    header.pack(fill=tk.X)

    # Input Type Selection
    input_frame = tk.Frame(root, bg="#2C3E50", pady=20)
    input_frame.pack(fill=tk.X, padx=20)
    tk.Label(input_frame, text="Input Type:", font=label_font, bg="#2C3E50", fg="white").grid(row=0, column=0, sticky="w", padx=10)
    input_type_var = tk.StringVar(value="Audio")
    tk.OptionMenu(input_frame, input_type_var, "Audio", "Video", "Document", "Microphone").grid(row=0, column=1, padx=10)

    # File Path Input
    tk.Label(input_frame, text="Input Path:", font=label_font, bg="#2C3E50", fg="white").grid(row=1, column=0, sticky="w", padx=10)
    input_path_entry = tk.Entry(input_frame, width=40, font=("Roboto", 12))
    input_path_entry.grid(row=1, column=1, padx=10)
    browse_button = tk.Button(input_frame, text="Browse", font=button_font, bg="#3498DB", fg="white", relief="flat", command=browse_file)
    browse_button.grid(row=1, column=2, padx=10)

    # Language Selection
    tk.Label(input_frame, text="Transcription Language:", font=label_font, bg="#2C3E50", fg="white").grid(row=2, column=0, sticky="w", padx=10)
    lang_var = tk.StringVar(value="English (US)")
    tk.OptionMenu(input_frame, lang_var, *languages.keys()).grid(row=2, column=1, padx=10)

    # Translation Language Selection
    tk.Label(input_frame, text="Translation Language:", font=label_font, bg="#2C3E50", fg="white").grid(row=3, column=0, sticky="w", padx=10)
    translate_var = tk.StringVar(value="Hindi")
    tk.OptionMenu(input_frame, translate_var, *translation_languages.keys()).grid(row=3, column=1, padx=10)

    # Button Frame
    button_frame = tk.Frame(root, bg="white", pady=20)
    button_frame.pack(fill=tk.X, padx=20)

    # Process Button
    process_button = tk.Button(button_frame, text="Process Input", font=button_font, bg="blue", fg="white", relief="flat", command=process_input)
    process_button.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

    # Translate Button
    translate_button = tk.Button(button_frame, text="Translate Output", font=button_font, bg="green", fg="white", relief="flat", command=translate_output)
    translate_button.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

    # Save as PDF Button
    save_pdf_button = tk.Button(button_frame, text="Save Translated Output as PDF", font=button_font, bg="red", fg="white", relief="flat", command=save_as_pdf)
    save_pdf_button.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

    # Output Display Frame
    output_frame = tk.Frame(root, bg="grey", pady=20)
    output_frame.pack(fill=tk.BOTH, expand=True, padx=20)

    # Processed Input Section
    tk.Label(output_frame, text="Processed Input:", font=label_font, bg="#F5F5F5", fg="black").grid(row=0, column=0, sticky="nw", padx=10)
    text_display = tk.Text(output_frame, wrap=tk.WORD, height=15, bg="#ECF0F1", font=("Roboto", 12), bd=2, relief="solid", padx=10, pady=10)
    text_display.grid(row=1, column=0, sticky="nsew", padx=10)

    # Translated Output Section
    tk.Label(output_frame, text="Translated Output:", font=label_font, bg="#F5F5F5", fg="black").grid(row=0, column=1, sticky="nw", padx=10)
    translated_text_display = tk.Text(output_frame, wrap=tk.WORD, height=15, bg="#ECF0F1", font=("Roboto", 12), bd=2, relief="solid", padx=10, pady=10)
    translated_text_display.grid(row=1, column=1, sticky="nsew", padx=10)
    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    run_app()
