# Тестовые данные для API Stellar Burgers

class TestData:
    # Данные для создания пользователя
    USER_EMAIL = "test_user_{}@yandex.ru"
    USER_PASSWORD = "TestPassword123"
    USER_NAME = "Test User"
    
    # Невалидные данные
    INVALID_EMAIL = "invalid@email.com"
    INVALID_PASSWORD = "wrongpassword"
    INVALID_INGREDIENT_HASH = "invalid_hash_123"
    
    # Сообщения об ошибках
    USER_ALREADY_EXISTS = "User already exists"
    REQUIRED_FIELDS = "Email, password and name are required fields"
    INVALID_CREDENTIALS = "email or password are incorrect"
    UNAUTHORIZED = "You should be authorised"
    INGREDIENTS_REQUIRED = "Ingredient ids must be provided"