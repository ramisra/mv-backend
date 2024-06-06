from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from google.cloud import storage
from fastapi import UploadFile, File

from core.models.user import User


class StorageWrapper:

    def __init__(self, bucket_name='mv_assets'):

        self.client = storage.Client.from_service_account_json(json_credentials_path='../key_test.json')
        self.bucket_name = bucket_name


    def upload_file(
        self, current_user: Optional[User], file: UploadFile
    ) -> Dict[str, Any]:

        if current_user is None:
            uid = "anonymous"
        else:
            uid = str(current_user.id)

        file_key = f"uploads/{uid}/{file.filename}"
        bucket = self.client.get_bucket(self.bucket_name)
        blob = bucket.blob(file_key)
        blob.upload_from_file(file.file)
        signed_url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(hours=1),  # URL expiration time
            method="GET"
        )

        return {"message": "File uploaded successfully", "url": signed_url}
