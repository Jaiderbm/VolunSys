from fastapi import APIRouter
from app.controllers.auth_controller import login

router = APIRouter()

@router.post("/login")
def login_route(data: dict):
    return login(data)