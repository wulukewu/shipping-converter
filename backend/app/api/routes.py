from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.services.processor_service import process_file, PROCESSORS
from app.models.schemas import ProcessorResponse
from app.core.config import settings
import os

router = APIRouter()

@router.get("/processors")
async def get_processors():
    """Get list of available processors."""
    return {
        "processors": [
            {"id": key, "name": config["name"]} 
            for key, config in PROCESSORS.items()
        ]
    }

@router.post("/process/{processor_type}", response_model=ProcessorResponse)
async def process_upload(processor_type: str, file: UploadFile = File(...)):
    """Process uploaded file with specified processor."""
    result = await process_file(file, processor_type)
    return result

@router.get("/download/{filename}")
async def download_file(filename: str):
    """Download processed file."""
    filepath = os.path.join(settings.UPLOAD_FOLDER, filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Extract original base name for download
    parts = filename.split('_', 2)
    if len(parts) >= 3:
        download_name = parts[2]
    else:
        download_name = filename
    
    return FileResponse(
        path=filepath,
        filename=download_name,
        media_type='application/octet-stream'
    )
