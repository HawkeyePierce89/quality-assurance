import pytest
import requests

API = 'https://dog.ceo/api'


@pytest.mark.list_breeds
def test_list_all_breeds_api():
    response = requests.get(API + '/breeds/list/all')
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "message" in data
    assert isinstance(data["message"], dict)


@pytest.mark.list_breeds
def test_list_breed_hound_api():
    response = requests.get(API + '/breed/hound/list')
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "message" in data
    assert isinstance(data["message"], list)
    assert all(isinstance(breed, str) for breed in data["message"])


@pytest.mark.list_images
@pytest.mark.parametrize('api_url', [
    API + '/breed/hound/images',
    API + '/breed/hound/afghan/images'
])
def test_list_images_api(api_url):
    response = requests.get(api_url)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "message" in data
    assert isinstance(data["message"], list)
    assert all(url.startswith("https://images.dog.ceo/breeds/hound") for url in data["message"])


@pytest.mark.random_image
@pytest.mark.parametrize('api_url', [
    API + '/breeds/image/random',
    API + '/breed/hound/images/random',
    API + '/breed/hound/afghan/images/random'
])
def test_random_image_api(api_url):
    response = requests.get(api_url)
    data = response.json()
    assert response.status_code == 200
    assert data["status"] == "success"
    assert "message" in data
    assert data["message"].startswith("https://images.dog.ceo")


@pytest.mark.random_N_images
@pytest.mark.parametrize('N', [-1, 0, 1, 25, 50, 51, "a", None])
@pytest.mark.parametrize('url_pattern', [
    API + '/breeds/image/random',
    API + '/breed/hound/images/random',
    API + '/breed/hound/afghan/images/random'
])
def test_random_N_images_api(N, url_pattern):
    response = requests.get(f'{url_pattern}/{N}')
    if isinstance(N, int) and 1 <= N <= 50:
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "message" in data
        assert isinstance(data["message"], list)
        assert len(data["message"]) <= N
        assert all(url.startswith("https://images.dog.ceo") for url in data["message"])
    else:
        if response.status_code != 400:
            pytest.xfail("API should return 400 for invalid values but it does not. API needs to be fixed.")
        assert response.status_code == 400
