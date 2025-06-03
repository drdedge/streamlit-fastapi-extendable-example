from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from .api.v1.routers import doc_extraction
from .core.config import settings

# Create temp directory if it doesn't exist
os.makedirs(settings.temp_storage_path, exist_ok=True)

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title="Multi-Service API",
        version="1.0.0",
        description="Scalable API platform supporting multiple services"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers for different services
    # Document Extraction Service
    app.include_router(
        doc_extraction.router,
        prefix="/api/v1/doc-extraction",
        tags=["document-extraction"]
    )
    
    # Future services can be added here:
    # app.include_router(
    #     image_processing.router,
    #     prefix="/api/v1/image-processing",
    #     tags=["image-processing"]
    # )
    # app.include_router(
    #     data_analytics.router,
    #     prefix="/api/v1/analytics",
    #     tags=["analytics"]
    # )
    
    @app.get("/")
    async def root():
        return {
            "message": "Multi-Service API Platform",
            "version": "1.0.0",
            "services": {
                "document_extraction": "/api/v1/doc-extraction",
                # Add more services here as they are implemented
            }
        }
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
    
    return app

# Create the app instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )