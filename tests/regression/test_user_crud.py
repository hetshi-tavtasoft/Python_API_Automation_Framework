import allure
from models.user_model import UserData


@allure.feature("User Management")
@allure.story("Regression - User CRUD")
@allure.title("GET all users returns list")
def test_get_all_users(api_client, base_url):
    response = api_client.get("/users", base_url=base_url)

    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) > 0


@allure.feature("User Management")
@allure.story("Regression - User CRUD")
@allure.title("PUT update existing user")
def test_update_user(api_client, base_url):
    payload = {"name": "Updated Name", "job": "Senior QA"}

    response = api_client.put("/users/1", payload, base_url=base_url)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"]


@allure.feature("User Management")
@allure.story("Regression - User CRUD")
@allure.title("PATCH partial update existing user")
def test_patch_user(api_client, base_url):
    payload = {"job": "Lead QA"}

    response = api_client.patch("/users/1", payload, base_url=base_url)

    assert response.status_code == 200
    data = response.json()
    assert data["job"] == payload["job"]


@allure.feature("User Management")
@allure.story("Regression - User CRUD")
@allure.title("DELETE existing user")
def test_delete_user(api_client, base_url):
    response = api_client.delete("/users/1", base_url=base_url)

    assert response.status_code == 200


@allure.feature("User Management")
@allure.story("Regression - User CRUD")
@allure.title("GET user by ID with Pydantic validation and email format")
def test_get_user_email_format(api_client, base_url):
    response = api_client.get("/users/1", base_url=base_url)

    assert response.status_code == 200

    user = UserData(**response.json())

    assert user.id == 1
    assert user.email is not None
    assert "@" in user.email
    assert user.address is not None
    assert user.company is not None
