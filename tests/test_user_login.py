# Тесты для логина пользователя

import pytest
import allure
import requests
from config import AUTH_URL
from data import TestData


@allure.epic("Пользователь")
@allure.feature("Логин пользователя")
class TestUserLogin:
    
    @allure.title("Логин под существующим пользователем")
    @allure.description("Проверка успешного входа существующего пользователя")
    def test_login_existing_user(self, create_and_delete_user):
        assert create_and_delete_user is not None, "Не удалось создать пользователя"
        
        user_data = create_and_delete_user["user_data"]
        
        with allure.step("Отправить запрос на логин"):
            response = requests.post(
                f"{AUTH_URL}/login",
                json={
                    "email": user_data["email"],
                    "password": user_data["password"]
                }
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
    
    @allure.title("Логин с неверными учетными данными")
    @allure.description("Проверка ошибки при входе с неверным email и паролем")
    @pytest.mark.parametrize("email,password,expected_message", [
        ("invalid@email.com", "TestPassword123", TestData.INVALID_CREDENTIALS),
        ("test_user@yandex.ru", "wrongpassword", TestData.INVALID_CREDENTIALS),
        ("invalid@email.com", "wrongpassword", TestData.INVALID_CREDENTIALS),
    ])
    def test_login_invalid_credentials(self, email, password, expected_message):
        with allure.step(f"Отправить запрос на логин с данными: {email}, {password}"):
            response = requests.post(
                f"{AUTH_URL}/login",
                json={
                    "email": email,
                    "password": password
                }
            )
        
        with allure.step("Проверить код ответа 401 Unauthorized"):
            assert response.status_code == 401
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data["success"] is False
            assert expected_message in response_data["message"]