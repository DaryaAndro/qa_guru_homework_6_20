import os
import json
import requests
from jsonschema.validators import validate

from tests.conftest import resources_path


def test_get_list_users_schema():
    with open(os.path.join(resources_path, 'get_list_users_schema.json')) as file:
        schema = json.loads(file.read())

    response = requests.get('https://reqres.in/api/users')
    validate(response.json(), schema)


def test_get_single_user_schema():
    with open(os.path.join(resources_path, 'get_single_user_schema.json')) as file:
        schema = json.loads(file.read())

    response = requests.get('https://reqres.in/api/users/1')
    validate(response.json(), schema)


def test_get_single_user_not_found():
    response = requests.get(
        url='https://reqres.in/api/users/44')

    assert response.status_code == 404


def test_get_list_users_page():
    page = 1
    per_page = 6
    total = 12

    response = requests.get(
        url='https://reqres.in/api/users',
        params={'page': page}
    )

    assert response.status_code == 200
    assert response.json()['page'] == 1
    assert response.json()['per_page'] == per_page
    assert len(response.json()['data']) == per_page
    assert response.json()['total'] == total


def test_first_user_on_page_2():
    page = 2

    response = requests.get(url='https://reqres.in/api/users',
                            params={'page': page})

    assert response.json()['data'][0]['id'] == 7
    assert response.json()['data'][0]['email'] == 'michael.lawson@reqres.in'


def test_page_2_per_page_3():
    page = 3

    response = requests.get(url='https://reqres.in/api/users',
                            params={'page': page})

    assert response.json()['page'] == 3
    assert response.json()['total_pages'] == 2
    assert len(response.json()['data']) == 0


def test_post_create_user():
    name = 'Dasha'
    job = 'QA'
    response = requests.post(url='https://reqres.in/api/users/1',
                             data={'name': name, 'job': job})

    assert response.status_code == 201
    assert response.json()['name'] == name
    assert response.json()['job'] == job


def test_put_update_user():
    name = 'Dasha'
    job = 'QA manual'

    response = requests.put(url='https://reqres.in/api/users/2',
                            data={'name': name, 'job': job})

    assert response.status_code == 200
    assert response.json()['name'] == name
    assert response.json()['job'] == job


def test_delete_user():
    response = requests.delete(url='https://reqres.in/api/users/2')

    assert response.status_code == 204


def test_post_register_successful():
    email = 'eve.holt@reqres.in'
    password = 'pistol'

    response = requests.post(url='https://reqres.in/api/register',
                             data={'email': email, 'password': password})

    assert response.status_code == 200
    assert response.json()['token'] is not None


def test_post_register_unsuccessful():
    email = 'sydney@fife'

    response = requests.post(url='https://reqres.in/api/register',
                             data={'email': email, 'password': ''})

    assert response.status_code == 400
    assert response.json()['error'] == 'Missing password'
