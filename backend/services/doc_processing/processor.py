import os
import uuid
import aiofiles
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import UploadFile, HTTPException

from ...models.doc_extraction import ProcessingMetadata, JobStatus
from .file_validator import FileValidator
from .text_extractor import TextExtractor
from .docx_generator import DocxGenerator
from ...core.config import settings

class DocumentProcessor:
    def __init__(self):
        self.file_validator = FileValidator()
        self.text_extractor = TextExtractor()
        self.docx_generator = DocxGenerator()
        self.jobs: Dict[str, Dict[str, Any]] = {}  # In-memory job tracking
        
    async def process_uploaded_file(
        self,
        file: UploadFile,
        issuer_id: str,
        user_email: str,
        update_callback=None
    ) -> str:
        job_id = str(uuid.uuid4())
        
        # Initialize job tracking
        self.jobs[job_id] = {
            "status": JobStatus.QUEUED,
            "message": "Job queued for processing",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "download_url": None
        }
        
        try:
            # Update status: Validating
            await self._update_job_status(job_id, JobStatus.VALIDATING, "Validating file", update_callback)
            
            # Validate file
            file_size = file.size if hasattr(file, 'size') else 0
            self.file_validator.validate_file(file.filename, file_size)
            
            # Save uploaded file temporarily
            temp_dir = os.path.join(settings.temp_storage_path, job_id)
            os.makedirs(temp_dir, exist_ok=True)
            
            input_path = os.path.join(temp_dir, file.filename)
            async with aiofiles.open(input_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
                file_size = len(content)
            
            # Update status: Processing
            await self._update_job_status(job_id, JobStatus.PROCESSING, "Extracting text content", update_callback)
            
            # Extract text
            text_content = await self.text_extractor.extract_from_file(input_path)
            
            # Update status: Converting
            await self._update_job_status(job_id, JobStatus.CONVERTING, "Creating DOCX document", update_callback)
            
            # Create metadata
            metadata = ProcessingMetadata(
                filename=file.filename,
                file_size=file_size,
                upload_datetime=datetime.now(),
                processing_datetime=datetime.now(),
                issuer_id=issuer_id,
                user_email=user_email
            )
            
            # Generate DOCX
            doc = self.docx_generator.create_document(text_content, metadata)
            output_filename = f"{os.path.splitext(file.filename)[0]}_processed.docx"
            output_path = os.path.join(temp_dir, output_filename)
            self.docx_generator.save_document(doc, output_path)
            
            # Update status: Completed
            download_url = f"/api/v1/doc-extraction/download/{job_id}"
            await self._update_job_status(
                job_id, 
                JobStatus.COMPLETED, 
                "Processing completed successfully",
                update_callback,
                download_url=download_url
            )
            
            # Store output path for download
            self.jobs[job_id]["output_path"] = output_path
            self.jobs[job_id]["output_filename"] = output_filename
            
            return job_id
            
        except HTTPException:
            raise
        except Exception as e:
            await self._update_job_status(
                job_id, 
                JobStatus.FAILED, 
                f"Processing failed: {str(e)}",
                update_callback
            )
            raise HTTPException(status_code=500, detail=str(e))
    
    async def _update_job_status(
        self, 
        job_id: str, 
        status: JobStatus, 
        message: str,
        update_callback=None,
        download_url: Optional[str] = None
    ):
        if job_id in self.jobs:
            self.jobs[job_id]["status"] = status
            self.jobs[job_id]["message"] = message
            self.jobs[job_id]["updated_at"] = datetime.now()
            if download_url:
                self.jobs[job_id]["download_url"] = download_url
        
        if update_callback:
            await update_callback(job_id, status, message)
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        if job_id not in self.jobs:
            raise HTTPException(status_code=404, detail="Job not found")
        return self.jobs[job_id]
    
    def get_job_file(self, job_id: str) -> tuple[str, str]:
        if job_id not in self.jobs:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job = self.jobs[job_id]
        if job["status"] != JobStatus.COMPLETED:
            raise HTTPException(status_code=400, detail="Job not completed yet")
        
        if "output_path" not in job:
            raise HTTPException(status_code=404, detail="Output file not found")
        
        return job["output_path"], job["output_filename"]