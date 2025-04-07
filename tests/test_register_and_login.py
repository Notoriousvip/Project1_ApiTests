import json
import httpx
import pytest
from jsonschema import validate

from core.contracts import REGISTERED_USER_SCHEME
from core.contracts import LOGIN_USER_SCHEME
from core.contracts import LOGIN_ERROR_SCHEME

BASE_URL = "https://reqres.in/"
REGISTER_USER = "api/register"
LOGIN_USER = "api/login"
json_file = open('/Users/eva/PycharmProjects/Project1_ApiTests/core/new_users_data.json')
json_file2 = open('/Users/eva/PycharmProjects/Project1_ApiTests/core/login_users_data.json')
json_file3 = open('/Users/eva/PycharmProjects/Project1_ApiTests/core/login_users_data_unsuccessful.json')
users_data = json.load(json_file)
login_data = json.load(json_file2)
login_without_password = json.load(json_file3)

@pytest.mark.parametrize('users_data', users_data)
def test_successful_register(users_data):
    response = httpx.post(BASE_URL + REGISTER_USER, json = users_data)
    assert response.status_code == 200

    validate(response.json(), REGISTERED_USER_SCHEME)


@pytest.mark.parametrize('login_data', login_data)
def test_successful_login(login_data):
    response = httpx.post(BASE_URL + LOGIN_USER, json=login_data)
    assert response.status_code == 200

    validate(response.json(), LOGIN_USER_SCHEME)

@pytest.mark.parametrize('login_without_password', login_without_password)
def test_unsuccessful_login(login_without_password):
    response = httpx.post(BASE_URL + LOGIN_USER, json=login_without_password)
    assert response.status_code == 400
    assert response.json().get("error") == "Missing password"

    validate(response.json(), LOGIN_ERROR_SCHEME)


