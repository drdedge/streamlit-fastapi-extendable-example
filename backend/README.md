# Backend Architecture Guide

## Overview

This backend is designed as a modular, scalable API platform using FastAPI. It's structured to make adding new services quick and straightforward while maintaining clean separation of concerns.

## Architecture Layers

```
┌─────────────────┐
│   API Routes    │  ← HTTP endpoints (routers/)
├─────────────────┤
│     Models      │  ← Request/Response schemas (models/)
├─────────────────┤
│    Services     │  ← Business logic (services/)
├─────────────────┤
│      Core       │  ← Config, exceptions (core/)
└─────────────────┘
```

## Directory Structure

```
backend/
├── api/v1/routers/      # API endpoints
├── models/              # Pydantic models for validation
├── services/            # Business logic implementation
├── core/                # Shared configuration
└── static/temp/         # Temporary file storage
```

## Quick Start: Adding a New Service

### Example: Adding an Image Processing Service

#### 1. Create Models (`models/image_processing.py`)
```python
from pydantic import BaseModel
from enum import Enum

class ImageFormat(str, Enum):
    PNG = "png"
    JPEG = "jpeg"
    WEBP = "webp"

class ImageProcessRequest(BaseModel):
    resize_width: int = None
    resize_height: int = None
    output_format: ImageFormat = ImageFormat.PNG
    quality: int = 85

class ImageProcessResponse(BaseModel):
    job_id: str
    status: str
    download_url: str = None
```

#### 2. Create Service Logic (`services/image_processing/processor.py`)
```python
from PIL import Image
import uuid

class ImageProcessor:
    async def process_image(self, file, options: ImageProcessRequest):
        job_id = str(uuid.uuid4())
        # Implementation here
        return job_id
```

#### 3. Create Router (`api/v1/routers/image_processing.py`)
```python
from fastapi import APIRouter, UploadFile, File
from backend.models.image_processing import ImageProcessRequest, ImageProcessResponse
from backend.services.image_processing.processor import ImageProcessor

router = APIRouter()
processor = ImageProcessor()

@router.post("/process", response_model=ImageProcessResponse)
async def process_image(
    file: UploadFile = File(...),
    options: ImageProcessRequest = ImageProcessRequest()
):
    job_id = await processor.process_image(file, options)
    return ImageProcessResponse(
        job_id=job_id,
        status="processing"
    )
```

#### 4. Register in Main App (`main.py`)
```python
from api.v1.routers import doc_extraction, image_processing

# In create_app() function:
app.include_router(
    image_processing.router,
    prefix="/api/v1/image-processing",
    tags=["image-processing"]
)
```

That's it! Your new service is ready.

## Service Pattern

Each service should follow this pattern:

1. **Models**: Define input/output schemas
2. **Service**: Implement business logic
3. **Router**: Create API endpoints
4. **Register**: Add to main app

## Best Practices

### 1. Keep Services Independent
- Each service should be self-contained
- Avoid dependencies between services
- Use shared models sparingly

### 2. Use Async Throughout
```python
async def process_file(self, file):  # ✓ Good
def process_file(self, file):        # ✗ Avoid
```

### 3. Error Handling
```python
from fastapi import HTTPException

# In your service
if not self.validate_file(file):
    raise HTTPException(status_code=400, detail="Invalid file")
```

### 4. Status Tracking
Use the job pattern for long-running tasks:
```python
jobs = {}  # In production, use Redis or a database

async def start_job(self):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "processing"}
    return job_id
```

## Common Patterns

### File Upload Endpoint
```python
@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user_id: str = Form(...)
):
    # Validate
    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(400, "Invalid file type")
    
    # Process
    result = await service.process(file)
    return {"status": "success", "data": result}
```

### Background Tasks
```python
from fastapi import BackgroundTasks

@router.post("/process")
async def process_with_notification(
    file: UploadFile,
    background_tasks: BackgroundTasks
):
    job_id = await service.process(file)
    background_tasks.add_task(send_email_notification, job_id)
    return {"job_id": job_id}
```

### Pagination
```python
@router.get("/items")
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    items = await service.get_items(skip, limit)
    return {"items": items, "skip": skip, "limit": limit}
```

## Testing Your Service

```python
# tests/test_image_processing.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_upload_image():
    with open("test.png", "rb") as f:
        response = client.post(
            "/api/v1/image-processing/process",
            files={"file": ("test.png", f, "image/png")}
        )
    assert response.status_code == 200
    assert "job_id" in response.json()
```

## Configuration

Use `core/config.py` for service-specific settings:
```python
# In core/config.py
class Settings(BaseSettings):
    # Existing settings...
    
    # Image processing settings
    max_image_size_mb: int = 50
    allowed_image_formats: str = "png,jpg,jpeg,webp"
    image_quality_default: int = 85
```

## Debugging Tips

1. **Check logs**: FastAPI logs all requests
2. **Test endpoints**: Visit `/docs` for interactive API docs
3. **Validate models**: Pydantic will show clear error messages
4. **Use debugger**: Set breakpoints in your service logic

## Production Considerations

When deploying:

1. **Replace in-memory storage**: Use Redis or a database for job tracking
2. **Add authentication**: Implement API keys or OAuth
3. **Set up monitoring**: Use tools like Sentry or DataDog
4. **Configure CORS**: Update allowed origins in main.py
5. **Use environment variables**: Never hardcode secrets

## Need Help?

- FastAPI Docs: https://fastapi.tiangolo.com/
- Check existing services for examples
- The document extraction service is a complete reference implementation