from fastapi import APIRouter, HTTPException
from app.models.user_model import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter()
service = UserService()


@router.get("/", response_model=list[UserResponse])
def get_users():
    return service.get_all()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(payload: UserCreate):
    return service.create(payload)
