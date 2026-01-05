"""Audio transcription service using Whisper."""
import os
import whisper
from pathlib import Path
from app.config import settings


class TranscriptionService:
    """Service for transcribing audio files."""

    def __init__(self):
        """Initialize the transcription service."""
        self.model = None

    def load_model(self):
        """Load the Whisper model."""
        if self.model is None:
            print(f"Loading Whisper model: {settings.WHISPER_MODEL}")
            self.model = whisper.load_model(settings.WHISPER_MODEL)

    def transcribe_audio(self, audio_path: str) -> str:
        """
        Transcribe an audio file to text.

        Args:
            audio_path: Path to the audio file

        Returns:
            Transcribed text
        """
        self.load_model()

        print(f"Transcribing audio file: {audio_path}")
        result = self.model.transcribe(audio_path)
        text = result["text"]

        # Save transcription
        transcription_path = os.path.join(
            settings.TRANSCRIPTION_DIR,
            Path(audio_path).stem + ".txt"
        )
        with open(transcription_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Transcription saved to: {transcription_path}")
        return text, transcription_path


# Singleton instance
transcription_service = TranscriptionService()
