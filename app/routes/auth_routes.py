from fastapi import APIRouter, HTTPException
from app.controllers.auth_controller import login_user

router = APIRouter()


@router.post("/login")
def login(data: dict):

    result = login_user(
        data["correo"],
        data["password"]
    )

    if "error" in result:
        raise HTTPException(status_code=401, detail=result["error"])

    return result
