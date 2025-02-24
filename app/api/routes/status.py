from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SyncSessionLocal
from app.models import ProcessingRequest

router = APIRouter()

@router.get("/{request_id}", summary="Check processing status")
async def check_status(request_id: str):
    """Check the processing status of a request"""

    db = SyncSessionLocal()
    request = db.query(ProcessingRequest).filter_by(request_id=request_id).first()
    db.close()

    if not request:
        raise HTTPException(status_code=404, detail="Request ID not found")

    return {"request_id": request_id, "status": request.status}