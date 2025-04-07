import httpx
from jsonschema import validate
import allure
import datetime

from core.contracts import CREATED_USER_SCHEME
from core.contracts import UPDATED_USER_SCHEME

BASE_URL = "https://reqres.in/"
CREATE_USER = "api/users"
UPDATE_USER = "api/users/2"
DELETE_USER = "api/users/2"

@allure.suite('Проверка запросов данных пользователей')
@allure.title('Проверяем создание пользователя')
def test_create_user_with_name_and_job():
    body = {
        "name": "morpheus",
        "job": "leader"
    }
    with allure.step(f'Делаем запрос по адресу {BASE_URL + CREATE_USER}'):
        response = httpx.post(BASE_URL + CREATE_USER, json=body)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 201

    response_json = response.json()
    creation_date = response_json['createdAt'].replace('T', ' ')
    current_date = str(datetime.datetime.utcnow())

    with allure.step('Проверяем, что структура ответа соответствует схеме'):
        validate(response_json, CREATED_USER_SCHEME)
    with allure.step('Проверяем, что имя в ответе совпадает с отправленным'):
        assert response_json['name'] == body['name']
    with allure.step('Проверяем, что работа в ответе совпадает с отправленной'):
        assert response_json['job'] == body['job']
    with allure.step('Проверяем, что дата создания пользователя соответствует текущей'):
        assert creation_date[0:16] == current_date[0:16]


def test_create_user_without_name():
    body = {
        "job": "leader"
    }
    with allure.step(f'Делаем запрос по адресу {BASE_URL + CREATE_USER}'):
        response = httpx.post(BASE_URL + CREATE_USER, json=body)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 201

    response_json = response.json()
    creation_date = response_json['createdAt'].replace('T', ' ')
    current_date = str(datetime.datetime.utcnow())

    with allure.step('Проверяем, что структура ответа соответствует схеме'):
        validate(response_json, CREATED_USER_SCHEME)
    with allure.step('Проверяем, что работа в ответе совпадает с отправленной'):
        assert response_json['job'] == body['job']
    with allure.step('Проверяем, что дата создания пользователя соответствует текущей'):
        assert creation_date[0:16] == current_date[0:16]

def test_create_user_without_job():
    body = {
        "name": "morpheus"
    }
    with allure.step(f'Делаем запрос по адресу {BASE_URL + CREATE_USER}'):
        response = httpx.post(BASE_URL + CREATE_USER, json=body)
    with allure.step('Проверяем код ответа'):
        assert response.status_code == 201

    response_json = response.json()
    creation_date = response_json['createdAt'].replace('T', ' ')
    current_date = str(datetime.datetime.utcnow())

    with allure.step('Проверяем, что структура ответа соответствует схеме'):
        validate(response_json, CREATED_USER_SCHEME)
    with allure.step('Проверяем, что имя в ответе совпадает с отправленным'):
        assert response_json['name'] == body['name']
    with allure.step('Проверяем, что дата создания пользователя соответствует текущей'):
        assert creation_date[0:16] == current_date[0:16]


@allure.title('Проверяем обновление данных пользователя с использованием метода PUT')
def test_update_user():
    body = {
        "name": "morpheus",
        "job": "zion resident"
    }

    with allure.step(f'Делаем запрос по адресу {BASE_URL + UPDATE_USER}'):
        response = httpx.put(BASE_URL + UPDATE_USER, json=body)

    with allure.step('Проверяем код ответа'):
        assert response.status_code == 200

    response_json = response.json()

    with allure.step('Проверяем, что структура ответа соответствует схеме'):
        validate(response_json, UPDATED_USER_SCHEME)

    with allure.step('Проверяем, что имя в ответе совпадает с отправленным'):
        assert response_json['name'] == body['name']

    with allure.step('Проверяем, что работа в ответе совпадает с отправленной'):
        assert response_json['job'] == body['job']

    with allure.step('Проверяем, что дата обновления пользователя соответствует формату'):
        updated_at = response_json['updatedAt'].replace('T', ' ')
        current_date = str(datetime.datetime.utcnow())
        assert updated_at[0:16] == current_date[0:16]


@allure.title('Проверяем обновление данных пользователя с использованием метода PATCH')
def test_patch_user():
    body = {
        "name": "morpheus",
        "job": "zion resident"
    }

    with allure.step(f'Делаем запрос по адресу {BASE_URL + UPDATE_USER}'):
        response = httpx.patch(BASE_URL + UPDATE_USER, json=body)

    with allure.step('Проверяем код ответа'):
        assert response.status_code == 200

    response_json = response.json()

    with allure.step('Проверяем, что структура ответа соответствует схеме'):
        validate(response_json, UPDATED_USER_SCHEME)

    with allure.step('Проверяем, что имя в ответе совпадает с отправленным'):
        assert response_json['name'] == body['name']

    with allure.step('Проверяем, что работа в ответе совпадает с отправленной'):
        assert response_json['job'] == body['job']

    with allure.step('Проверяем, что дата обновления пользователя соответствует формату'):
        updated_at = response_json['updatedAt'].replace('T', ' ')
        current_date = str(datetime.datetime.utcnow())
        assert updated_at[0:16] == current_date[0:16]


@allure.title('Проверяем удаление пользователя')
def test_delete_user():
    with allure.step(f'Делаем запрос по адресу {BASE_URL + DELETE_USER}'):
        response = httpx.delete(BASE_URL + DELETE_USER)

    with allure.step('Проверяем код ответа'):
        assert response.status_code == 204

    with allure.step('Проверяем, что тело ответа пустое'):
        assert response.text == ""