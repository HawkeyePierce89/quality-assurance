import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com/"


@pytest.mark.parametrize(
    "endpoint, expected_status, expected_schema",
    [
        ("posts", 200, [{"userId": int, "id": int, "title": str, "body": str}]),
        ("posts/1", 200, {"userId": int, "id": int, "title": str, "body": str}),
        ("posts/1/comments", 200, [{"postId": int, "id": int, "name": str, "email": str, "body": str}]),
        ("comments?postId=1", 200, [{"postId": int, "id": int, "name": str, "email": str, "body": str}])
    ]
)
def test_get_requests(endpoint, expected_status, expected_schema):
    response = requests.get(BASE_URL + endpoint)
    assert response.status_code == expected_status

    # Если ожидаемый ответ - это словарь
    if isinstance(expected_schema, dict):
        for key, value_type in expected_schema.items():
            assert isinstance(response.json()[key], value_type)
    # Если ожидаемый ответ - это список
    elif isinstance(expected_schema, list):
        for item in response.json():
            for schema in expected_schema:
                for key, value_type in schema.items():
                    assert isinstance(item[key], value_type)


@pytest.mark.parametrize(
    "endpoint, method, data, expected_status, expected_schema",
    [
        ("posts", "POST", {"title": "foo", "body": "bar", "userId": 1}, 201,
         {"title": str, "body": str, "userId": int, "id": int}),
        ("posts/1", "PUT", {"id": 1, "title": "foo", "body": "bar", "userId": 1}, 200,
         {"id": int, "title": str, "body": str, "userId": int}),
        ("posts/1", "PATCH", {"title": "foo"}, 200, {"userId": int, "id": int, "title": str, "body": str})
    ]
)
def test_post_put_patch_requests(endpoint, method, data, expected_status, expected_schema):
    if method == "POST":
        response = requests.post(BASE_URL + endpoint, json=data)
    elif method == "PUT":
        response = requests.put(BASE_URL + endpoint, json=data)
    else:  # PATCH
        response = requests.patch(BASE_URL + endpoint, json=data)

    assert response.status_code == expected_status

    for key, value_type in expected_schema.items():
        assert isinstance(response.json()[key], value_type)


def test_delete_request():
    response = requests.delete(BASE_URL + "posts/1")
    assert response.status_code == 200
    assert response.json() == {}
