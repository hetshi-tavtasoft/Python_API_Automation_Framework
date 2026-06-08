import pytest
import allure
from models.product_model import Product

@allure.feature("FakeStore Products")
@allure.story("Fetch Product")
@allure.title("GET single product by ID with Pydantic validation")
def test_get_single_product(api_client, fakestore_base_url):

    response = api_client.get("/products/1", base_url=fakestore_base_url)

    if response.status_code == 403:
        pytest.xfail("FakeStore API blocked the request (403)")

    assert response.status_code == 200

    product = Product(**response.json())

    assert product.id == 1
    assert product.title is not None
    assert product.price > 0
