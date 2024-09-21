import os
import requests
from PyQt5.QtCore import QObject, pyqtSignal
from threading import Thread
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Model(QObject):
    """
    Manages the transcription process and data manipulation.
    """
    transcription_started = pyqtSignal()
    transcription_complete = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.current_file = None
        self.transcription = None

    def validate_audio_file(self, file_path):
        """Check if the given file is a valid audio file"""
        valid_extensions = ['.wav', '.mp3', '.mp2', '.aac', '.flac', '.m4a', '.ogg', '.opus']
        return os.path.exists(file_path) and any(file_path.lower().endswith(ext) for ext in valid_extensions)

    def reset_transcription(self):
        """Reset the current transcription state"""
        self.current_file = None
        self.transcription = None

    def perform_transcription(self, file_path):
        """Start the transcription process for the given file"""
        self.current_file = file_path
        self.transcription_started.emit()
        thread = Thread(target=self._transcribe, args=(file_path,))
        thread.start()

    def _transcribe(self, file_path):
        """Perform the actual transcription request"""
        url = "https://api.deepgram.com/v1/listen?smart_format=true&diarize=true&language=en&model=nova-2"
        headers = {
            "Authorization": f"{os.getenv('DEEPGRAM_API_KEY')}",
            "Content-Type": "audio/*"
        }


        with open(file_path, "rb") as audio_file:
            response = requests.post(url, headers=headers, data=audio_file)

        self.transcription = response.json()
        self.transcription_complete.emit(self.transcription)

    def get_formatted_transcription(self):
        """Get the formatted transcription text"""
        if not self.transcription:
            return ""
        return self.transcription['results']['channels'][0]['alternatives'][0]['paragraphs']['transcript']

    def generate_srt(self):
        """Generate SRT format subtitles from the transcription"""
        if not self.transcription:
            return ""

        words = self.transcription['results']['channels'][0]['alternatives'][0]['words']
        sentences = self.group_words_into_sentences(words)
        return self.format_srt(sentences)

    @staticmethod
    def group_words_into_sentences(words):
        """Group words into sentences based on punctuation"""
        sentences = []
        current_sentence = []
        for word in words:
            current_sentence.append(word)
            if word['punctuated_word'].endswith(('.', '!', '?')):
                sentences.append(current_sentence)
                current_sentence = []
        if current_sentence:
            sentences.append(current_sentence)
        return sentences

    @staticmethod
    def format_srt(sentences):
        """Format sentences into SRT subtitle format"""
        srt_content = ""
        for i, sentence in enumerate(sentences):
            start_time = Model.format_time(sentence[0]['start'])
            end_time = Model.format_time(sentence[-1]['end'])
            text = ' '.join(word['punctuated_word'] for word in sentence)
            srt_content += f"{i+1}\n{start_time} --> {end_time}\n{text}\n\n"
        return srt_content

    @staticmethod
    def format_time(seconds):
        """Format time in seconds to SRT time format"""
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((seconds % 1) * 1000)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{milliseconds:03d}"