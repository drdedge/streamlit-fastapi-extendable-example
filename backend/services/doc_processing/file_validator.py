import os
from typing import BinaryIO
from fastapi import HTTPException
from ...core.config import settings

class FileValidator:
    def __init__(self):
        self.allowed_extensions = settings.allowed_extensions.split(',')
        self.max_file_size = settings.max_file_size_mb * 1024 * 1024  # Convert to bytes
    
    def validate_file_type(self, filename: str) -> bool:
        ext = filename.lower().split('.')[-1] if '.' in filename else ''
        if ext not in self.allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Only {', '.join(self.allowed_extensions)} files are accepted."
            )
        return True
    
    def validate_file_size(self, file_size: int) -> bool:
        if file_size > self.max_file_size:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum allowed size of {settings.max_file_size_mb}MB"
            )
        return True
    
    def validate_file(self, filename: str, file_size: int) -> bool:
        self.validate_file_type(filename)
        self.validate_file_size(file_size)
        return True