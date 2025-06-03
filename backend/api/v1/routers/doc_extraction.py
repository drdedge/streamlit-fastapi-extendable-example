from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from typing import Optional

from ....models.doc_extraction import (
    ExtractionRequest, 
    JobResponse, 
    JobStatus
)
from ....services.doc_processing.processor import DocumentProcessor

router = APIRouter()
processor = DocumentProcessor()

@router.post("/upload", response_model=JobResponse)
async def upload_document(
    file: UploadFile = File(...),
    issuer_id: str = Form(...),
    user_email: str = Form(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Upload a text file for processing"""
    try:
        # Process the file
        job_id = await processor.process_uploaded_file(
            file=file,
            issuer_id=issuer_id,
            user_email=user_email
        )
        
        # Get job status
        job_info = processor.get_job_status(job_id)
        
        return JobResponse(
            job_id=job_id,
            status=job_info["status"],
            message=job_info["message"],
            created_at=job_info["created_at"],
            updated_at=job_info["updated_at"],
            download_url=job_info.get("download_url")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{job_id}", response_model=JobResponse)
async def get_job_status(job_id: str):
    """Get the status of a processing job"""
    try:
        job_info = processor.get_job_status(job_id)
        
        return JobResponse(
            job_id=job_id,
            status=job_info["status"],
            message=job_info["message"],
            created_at=job_info["created_at"],
            updated_at=job_info["updated_at"],
            download_url=job_info.get("download_url")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{job_id}")
async def download_document(job_id: str):
    """Download the processed document"""
    try:
        file_path, filename = processor.get_job_file(job_id)
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))