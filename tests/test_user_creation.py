# Тесты для создания пользователя

import pytest
import requests
import allure
from config import AUTH_URL
from helpers import generate_user_data
from data import TestData


@allure.epic("Пользователь")
@allure.feature("Создание пользователя")
class TestUserCreation:
    
    @allure.title("Создание уникального пользователя")
    @allure.description("Проверка успешного создания нового пользователя")
    def test_create_unique_user(self, delete_user):
        user_data = generate_user_data()
        
        with allure.step("Отправить запрос на регистрацию пользователя"):
            response = requests.post(
                f"{AUTH_URL}/register",
                json=user_data
            )
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 200
        
        with allure.step("Проверить тело ответа"):
            response_data = response.json()
            assert response_data["success"] is True
            assert response_data["user"]["email"] == user_data["email"]
            assert response_data["user"]["name"] == user_data["name"]
            assert "accessToken" in response_data
            assert "refreshToken" in response_data
        
        if response.status_code == 200:
            access_token = response.json().get("accessToken")
            delete_user(user_data, access_token)
    
    @allure.title("Создание пользователя, который уже зарегистрирован")
    @allure.description("Проверка ошибки при попытке создать существующего пользователя")
    def test_create_existing_user(self, create_and_delete_user):

        user_data = create_and_delete_user["user_data"]
        
        with allure.step("Отправить повторный запрос на регистрацию того же пользователя"):
            response = requests.post(
                f"{AUTH_URL}/register",
                json=user_data
            )
        
        with allure.step("Проверить код ответа 403 Forbidden"):
            assert response.status_code == 403
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == TestData.USER_ALREADY_EXISTS
    
    @allure.title("Создание пользователя без обязательного поля")
    @allure.description("Проверка ошибки при отсутствии одного из обязательных полей")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, missing_field):
        user_data = generate_user_data()
        del user_data[missing_field]
        
        with allure.step(f"Отправить запрос на регистрацию без поля {missing_field}"):
            response = requests.post(
                f"{AUTH_URL}/register",
                json=user_data
            )
        
        with allure.step("Проверить код ответа 403 Forbidden"):
            assert response.status_code == 403
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == TestData.REQUIRED_FIELDS