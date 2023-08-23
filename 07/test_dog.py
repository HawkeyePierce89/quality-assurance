import pytest
import requests

API = 'https://dog.ceo/api'


def get_api_response(api_url):
    response = requests.get(api_url)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "message" in data
    return data


@pytest.mark.list_breeds
def test_list_all_breeds_api():
    data = get_api_response(API + '/breeds/list/all')
    assert isinstance(data["message"], dict)


@pytest.mark.list_breeds
def test_list_breed_hound_api():
    data = get_api_response(API + '/breed/hound/list')
    assert isinstance(data["message"], list)
    assert all(isinstance(breed, str) for breed in data["message"])


@pytest.mark.list_images
@pytest.mark.parametrize('api_url', [
    API + '/breed/hound/images',
    API + '/breed/hound/afghan/images'
])
def test_list_images_api(api_url):
    data = get_api_response(api_url)
    assert isinstance(data["message"], list)
    assert all(url.startswith("https://images.dog.ceo/breeds/hound") for url in data["message"])


@pytest.mark.random_image
@pytest.mark.parametrize('api_url', [
    API + '/breeds/image/random',
    API + '/breed/hound/images/random',
    API + '/breed/hound/afghan/images/random'
])
def test_random_image_api(api_url):
    data = get_api_response(api_url)
    assert data["message"].startswith("https://images.dog.ceo")


@pytest.mark.random_valid_images
@pytest.mark.parametrize('random_number', [1, 25, 50])
@pytest.mark.parametrize('url_pattern', [
    API + '/breeds/image/random',
    API + '/breed/hound/images/random',
    API + '/breed/hound/afghan/images/random'
])
def test_random_valid_N_images_api(random_number, url_pattern):
    data = get_api_response(f'{url_pattern}/{random_number}')
    assert isinstance(data["message"], list)
    assert len(data["message"]) <= random_number
    assert all(url.startswith("https://images.dog.ceo") for url in data["message"])


@pytest.mark.random_invalid_images
@pytest.mark.parametrize('random_number', [-1, 0, 51, "a", None])
@pytest.mark.parametrize('url_pattern', [
    API + '/breeds/image/random',
    API + '/breed/hound/images/random',
    API + '/breed/hound/afghan/images/random'
])
def test_random_invalid_N_images_api(random_number, url_pattern):
    response = requests.get(f'{url_pattern}/{random_number}')
    if response.status_code != 400:
        pytest.xfail("API should return 400 for invalid values but it does not. API needs to be fixed.")
    assert response.status_code == 400
