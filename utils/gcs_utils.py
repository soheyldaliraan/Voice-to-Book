from google.cloud import storage
from pathlib import Path
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class GCSManager:
    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket_name = os.getenv('GCS_BUCKET_NAME')
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Ensure the bucket exists, create if it doesn't"""
        try:
            self.bucket = self.storage_client.get_bucket(self.bucket_name)
        except Exception:
            logger.info(f"Creating bucket: {self.bucket_name}")
            self.bucket = self.storage_client.create_bucket(self.bucket_name)

    def upload_file(self, file_path: Path, destination_folder: str = "audio") -> str:
        """Upload file to Google Cloud Storage and return URI"""
        blob_name = f"{destination_folder}/{file_path.name}"
        blob = self.bucket.blob(blob_name)
        
        with open(file_path, "rb") as file:
            blob.upload_from_file(file)
            
        gcs_uri = f"gs://{self.bucket_name}/{blob_name}"
        logger.info(f"Uploaded file to {gcs_uri}")
        return gcs_uri

    def delete_file(self, file_name: str, folder: str = "audio"):
        """Delete file from Google Cloud Storage"""
        blob_path = f"{folder}/{file_name}"
        blob = self.bucket.blob(blob_path)
        try:
            blob.delete()
            logger.info(f"Deleted file: {blob_path}")
        except Exception as e:
            logger.error(f"Error deleting file {blob_path}: {str(e)}") 