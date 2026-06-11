import pytest
import allure

@allure.feature("FakeStore Products")
@allure.story("Create Product")
@allure.title("POST create a new product")
def test_create_product(api_client, fakestore_base_url, load_json):
    payload = load_json("testdata/payloads/create_product.json")
    response = api_client.post("/products", payload, base_url=fakestore_base_url)
    if response.status_code == 403:
        pytest.xfail("FakeStore API blocked the request (403)")
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["id"] is not None
    assert data["title"] == payload["title"]
