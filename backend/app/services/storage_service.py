# storage_service.py - Cloud Storage Service
#
# Business logic for file upload/download operations.

"""
Storage Service

Methods:
- upload_file(file, folder) -> str (URL)
- download_file(url) -> bytes
- delete_file(url) -> None
- generate_presigned_url(url, expiry) -> str
- validate_file_type(file, allowed_types) -> bool
- get_file_metadata(url) -> FileMetadata
"""

import os
import uuid
from typing import Optional, List
from datetime import datetime, timezone
from fastapi import UploadFile
import boto3
from botocore.exceptions import ClientError
import cloudinary
import cloudinary.uploader

from app.core.config import settings


class StorageService:
    """
    Service for cloud storage operations.
    Supports both AWS S3 and Cloudinary backends.
    """

    def __init__(self):
        self.use_cloudinary = bool(settings.cloudinary_cloud_name)
        self.use_s3 = bool(settings.aws_access_key_id)

        # Initialize Cloudinary if configured
        if self.use_cloudinary:
            cloudinary.config(
                cloud_name=settings.cloudinary_cloud_name,
                api_key=settings.cloudinary_api_key,
                api_secret=settings.cloudinary_api_secret
            )

        # Initialize S3 client if configured
        if self.use_s3:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                region_name=settings.aws_region
            )
            self.bucket_name = settings.s3_bucket_name

    async def upload_file(
        self,
        file: UploadFile,
        folder: str = "uploads"
    ) -> str:
        """
        Upload a file to cloud storage.

        Args:
            file: FastAPI UploadFile object
            folder: Target folder/path prefix

        Returns:
            URL of the uploaded file
        """
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1] if file.filename else ""
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = f"{folder}/{unique_filename}"

        # Read file content
        content = await file.read()

        if self.use_cloudinary:
            return await self._upload_to_cloudinary(content, file_path, file.content_type)
        elif self.use_s3:
            return await self._upload_to_s3(content, file_path, file.content_type)
        else:
            # Fallback: Save locally (for development)
            return await self._save_locally(content, file_path)

    async def _upload_to_cloudinary(
        self,
        content: bytes,
        file_path: str,
        content_type: Optional[str]
    ) -> str:
        """Upload to Cloudinary."""
        try:
            # Determine resource type
            resource_type = "raw"
            if content_type:
                if content_type.startswith("image/"):
                    resource_type = "image"
                elif content_type == "application/pdf":
                    resource_type = "raw"

            result = cloudinary.uploader.upload(
                content,
                public_id=file_path.replace("/", "_"),
                resource_type=resource_type,
                folder="eduproof"
            )
            return result.get("secure_url", result.get("url"))
        except Exception as e:
            raise Exception(f"Cloudinary upload failed: {str(e)}")

    async def _upload_to_s3(
        self,
        content: bytes,
        file_path: str,
        content_type: Optional[str]
    ) -> str:
        """Upload to AWS S3."""
        try:
            extra_args = {}
            if content_type:
                extra_args["ContentType"] = content_type

            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_path,
                Body=content,
                **extra_args
            )

            # Return public URL
            return f"https://{self.bucket_name}.s3.{settings.aws_region}.amazonaws.com/{file_path}"
        except ClientError as e:
            raise Exception(f"S3 upload failed: {str(e)}")

    async def _save_locally(self, content: bytes, file_path: str) -> str:
        """Save file locally (development fallback)."""
        local_path = f"uploads/{file_path}"
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        with open(local_path, "wb") as f:
            f.write(content)

        return f"/static/{file_path}"

    async def delete_file(self, file_url: str) -> bool:
        """
        Delete a file from cloud storage.

        Args:
            file_url: URL of the file to delete

        Returns:
            True if deleted successfully
        """
        try:
            if self.use_cloudinary and "cloudinary" in file_url:
                # Extract public_id from URL
                public_id = file_url.split("/")[-1].split(".")[0]
                cloudinary.uploader.destroy(public_id)
                return True
            elif self.use_s3 and "s3" in file_url:
                # Extract key from URL
                key = file_url.split(".com/")[1]
                self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
                return True
            else:
                # Local file
                local_path = file_url.replace("/static/", "uploads/")
                if os.path.exists(local_path):
                    os.remove(local_path)
                return True
        except Exception:
            return False

    def generate_presigned_url(
        self,
        file_url: str,
        expiry_seconds: int = 3600
    ) -> str:
        """
        Generate a presigned URL for temporary access.

        Args:
            file_url: Original file URL
            expiry_seconds: URL expiry time in seconds

        Returns:
            Presigned URL
        """
        if not self.use_s3:
            return file_url

        try:
            key = file_url.split(".com/")[1]
            presigned_url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': key},
                ExpiresIn=expiry_seconds
            )
            return presigned_url
        except ClientError:
            return file_url

    def validate_file_type(
        self,
        content_type: str,
        allowed_types: List[str]
    ) -> bool:
        """
        Validate file type.

        Args:
            content_type: File MIME type
            allowed_types: List of allowed MIME types

        Returns:
            True if valid
        """
        return content_type in allowed_types

    def validate_file_size(
        self,
        file_size: int,
        max_size_mb: int = 10
    ) -> bool:
        """
        Validate file size.

        Args:
            file_size: File size in bytes
            max_size_mb: Maximum allowed size in MB

        Returns:
            True if within limit
        """
        max_bytes = max_size_mb * 1024 * 1024
        return file_size <= max_bytes
