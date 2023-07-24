import os
import requests
import pandas
import json
import shutil

URL_CSV = 'https://raw.githubusercontent.com/konflic/examples/master/data/books.csv'
URL_JSON = 'https://raw.githubusercontent.com/konflic/examples/master/data/users.json'
RESULT_FILE_NAME = 'result.json'
TEMP_FOLDER_NAME = 'tmp'


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


def delete_folder_if_exists(folder_name):
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)


delete_folder_if_exists(TEMP_FOLDER_NAME)

file_csv_path = download_file(URL_CSV, TEMP_FOLDER_NAME)
file_json_path = download_file(URL_JSON, TEMP_FOLDER_NAME)

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

with open(TEMP_FOLDER_NAME + '/' + RESULT_FILE_NAME, 'w') as f:
    json.dump(result, f, indent=4)

os.remove(file_csv_path)
os.remove(file_json_path)
