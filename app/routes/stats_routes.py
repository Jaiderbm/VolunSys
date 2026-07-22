from fastapi import APIRouter
from app.controllers.stats_controller import get_dashboard_stats

router = APIRouter()

@router.get("/stats")
def read_stats():
    return get_dashboard_stats()
