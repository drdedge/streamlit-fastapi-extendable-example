from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_version: str = "v1"
    
    # File Processing
    max_file_size_mb: int = 10
    allowed_extensions: str = "txt"
    temp_storage_path: str = "./static/temp"
    download_expiry_hours: int = 24
    
    # Integrations (Placeholders)
    sendgrid_api_key: Optional[str] = "placeholder_key"
    sendgrid_from_email: Optional[str] = "noreply@example.com"
    aws_access_key_id: Optional[str] = "placeholder_key"
    aws_secret_access_key: Optional[str] = "placeholder_secret"
    aws_bucket_name: Optional[str] = "placeholder_bucket"
    aws_region: Optional[str] = "us-east-1"
    
    # WebSocket
    ws_heartbeat_interval: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()