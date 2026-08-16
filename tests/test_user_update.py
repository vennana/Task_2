# Тесты для обновления данных пользователя

import pytest
import allure
import requests
from config import AUTH_URL
from helpers import generate_unique_email


@allure.epic("Пользователь")
@allure.feature("Обновление данных пользователя")
class TestUserUpdate:
    
    @allure.title("Обновление данных пользователя с авторизацией")
    @allure.description("Проверка возможности обновления данных авторизованного пользователя")
    @pytest.mark.parametrize("field,new_value", [
        ("email", None),  # будет сгенерирован новый email
        ("name", "New Test User"),
    ])
    def test_update_user_authorized(self, create_and_delete_user, field, new_value):
        assert create_and_delete_user is not None, "Не удалось создать пользователя"
        
        user_data = create_and_delete_user["user_data"]
        access_token = create_and_delete_user["access_token"]
        
        if field == "email":
            new_value = generate_unique_email()
        
        update_data = {field: new_value}
        
        with allure.step(f"Отправить запрос на обновление поля {field} авторизованным пользователем"):
            response = requests.patch(
                f"{AUTH_URL}/user",
                headers={"Authorization": access_token},
                json=update_data
            )
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 200
        
        with allure.step("Проверить, что данные обновились"):
            response_data = response.json()
            assert response_data["success"] is True
            assert response_data["user"][field] == new_value
        
        # Обновляем данные пользователя для удаления
        if field == "email":
            user_data["email"] = new_value
    
    @allure.title("Обновление данных пользователя без авторизации")
    @allure.description("Проверка ошибки при обновлении данных неавторизованного пользователя")
    @pytest.mark.parametrize("field,new_value", [
        ("email", "new_email@yandex.ru"),
        ("name", "New Unauthorized User"),
    ])
    def test_update_user_unauthorized(self, create_user, field, new_value):
        assert create_user is not None, "Не удалось создать пользователя"
        
        update_data = {field: new_value}
        
        with allure.step(f"Отправить запрос на обновление поля {field} без авторизации"):
            response = requests.patch(
                f"{AUTH_URL}/user",
                json=update_data
            )
        
        with allure.step("Проверить код ответа 401 Unauthorized"):
            assert response.status_code == 401
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data["success"] is False
            assert "You should be authorised" in response_data.get("message", "")