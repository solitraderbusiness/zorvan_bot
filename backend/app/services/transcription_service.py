"""Audio transcription service using Whisper."""
import os
import warnings
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
            # Suppress FP16 warning on CPU
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")
                self.model = whisper.load_model(settings.WHISPER_MODEL, device="cpu")

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
        print("Note: Audio transcription on CPU may take several minutes depending on file length...")
        result = self.model.transcribe(audio_path)
        text = result["text"]

        # Save transcription
        transcription_path = os.path.join(
            settings.TRANSCRIPTION_DIR,
            Path(audio_path).stem + ".txt"
        )
        os.makedirs(settings.TRANSCRIPTION_DIR, exist_ok=True)
        with open(transcription_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Transcription completed! Saved to: {transcription_path}")
        return text, transcription_path


# Singleton instance
transcription_service = TranscriptionService()
