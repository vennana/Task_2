# Тесты для получения заказов пользователя

import allure
import requests
from config import BASE_URL
from data import TestData


@allure.epic("Заказы")
@allure.feature("Получение заказов пользователя")
class TestUserOrders:
    
    @allure.title("Получение заказов авторизованного пользователя")
    @allure.description("Проверка получения списка заказов авторизованным пользователем")
    def test_get_user_orders_authorized(self, create_and_delete_user):

        access_token = create_and_delete_user["access_token"]
        
        with allure.step("Отправить запрос на получение заказов пользователя"):
            response = requests.get(
                f"{BASE_URL}/orders",
                headers={"Authorization": access_token}
            )
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 200
        
        with allure.step("Проверить структуру ответа"):
            response_data = response.json()
            assert response_data["success"] is True
            assert "orders" in response_data
            assert isinstance(response_data["orders"], list)
            assert "total" in response_data
            assert "totalToday" in response_data
    
    @allure.title("Получение заказов неавторизованного пользователя")
    @allure.description("Проверка ошибки при получении заказов без авторизации")
    def test_get_user_orders_unauthorized(self):
        with allure.step("Отправить запрос на получение заказов без авторизации"):
            response = requests.get(f"{BASE_URL}/orders")
        
        with allure.step("Проверить код ответа 401 Unauthorized"):
            assert response.status_code == 401
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data["success"] is False
            assert TestData.UNAUTHORIZED in response_data.get("message", "")