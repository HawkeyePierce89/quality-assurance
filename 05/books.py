import os
import requests
import pandas
import json
import shutil

URL_CSV = 'https://raw.githubusercontent.com/konflic/examples/master/data/books.csv'
URL_JSON = 'https://raw.githubusercontent.com/konflic/examples/master/data/users.json'
RESULT_FILE_NAME = 'result.json'
TEMP_FOLDER_NAME = 'tmp'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, TEMP_FOLDER_NAME)


def download_file(url, folder_name):
    file_name = url.split("/")[-1]
    file_path = os.path.join(folder_name, file_name)

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    return file_path


def delete_temp_folder():
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)


def create_result_json():
    delete_temp_folder()

    file_csv_path = download_file(URL_CSV, TEMP_DIR)
    file_json_path = download_file(URL_JSON, TEMP_DIR)

    books = pandas.read_csv(file_csv_path)
    books = books.fillna("")

    with open(file_json_path, 'r') as f:
        users = json.load(f)

    num_books = len(books)
    num_users = len(users)

    for i in range(num_books):
        user_idx = i % num_users
        book = books.iloc[i].to_dict()

        del book['Publisher']

        # Приведение ключей к нижнему регистру
        book = {k.lower(): v for k, v in book.items()}

        if 'books' not in users[user_idx]:
            users[user_idx]['books'] = []

        users[user_idx]['books'].append(book)

    result = []
    for user in users:
        result.append({
            'name': user['name'],
            'gender': user['gender'],
            'address': user['address'],
            'age': user['age'],
            'books': user.get('books', [])
        })

    with open(os.path.join(TEMP_DIR, RESULT_FILE_NAME), 'w') as f:
        json.dump(result, f, indent=4)
