import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com/"


# Тесты для GET запросов с ожидаемым ответом в виде словаря
@pytest.mark.parametrize(
    "endpoint, expected_status, expected_schema",
    [
        ("posts/1", 200, {"userId": int, "id": int, "title": str, "body": str}),
    ]
)
def test_get_requests_dict(endpoint, expected_status, expected_schema):
    response = requests.get(BASE_URL + endpoint)
    assert response.status_code == expected_status

    for key, value_type in expected_schema.items():
        assert isinstance(response.json()[key], value_type)

# Тесты для GET запросов с ожидаемым ответом в виде списка
@pytest.mark.parametrize(
    "endpoint, expected_status, expected_schema",
    [
        ("posts", 200, [{"userId": int, "id": int, "title": str, "body": str}]),
        ("posts/1/comments", 200, [{"postId": int, "id": int, "name": str, "email": str, "body": str}]),
        ("comments?postId=1", 200, [{"postId": int, "id": int, "name": str, "email": str, "body": str}])
    ]
)
def test_get_requests_list(endpoint, expected_status, expected_schema):
    response = requests.get(BASE_URL + endpoint)
    assert response.status_code == expected_status

    schema = expected_schema[0]
    assert all(
        isinstance(item[key], value_type) for item in response.json() for key,
        value_type in schema.items()
    )

@pytest.mark.parametrize(
    "endpoint, method, data, expected_status, expected_schema",
    [
        ("posts", requests.post, {"title": "foo", "body": "bar", "userId": 1}, 201,
         {"title": str, "body": str, "userId": int, "id": int}),
        ("posts/1", requests.put, {"id": 1, "title": "foo", "body": "bar", "userId": 1}, 200,
         {"id": int,  "title": str, "body": str, "userId": int}),
        ("posts/1", requests.patch, {"title": "foo"}, 200, {"userId": int, "id": int, "title": str, "body": str})
    ]
)
def test_post_put_patch_requests(endpoint, method, data, expected_status, expected_schema):
    response = method(BASE_URL + endpoint, json=data)
    assert response.status_code == expected_status

    check_json_schema(response, expected_schema)


def check_json_schema(response, expected_schema):
    for key, value_type in expected_schema.items():
        assert isinstance(response.json()[key], value_type)


def test_delete_request():
    response = requests.delete(BASE_URL + "posts/1")
    assert response.status_code == 200
    assert response.json() == {}
