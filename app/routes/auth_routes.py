from fastapi import APIRouter, HTTPException
from app.models.user_model import LoginRequest, TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    if payload.username == "admin" and payload.password == "admin":
        return TokenResponse(access_token="fake-token", token_type="bearer")
    raise HTTPException(status_code=401, detail="Invalid credentials")
