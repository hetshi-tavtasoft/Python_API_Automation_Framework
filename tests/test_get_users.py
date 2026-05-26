def test_get_users(api):
    response = api.get("/users")

    users = response.json()

    assert response.status_code == 200
    assert len(users) > 0
    assert users[0]["name"] == "Leanne Graham"

def test_get_user_by_id(api):
    response = api.get("/users/1")

    user = response.json()

    assert response.status_code == 200
    assert user["id"] == 1
    assert user["name"] == "Leanne Graham"
