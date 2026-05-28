from app.database.fake_db import fake_users_db
from app.models.user_model import UserCreate, UserResponse


class UserService:

    def get_all(self) -> list[UserResponse]:
        return [UserResponse(**u) for u in fake_users_db.values()]

    def get_by_id(self, user_id: int) -> UserResponse | None:
        user = fake_users_db.get(user_id)
        return UserResponse(**user) if user else None

    def create(self, payload: UserCreate) -> UserResponse:
        new_id = max(fake_users_db.keys()) + 1
        user = {"id": new_id, **payload.model_dump()}
        fake_users_db[new_id] = user
        return UserResponse(**user)
