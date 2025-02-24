from fastapi import APIRouter

router = APIRouter()

@router.get("/", summary="Health check endpoint")
async def health_check():
    """Returns a simple health status."""
    return {"status": "OK"}
