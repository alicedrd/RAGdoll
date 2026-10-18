from fastapi import APIRouter

router = APIRouter()

# Health check
@router.get("health", tags = ["Monitoring"])
def health_check() -> dict[str, str]:
    return {"status": "OK"}