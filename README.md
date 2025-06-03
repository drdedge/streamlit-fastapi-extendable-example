# Streamlit FastAPI Extendable Example

A scalable web application template combining Streamlit (frontend) and FastAPI (backend) for document processing services. This architecture is designed to be easily extended with additional services.

## Features

- **Document Processing**: Convert text files to formatted Word documents with metadata
- **Modular Architecture**: Easy to add new services and endpoints
- **Real-time Status Updates**: Track processing progress
- **Clean Separation**: Frontend and backend are clearly separated
- **Type Safety**: Full Pydantic model validation
- **Async Processing**: Built for performance with async/await

## Project Structure

```
├── backend/                 # FastAPI backend
│   ├── main.py             # Application entry point
│   ├── api/                # API endpoints
│   ├── models/             # Pydantic models
│   ├── services/           # Business logic
│   └── core/               # Configuration
├── streamlit_app/          # Streamlit frontend
│   ├── app.py              # Main application
│   └── utils/              # Utilities
└── requirements.txt        # Python dependencies
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/drdedge/streamlit-fastapi-extendable-example.git
cd streamlit-fastapi-extendable-example
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Start the Backend (FastAPI)

From the project root directory:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs

### Start the Frontend (Streamlit)

In a new terminal (with virtual environment activated):

```bash
streamlit run streamlit_app/app.py
```

The Streamlit app will open in your browser at http://localhost:8501

## Usage

1. Open the Streamlit app in your browser
2. Upload a file (currently supports .txt files)
3. Enter your Issuer ID and email address
4. Click "Process Document"
5. Wait for processing to complete
6. Download the generated DOCX file

## Extending the Application

To add a new service (e.g., PDF processing):

1. Create models in `backend/models/your_service.py`
2. Implement logic in `backend/services/your_service/`
3. Add routes in `backend/api/v1/routers/your_service.py`
4. Register in `backend/main.py`

See `backend/README.md` for detailed instructions.

## Development

- Backend runs with auto-reload enabled
- Frontend updates automatically when you save files
- Check API documentation at http://localhost:8000/docs

## Environment Variables

Create a `.env` file in the project root (optional):

```env
API_HOST=0.0.0.0
API_PORT=8000
MAX_FILE_SIZE_MB=10
```

## License

MIT License - feel free to use this template for your projects!