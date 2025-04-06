import httpx
from jsonschema import validate
import allure

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

@allure.suite('Проверка запросов данных пользователей')
@allure.title('Проверяем получение списка пользователей')
def test_list_users():
    with allure.step(f'Делаем запрос по адресу {BASE_URL + LIST_USERS}'):
        response = httpx.get(BASE_URL + LIST_USERS)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 200
    data = response.json()['data']

    for item in data:
        with allure.step('Проверяем элемент из списка'):
            validate(item, USER_DATA_SCHEME)
            with allure.step('Проверяем окончание Email адреса'):
                assert item['email'].endswith(EMAIL_ENDS)
            with allure.step('Проверяем наличие id в ссылке на аватарку'):
                assert item['avatar'].endswith(str(item['id']) + AVATAR_ENDS)

@allure.title('Проверяем получение данных одного пользователя')
def test_single_user():
    with allure.step(f'Делаем запрос по адресу {BASE_URL + SINGLE_USER}'):
        response = httpx.get(BASE_URL + SINGLE_USER)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 200
    data = response.json()['data']

    with allure.step('Проверяем окончание Email адреса'):
        assert data['email'].endswith(EMAIL_ENDS)
    with allure.step('Проверяем наличие id в ссылке на аватарку'):
        assert data['avatar'].endswith(str(data['id']) + AVATAR_ENDS)

@allure.title('Проверяем, что пользователь не найден')
def test_user_not_found():
    with allure.step(f'Делаем запрос по адресу {BASE_URL + NOT_FOUND_USER}'):
        response = httpx.get(BASE_URL + NOT_FOUND_USER)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 404

@allure.title('Проверяем получение списка ресурсов')
def test_list_resource():
    with allure.step(f'Делаем запрос по адресу {BASE_URL + LIST_RESOURCE}'):
        response = httpx.get(BASE_URL + LIST_RESOURCE)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 200
    response = response.json()
    data = response['data']
    with allure.step('Проверяем формат номера страницы'):
        assert isinstance(response['page'], int), "Номер страницы должен быть целым числом"
    with allure.step('Проверяем, что data является списком'):
        assert isinstance(data, list), "'data' должен быть списком"

    for item in data:
        with allure.step('Проверяем элемент из списка ресурса'):
            validate(item, LIST_RESOURCE_SCHEME)
        with allure.step('Проверяем актуальность года'):
            assert item["year"] >= 2000, "Год должен быть 2000 или позже"
        with allure.step('Проверяем корректность названия цвета'):
            assert item["color"].startswith("#"), "Цвет должен начинаться с #"

@allure.title('Проверяем получение данных одного ресурса')
def test_single_resource():
    with allure.step(f'Делаем запрос по адресу {BASE_URL + SINGLE_RESOURCE}'):
        response = httpx.get(BASE_URL + SINGLE_RESOURCE)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 200
    data = response.json()['data']
    with allure.step('Проверяем, что data является словарем'):
        assert isinstance(data, dict), "'data' должен быть словарем"
    with allure.step('Проверяем актуальность года'):
        assert data["year"] >= 2000, "Год должен быть 2000 или позже"
    with allure.step('Проверяем корректность названия цвета'):
        assert data["color"].startswith("#"), "Цвет должен начинаться с #"

@allure.title('Проверяем, что ресурс не найден')
def test_single_resource_not_found():
    with allure.step(f'Делаем запрос по адресу {BASE_URL + SINGLE_RESOURCE_NOT_FOUND}'):
        response = httpx.get(BASE_URL + SINGLE_RESOURCE_NOT_FOUND)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 404
