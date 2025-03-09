from pathlib import Path
import logging
from typing import List
from google.cloud import speech
from utils.gcs_utils import GCSManager

logger = logging.getLogger(__name__)

class AudioService:
    def __init__(self, upload_folder: str, allowed_extensions: set):
        self.upload_folder = Path(upload_folder)
        self.allowed_extensions = allowed_extensions
        self.speech_client = speech.SpeechClient()
        self.gcs_manager = GCSManager()

    def get_audio_files(self) -> List[Path]:
        """Get all audio files from the assets directory"""
        audio_files = [
            f for f in self.upload_folder.iterdir()
            if f.is_file() and f.suffix.lower() in self.allowed_extensions
        ]
        return sorted(audio_files, key=lambda x: x.stat().st_mtime, reverse=True)

    def allowed_file(self, filename: str) -> bool:
        """Check if file extension is allowed"""
        return Path(filename).suffix.lower() in self.allowed_extensions

    def transcribe_audio(self, audio_file_path: Path) -> str:
        """Transcribe Persian audio using Google Speech-to-Text"""
        logger.info(f"Starting transcription of {audio_file_path.name}")
        
        # Upload to GCS first
        gcs_uri = self.gcs_manager.upload_file(audio_file_path)

        # Configure the audio and recognition settings
        audio = speech.RecognitionAudio(uri=gcs_uri)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            sample_rate_hertz=48000,
            language_code="fa-IR",
            enable_automatic_punctuation=True,
            model="default",
        )

        try:
            # Use long running recognize
            logger.debug("Sending file to Google Speech-to-Text API...")
            operation = self.speech_client.long_running_recognize(config=config, audio=audio)
            
            logger.info("Waiting for operation to complete...")
            response = operation.result(timeout=90)

            # Combine all transcribed pieces
            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript + " "

            logger.info("Transcription completed successfully")
            logger.info(f"Transcription: {transcript}")
            
            # Clean up - delete the file from GCS
            self.gcs_manager.delete_file(audio_file_path.name)
            
            return transcript.strip()

        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}")
            raise 