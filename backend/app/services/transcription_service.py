"""Audio transcription service using Whisper."""
import os
from pathlib import Path
from openai import OpenAI
from app.config import settings


class TranscriptionService:
    """Service for transcribing audio files using OpenAI's Whisper API."""

    def __init__(self):
        """Initialize the transcription service."""
        self.client = None
        if settings.OPENAI_API_KEY:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def transcribe_audio(self, audio_path: str) -> tuple:
        """
        Transcribe an audio file to text using OpenAI's Whisper API.

        Args:
            audio_path: Path to the audio file

        Returns:
            Tuple of (transcribed_text, transcription_path)
        """
        if not self.client:
            raise ValueError("OpenAI API key is required for transcription. Please set OPENAI_API_KEY in .env file.")

        print(f"Transcribing audio file using OpenAI Whisper API: {audio_path}")
        print("This will take just a few seconds...")

        # Open and transcribe the audio file
        with open(audio_path, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )

        text = transcript if isinstance(transcript, str) else transcript.text

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
