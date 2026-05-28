import allure

@allure.feature("User Management")
@allure.story("Create User")
@allure.title("POST create a new user")
def test_create_user(api_client, load_json):

    payload = load_json("testdata/create_user.json")

    response = api_client.post("/posts", payload)

    assert response.status_code == 201
