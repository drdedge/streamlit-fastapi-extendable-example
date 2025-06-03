from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal
from enum import Enum

class JobStatus(str, Enum):
    QUEUED = "queued"
    VALIDATING = "validating"
    PROCESSING = "processing"
    CONVERTING = "converting"
    SENDING_EMAIL = "sending_email"
    COMPLETED = "completed"
    FAILED = "failed"

class ExtractionRequest(BaseModel):
    issuer_id: str
    user_email: EmailStr

class S3ExtractionRequest(ExtractionRequest):
    file_path: str  # s3://bucket/path/to/file.txt

class JobResponse(BaseModel):
    job_id: str
    status: JobStatus
    message: str
    created_at: datetime
    updated_at: datetime
    download_url: Optional[str] = None

class ProcessingMetadata(BaseModel):
    filename: str
    file_size: int
    upload_datetime: datetime
    processing_datetime: datetime
    issuer_id: str
    user_email: str
    original_format: str = "txt"
    output_format: str = "docx"