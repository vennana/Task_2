# Тесты для создания заказов

import allure
import requests
from config import BASE_URL, AUTH_URL
from data import TestData


@allure.epic("Заказы")
@allure.feature("Создание заказов")
class TestOrders:
    
    @allure.title("Создание заказа с авторизацией")
    @allure.description("Проверка успешного создания заказа авторизованным пользователем")
    def test_create_order_authorized(self, create_and_delete_user, valid_ingredients):
        assert create_and_delete_user is not None, "Не удалось создать пользователя"
        
        access_token = create_and_delete_user["access_token"]
        order_data = {"ingredients": valid_ingredients}
        
        with allure.step("Отправить запрос на создание заказа авторизованным пользователем"):
            response = requests.post(
                f"{BASE_URL}/orders",
                headers={"Authorization": access_token},
                json=order_data
            )
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 200
        
        with allure.step("Проверить тело ответа"):
            response_data = response.json()
            assert response_data["success"] is True
            assert "name" in response_data
            assert "order" in response_data
            assert "number" in response_data["order"]
    
    @allure.title("Создание заказа без авторизации")
    @allure.description("Проверка создания заказа неавторизованным пользователем")
    def test_create_order_unauthorized(self, valid_ingredients):
        order_data = {"ingredients": valid_ingredients}
        
        with allure.step("Отправить запрос на создание заказа без авторизации"):
            response = requests.post(
                f"{BASE_URL}/orders",
                json=order_data
            )
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 200
        
        with allure.step("Проверить тело ответа (заказ создается даже без авторизации)"):
            response_data = response.json()
            assert response_data["success"] is True
            assert "name" in response_data
            assert "order" in response_data
            assert "number" in response_data["order"]
    
    @allure.title("Создание заказа с ингредиентами")
    @allure.description("Проверка создания заказа с валидными ингредиентами")
    def test_create_order_with_ingredients(self, create_and_delete_user, valid_ingredients):
        assert create_and_delete_user is not None, "Не удалось создать пользователя"
        
        access_token = create_and_delete_user["access_token"]
        order_data = {"ingredients": valid_ingredients}
        
        with allure.step("Отправить запрос на создание заказа с ингредиентами"):
            response = requests.post(
                f"{BASE_URL}/orders",
                headers={"Authorization": access_token},
                json=order_data
            )
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 200
        
        with allure.step("Проверить, что заказ создан"):
            response_data = response.json()
            assert response_data["success"] is True
            assert "order" in response_data
    
    @allure.title("Создание заказа без ингредиентов")
    @allure.description("Проверка ошибки при создании заказа без ингредиентов")
    def test_create_order_without_ingredients(self, create_and_delete_user):
        assert create_and_delete_user is not None, "Не удалось создать пользователя"
        
        access_token = create_and_delete_user["access_token"]
        order_data = {"ingredients": []}
        
        with allure.step("Отправить запрос на создание заказа без ингредиентов"):
            response = requests.post(
                f"{BASE_URL}/orders",
                headers={"Authorization": access_token},
                json=order_data
            )
        
        with allure.step("Проверить код ответа 400 Bad Request"):
            assert response.status_code == 400
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data["success"] is False
            assert TestData.INGREDIENTS_REQUIRED in response_data.get("message", "")
    
    @allure.title("Создание заказа с неверным хешем ингредиента")
    @allure.description("Проверка ошибки при создании заказа с невалидным хешем ингредиента")
    def test_create_order_invalid_ingredient(self, create_and_delete_user, valid_ingredients):
        assert create_and_delete_user is not None, "Не удалось создать пользователя"
        
        access_token = create_and_delete_user["access_token"]
        # Заменяем один ингредиент на невалидный
        invalid_ingredients = valid_ingredients.copy()
        invalid_ingredients[0] = TestData.INVALID_INGREDIENT_HASH
        
        order_data = {"ingredients": invalid_ingredients}
        
        with allure.step("Отправить запрос на создание заказа с неверным хешем ингредиента"):
            response = requests.post(
                f"{BASE_URL}/orders",
                headers={"Authorization": access_token},
                json=order_data
            )
        
        with allure.step("Проверить код ответа 500 Internal Server Error"):
            assert response.status_code == 500