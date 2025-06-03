# Project Structure

This project demonstrates a scalable multi-service API platform using FastAPI and Streamlit.

## Directory Structure

```
streamlit-fastapi-extendable-example/
├── requirements.txt                 # Python dependencies
├── .env                            # Environment configuration (optional)
├── README.md                       # Main documentation
├── PROJECT_STRUCTURE.md            # This file
├── .gitignore                      # Git ignore rules
│
├── backend/                        # Backend module (FastAPI)
│   ├── main.py                     # FastAPI application entry point
│   ├── __init__.py
│   ├── api/                        # API layer
│   │   ├── __init__.py
│   │   └── v1/                     # API version 1
│   │       ├── __init__.py
│   │       └── routers/            # Service routers
│   │           ├── __init__.py
│   │           └── doc_extraction.py    # Document extraction endpoints
│   │
│   ├── core/                       # Core configuration and utilities
│   │   ├── __init__.py
│   │   └── config.py              # Settings management
│   │
│   ├── models/                     # Pydantic models
│   │   ├── __init__.py
│   │   └── doc_extraction.py      # Models for document extraction
│   │
│   ├── services/                   # Business logic layer
│   │   ├── __init__.py
│   │   └── doc_processing/        # Document processing service
│   │       ├── __init__.py
│   │       ├── file_validator.py  # File type and size validation
│   │       ├── text_extractor.py  # Text content extraction
│   │       ├── docx_generator.py  # Word document generation
│   │       └── processor.py       # Main processing orchestrator
│   │
│   └── static/                    # Static files
│       └── temp/                  # Temporary file storage
│
└── streamlit_app/                 # Frontend application (Streamlit)
    ├── __init__.py
    ├── app.py                     # Main Streamlit application
    └── utils/                     # Frontend utilities
        ├── __init__.py
        └── api_client.py         # API communication helper
```

## Key Design Decisions

### 1. **Separation of Concerns**
- Frontend (Streamlit) and Backend (FastAPI) are completely separate
- Each backend service is self-contained in its own directory
- Clear layering: Routes → Models → Services

### 2. **Scalability**
- API versioning built-in (`/api/v1/`)
- Service-based architecture allows easy addition of new features
- Each service has its own models, routes, and business logic

### 3. **Import Structure**
- Backend uses relative imports for portability
- Frontend uses simple imports relative to streamlit_app directory
- Main app entry point in `backend/main.py`

## Adding New Services

To add a new service (e.g., image processing):

1. **Create service directory**: `backend/services/image_processing/`
2. **Add models**: `backend/models/image_processing.py`
3. **Create router**: `backend/api/v1/routers/image_processing.py`
4. **Register in main.py**: Add the router to the FastAPI app

Example structure for a new service:
```
backend/
├── models/
│   └── image_processing.py       # New models
├── services/
│   └── image_processing/         # New service
│       ├── __init__.py
│       ├── validator.py
│       └── processor.py
└── api/v1/routers/
    └── image_processing.py       # New endpoints
```

## File Flow

1. **User uploads file** → Streamlit frontend
2. **API call** → FastAPI backend (`/api/v1/doc-extraction/upload`)
3. **Validation** → `file_validator.py`
4. **Processing** → `processor.py` orchestrates the flow
5. **Text extraction** → `text_extractor.py`
6. **Document generation** → `docx_generator.py`
7. **Response** → Job ID and status
8. **Download** → Processed file

## Running the Application

```bash
# Terminal 1 - Backend
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
streamlit run streamlit_app/app.py
```

## Development Tips

1. **API Documentation**: Visit http://localhost:8000/docs for interactive API docs
2. **Hot Reload**: Both backend and frontend auto-reload on code changes
3. **Testing**: Add tests in a `tests/` directory at the project root
4. **Logging**: Use Python's logging module for debugging

## Environment Variables

Key settings in `.env`:
- `API_HOST`: Backend host (default: 0.0.0.0)
- `API_PORT`: Backend port (default: 8000)
- `MAX_FILE_SIZE_MB`: Maximum upload size (default: 10)
- `TEMP_STORAGE_PATH`: Where to store temporary files