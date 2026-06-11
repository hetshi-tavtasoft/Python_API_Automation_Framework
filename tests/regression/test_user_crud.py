import allure
from models.response_models.user_model import UserData
from utils.validators import is_valid_email
from core.assertions import assert_status


@allure.feature("User Management")
@allure.story("Regression - User CRUD")
@allure.title("GET all users returns list")
def test_get_all_users(api_client, base_url):
    response = api_client.get("/users", base_url=base_url)
    assert_status(response, 200)
    users = response.json()
    assert isinstance(users, list)
    assert len(users) > 0


@allure.feature("User Management")
@allure.story("Regression - User CRUD")
@allure.title("PUT update existing user")
def test_update_user(api_client, base_url, load_json):
    payload = load_json("testdata/users.json")["update"]
    response = api_client.put("/users/1", payload, base_url=base_url)
    assert_status(response, 200)
    assert response.json()["name"] == payload["name"]


@allure.feature("User Management")
@allure.story("Regression - User CRUD")
@allure.title("PATCH partial update existing user")
def test_patch_user(api_client, base_url, load_json):
    payload = load_json("testdata/users.json")["patch"]
    response = api_client.patch("/users/1", payload, base_url=base_url)
    assert_status(response, 200)
    assert response.json()["job"] == payload["job"]


@allure.feature("User Management")
@allure.story("Regression - User CRUD")
@allure.title("DELETE existing user")
def test_delete_user(api_client, base_url):
    response = api_client.delete("/users/1", base_url=base_url)
    assert_status(response, 200)


@allure.feature("User Management")
@allure.story("Regression - User CRUD")
@allure.title("GET user by ID with Pydantic validation and email format")
def test_get_user_email_format(api_client, base_url):
    response = api_client.get("/users/1", base_url=base_url)
    assert_status(response, 200)
    user = UserData(**response.json())
    assert user.id == 1
    assert is_valid_email(user.email)
    assert user.address is not None
    assert user.company is not None
