import allure
from models.response_models.user_model import UserData

@allure.feature("User Management")
@allure.story("Fetch User")
@allure.title("GET single user by ID with Pydantic validation")
def test_get_single_user(api_client):
    response = api_client.get("/users/1")
    assert response.status_code == 200
    user = UserData(**response.json())
    assert user.id == 1
    assert user.email is not None
