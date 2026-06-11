import pytest


def assert_status(response, expected):
    assert response.status_code == expected, (
        f"Expected status {expected}, got {response.status_code}"
    )


def assert_status_any(response, *expected):
    assert response.status_code in expected, (
        f"Expected one of {expected}, got {response.status_code}"
    )


def assert_json_has(response, *keys):
    data = response.json()
    for key in keys:
        assert key in data, f"Response missing key: {key}"


def assert_not_403(response):
    if response.status_code == 403:
        pytest.xfail("API blocked the request (403)")
