# Фикстуры для тестов API Stellar Burgers

import pytest
import requests
from config import BASE_URL, AUTH_URL
from helpers import generate_user_data

@pytest.fixture
def create_user():
    # Фикстура создает пользователя и возвращает его данные

    user_data = generate_user_data()
    
    response = requests.post(
        f"{AUTH_URL}/register",
        json=user_data
    )
    
    if response.status_code == 200:
        response_data = response.json()
        return {  # Исправлено ранее: return вместо yield
            "user_data": user_data,
            "access_token": response_data.get("accessToken", ""),
            "refresh_token": response_data.get("refreshToken", ""),
            "response": response
        }
    return None


@pytest.fixture
def delete_user():
    # Фикстура для удаления пользователя после теста

    def _delete_user(user_data, access_token):
        if access_token:
            requests.patch(
                f"{AUTH_URL}/user",
                headers={"Authorization": access_token},
                json={"email": user_data["email"]}
            )
    return _delete_user


@pytest.fixture
def create_and_delete_user(create_user, delete_user):
    # Фикстура создает пользователя, возвращает его данные и токен, и удаляет пользователя после теста

    user = create_user
    if user is None:
        return None  # Исправлено ранее: return вместо yield
    
    # Сохраняем данные для удаления
    user_data = user["user_data"]
    access_token = user["access_token"]
    
    yield user
    
    # Удаление пользователя после теста
    delete_user(user_data, access_token)


@pytest.fixture
def valid_ingredients():
    # Возвращает валидные ID ингредиентов для заказа
    
    response = requests.get(f"{BASE_URL}/ingredients")
    if response.status_code == 200:
        ingredients = response.json().get("data", [])
        if len(ingredients) >= 2:
            return [ingredients[0]["_id"], ingredients[1]["_id"]]
    return ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]