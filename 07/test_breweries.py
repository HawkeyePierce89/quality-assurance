import pytest
import requests

API_URL = 'https://api.openbrewerydb.org/v1/breweries'

def get_brewery(brewery_id):
    response = requests.get(API_URL + f'/{brewery_id}')
    return response.json()


def get_breweries_by_param(param, value):
    response = requests.get(API_URL + f'?{param}={value}')
    return response.json()


def common_fields_test(brewery):
    assert 'address_1' in brewery, 'address_1 is missing in brewery data'
    assert 'brewery_type' in brewery, 'brewery_type is missing in brewery data'
    assert 'city' in brewery, 'city is missing in brewery data'
    assert 'country' in brewery, 'country is missing in brewery data'
    assert 'id' in brewery, 'id is missing in brewery data'
    assert 'latitude' in brewery, 'latitude is missing in brewery data'
    assert 'longitude' in brewery, 'longitude is missing in brewery data'
    assert 'name' in brewery, 'name is missing in brewery data'
    assert 'phone' in brewery, 'phone is missing in brewery data'
    assert 'postal_code' in brewery, 'postal_code is missing in brewery data'
    assert 'state' in brewery, 'state is missing in brewery data'
    assert 'state_province' in brewery, 'state_province is missing in brewery data'
    assert 'street' in brewery, 'street is missing in brewery data'
    assert 'website_url' in brewery, 'website_url is missing in brewery data'


@pytest.fixture
def breweries():
    response = requests.get(API_URL)
    assert response.status_code == 200
    return response.json()


def test_breweries_list_api(breweries):
    brewery = breweries[0]
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
    brewery = get_breweries_by_param(param, encoded_value)[0]

    assert brewery[value_field] == value
    common_fields_test(brewery)

def test_breweries_by_dist_api(breweries):
    latitude = breweries[0]['latitude']
    longitude = breweries[0]['longitude']

    response = requests.get(API_URL + f'?by_dist={latitude},{longitude}')
    brewery = response.json()[0]

    common_fields_test(brewery)

def test_breweries_by_ids_api(breweries):
    ids = [breweries[0]['id'], breweries[1]['id']]

    response = requests.get(API_URL + f'?by_ids={ids[0]},{ids[1]}')
    breweries = response.json()

    for index, brewery in enumerate(breweries):
        assert brewery['id'] == ids[index], 'Brewery id is incorrect'
        common_fields_test(brewery)

def test_breweries_by_postal_api(breweries):
    postal_full = breweries[0]['postal_code']
    postal_short = postal_full.split('-')[0]

    response_full = requests.get(API_URL + f'?by_postal={postal_full}')
    brewery_full = response_full.json()[0]

    response_short = requests.get(API_URL + f'?by_postal={postal_short}')
    brewery_short = response_short.json()[0]

    common_fields_test(brewery_full)
    common_fields_test(brewery_short)


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
    brewery = response.json()[0]

    common_fields_test(brewery)
