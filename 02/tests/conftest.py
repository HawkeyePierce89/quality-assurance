import pytest as pytest


@pytest.fixture(scope='session')
def start_db():
    print("start db")
    yield
    print("stop db")

@pytest.fixture(scope='session')
def start_stop_rest_service(start_db):
    print("start rest")
    yield 'container_name:8080'
    print("stop rest")
