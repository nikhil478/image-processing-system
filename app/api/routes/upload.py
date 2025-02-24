
from fastapi import APIRouter, UploadFile, File, BackgroundTasks
import uuid
import shutil
import os
from app.core.database import SyncSessionLocal
from app.models.processing_request import ProcessingRequest
from app.workers.tasks import process_csv
import time


router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/", summary="Upload CSV for image processing")
async def upload_csv(file: UploadFile = File(...)):
    """Upload a CSV file, save it, and enqueue a Celery task for processing"""

    request_id = str(uuid.uuid4())

    db = SyncSessionLocal()
    new_request = ProcessingRequest(request_id=request_id, status="PENDING")
    db.add(new_request)
    db.commit()
    db.close()

    file_path = os.path.join(UPLOAD_FOLDER, f"{request_id}.csv")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    process_csv.apply_async(args=[request_id, file_path])  # Pass file path

    return {"message": "File uploaded successfully", "request_id": request_id}
