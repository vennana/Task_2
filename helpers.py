# Вспомогательные функции для тестов

import random
import string
from data import TestData


def generate_unique_email():
    # Генерирует уникальный email для тестов

    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_user_{random_suffix}@yandex.ru"


def generate_user_data():
    # Генерирует данные для нового пользователя

    email = generate_unique_email()
    return {
        "email": email,
        "password": TestData.USER_PASSWORD,
        "name": TestData.USER_NAME
    }


def generate_order_data(ingredients):
    # Генерирует данные для заказа

    return {"ingredients": ingredients}


def get_auth_headers(token):
    # Возвращает заголовки с авторизацией
    
    return {"Authorization": token}