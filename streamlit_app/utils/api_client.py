import requests
from typing import Optional, Dict, Any
import time

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.doc_extraction_url = f"{base_url}/api/v1/doc-extraction"
    
    def upload_file(self, file, issuer_id: str, user_email: str) -> Dict[str, Any]:
        """Upload a file for processing"""
        files = {"file": (file.name, file, file.type)}
        data = {
            "issuer_id": issuer_id,
            "user_email": user_email
        }
        
        response = requests.post(
            f"{self.doc_extraction_url}/upload",
            files=files,
            data=data
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Upload failed: {response.text}")
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get the status of a processing job"""
        response = requests.get(f"{self.doc_extraction_url}/status/{job_id}")
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get status: {response.text}")
    
    def get_download_url(self, job_id: str) -> str:
        """Get the download URL for a completed job"""
        return f"{self.base_url}/api/v1/doc-extraction/download/{job_id}"
    
    def wait_for_completion(self, job_id: str, timeout: int = 60) -> Dict[str, Any]:
        """Wait for a job to complete"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self.get_job_status(job_id)
            
            if status["status"] in ["completed", "failed"]:
                return status
            
            time.sleep(1)
        
        raise TimeoutError("Job processing timed out")