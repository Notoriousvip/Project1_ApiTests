import httpx
from jsonschema import validate

from core.contracts import USER_DATA_SCHEME
from core.contracts import LIST_RESOURCE_SCHEME

BASE_URL = "https://reqres.in/"
LIST_USERS = "api/users?page=2"
SINGLE_USER = "api/users/2"
NOT_FOUND_USER = "api/users/23"
LIST_RESOURCE = "api/unknown"
SINGLE_RESOURCE = "api/unknown/2"
SINGLE_RESOURCE_NOT_FOUND = "api/unknown/23"
EMAIL_ENDS = "reqres.in"
AVATAR_ENDS = "-image.jpg"

def test_list_users():
    response = httpx.get(BASE_URL + LIST_USERS)
    assert response.status_code == 200
    data = response.json()['data']

    for item in data:
        validate(item, USER_DATA_SCHEME)
        assert item['email'].endswith(EMAIL_ENDS)
        assert item['avatar'].endswith(str(item['id']) + AVATAR_ENDS)

def test_single_user():
    response = httpx.get(BASE_URL + SINGLE_USER)
    assert response.status_code == 200
    data = response.json()['data']

    assert data['email'].endswith(EMAIL_ENDS)
    assert data['avatar'].endswith(str(data['id']) + AVATAR_ENDS)

def test_user_not_found():
    response = httpx.get(BASE_URL + NOT_FOUND_USER)
    assert response.status_code == 404

def test_list_resource():
    response = httpx.get(BASE_URL + LIST_RESOURCE)
    assert response.status_code == 200
    response = response.json()
    data = response['data']
    assert isinstance(response['page'], int), "Номер страницы должен быть целым числом"
    assert isinstance(data, list), "'data' должен быть списком"

    for item in data:
        validate(item, LIST_RESOURCE_SCHEME)
        assert item["year"] >= 2000, "Год должен быть 2000 или позже"
        assert item["color"].startswith("#"), "Цвет должен начинаться с #"

def test_single_resource():
    response = httpx.get(BASE_URL + SINGLE_RESOURCE)
    assert response.status_code == 200
    data = response.json()['data']
    assert isinstance(data, dict), "'data' должен быть словарем"

    assert data["year"] >= 2000, "Год должен быть 2000 или позже"
    assert data["color"].startswith("#"), "Цвет должен начинаться с #"

def test_single_resource_not_found():
    response = httpx.get(BASE_URL + SINGLE_RESOURCE_NOT_FOUND)
    assert response.status_code == 404
