import pytest
import requests
from jsonschema import validate, ValidationError

API_URL = 'https://api.openbrewerydb.org/v1/breweries'

brewery_schema = {
    "type": "object",
    "properties": {
        "address_1": {"type": ["string", "null"]},
        "address_2": {"type": ["string", "null"]},
        "address_3": {"type": ["string", "null"]},
        "brewery_type": {"type": "string"},
        "city": {"type": "string"},
        "country": {"type": "string"},
        "id": {"type": "string"},
        "latitude": {"type": ["string", "null"]},
        "longitude": {"type": ["string", "null"]},
        "name": {"type": "string"},
        "phone": {"type": ["string", "null"]},
        "postal_code": {"type": "string"},
        "state": {"type": "string"},
        "state_province": {"type": "string"},
        "street": {"type": ["string", "null"]},
        "website_url": {"type": ["string", "null"]},
    },
    "required": [
        "brewery_type", "city", "country", "id", "latitude",
        "name", "postal_code", "state", "state_province", "website_url",
    ]
}

def get_brewery(brewery_id):
    response = requests.get(API_URL + f'/{brewery_id}')
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    return response.json()


def get_breweries_by_param(param, value):
    response = requests.get(API_URL + f'?{param}={value}')
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    return response.json()


def common_fields_test(brewery):
    try:
        validate(instance=brewery, schema=brewery_schema)
    except ValidationError as e:
        raise AssertionError(f"Validation error: {e.message}")

@pytest.fixture
def breweries():
    response = requests.get(API_URL)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    return response.json()


def test_breweries_list_api(breweries):
    for brewery in breweries:
        common_fields_test(brewery)


def test_breweries_by_id_api(breweries):
    brewery_id = breweries[0]['id']
    brewery = get_brewery(brewery_id)

    assert brewery['id'] == brewery_id
    common_fields_test(brewery)


@pytest.mark.parametrize("param,value_field", [
    ('by_city', 'city'),
    ('by_state', 'state'),
    ('by_name', 'name')
])
def test_breweries_by_param_api(breweries, param, value_field):
    value = breweries[0][value_field]
    encoded_value = value.lower().replace(" ", "_")
    breweries_by_param = get_breweries_by_param(param, encoded_value)

    for brewery in breweries_by_param:
        assert brewery[value_field] == value, f"Expected {value} for {value_field}, but got {brewery[value_field]}"
        common_fields_test(brewery)


def test_breweries_by_dist_api(breweries):
    expected_latitude = float(breweries[0]['latitude'])
    expected_longitude = float(breweries[0]['longitude'])

    response = requests.get(API_URL + f'?by_dist={expected_latitude},{expected_longitude}')
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    breweries_from_response = response.json()

    for brewery in breweries_from_response:
        common_fields_test(brewery)

        approx_tolerance = 3

        assert float(brewery['latitude']) == pytest.approx(expected_latitude, abs=approx_tolerance), \
            f"Expected latitude approximately {expected_latitude} but got {brewery['latitude']} for a brewery in the response"

        assert float(brewery['longitude']) == pytest.approx(expected_longitude, abs=approx_tolerance), \
            f"Expected longitude approximately {expected_longitude} but got {brewery['longitude']} for a brewery in the response"


def test_breweries_by_ids_api(breweries):
    expected_ids = {breweries[0]['id'], breweries[1]['id']}

    response = requests.get(API_URL + f'?by_ids={",".join(map(str, expected_ids))}')
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    returned_breweries = response.json()

    # Проверка количества вернувшихся пивоварен
    assert len(returned_breweries) == len(expected_ids), 'Number of returned breweries is incorrect'

    returned_ids = {brewery['id'] for brewery in returned_breweries}

    # Проверка на соответствие id
    assert returned_ids == expected_ids, 'Returned brewery ids do not match the expected ones'

    for brewery in returned_breweries:
        common_fields_test(brewery)

def test_breweries_by_postal_api(breweries):
    postal_full = breweries[0]['postal_code']
    postal_short = postal_full.split('-')[0]

    response_full = requests.get(API_URL + f'?by_postal={postal_full}')
    assert response_full.status_code == 200, f"Expected status code 200 but got {response_full.status_code}"
    breweries_full = response_full.json()

    response_short = requests.get(API_URL + f'?by_postal={postal_short}')
    assert response_short.status_code == 200, f"Expected status code 200 but got {response_short.status_code}"
    breweries_short = response_short.json()

    # Проверка и валидация для всех пивоварен из response_full
    for brewery in breweries_full:
        assert brewery['postal_code'] == postal_full, \
            f"Expected postal_code {postal_full} but got {brewery['postal_code']} for a brewery in breweries_full"
        common_fields_test(brewery)

    # Проверка и валидация для всех пивоварен из response_short
    for brewery in breweries_short:
        assert brewery['postal_code'].startswith(postal_short), \
            f"Expected postal_code to start with {postal_short} but got {brewery['postal_code']} for a brewery in breweries_short"
        common_fields_test(brewery)


@pytest.mark.parametrize("brewery_type", [
    "micro",
    "nano",
    "regional",
    "brewpub",
    "large",
    "planning",
    "bar",
    "contract",
    "proprietor",
    "closed"
])
def test_breweries_by_type_api(breweries, brewery_type):
    breweries_by_type = get_breweries_by_param('by_type', brewery_type)

    for brewery in breweries_by_type:
        assert brewery['brewery_type'] == brewery_type, f"Expected type {brewery_type}, but got {brewery['brewery_type']}"

        common_fields_test(brewery)

def test_breweries_by_page_api():
    response = requests.get(API_URL + f'?page=1')
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    breweries = response.json()

    # Проверка на наличие данных в ответе
    assert breweries, "API response is empty or not a list"

    for brewery in breweries:
        common_fields_test(brewery)
