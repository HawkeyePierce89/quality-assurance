import pytest
import json
import math

from books import create_result_json, delete_temp_folder, TEMP_DIR

@pytest.fixture(scope='module', autouse=True)
def prepare_and_cleanup():
    # This function should create result.json file
    create_result_json()

    yield  # this is where the testing happens

    # after tests have run, cleanup the files
    delete_temp_folder()

def test_books_distribution():
    RESULT_FILE_NAME = 'result.json'

    with open(TEMP_DIR + '/' + RESULT_FILE_NAME) as f:
        result = json.load(f)

    num_users = len(result)
    num_books = sum(len(user['books']) for user in result)

    # calculate the expected minimum and maximum number of books per user
    min_books_per_user = math.floor(num_books / num_users)
    max_books_per_user = min_books_per_user + 1

    num_users_with_max_books = num_books % num_users

    users_with_max_books = 0
    users_with_min_books = 0

    for user in result:
        num_user_books = len(user['books'])
        if num_user_books == min_books_per_user:
            users_with_min_books += 1
        elif num_user_books == max_books_per_user:
            users_with_max_books += 1
            # checking the condition that users with N+1 books have been distributed books to those with N books
            assert users_with_min_books == 0
        else:
            assert False, f"User {user['name']} has unexpected count of books: {num_user_books}"

    # checking that the number of users with max_books_per_user books matches the expected value
    assert users_with_max_books == num_users_with_max_books
    # checking that the number of users with min_books_per_user books matches the expected value
    assert users_with_min_books == num_users - num_users_with_max_books
