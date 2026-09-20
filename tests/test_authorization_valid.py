import allure
import pytest

from pages.main_page import MainPage
from pages.login_page import LoginPage


@allure.title("Тест авторизации валидного пользователя: {user}")
@allure.description("Тест проверяет, что валидный пользователь может успешно авторизоваться")
@pytest.mark.parametrize("user", [
    "standard_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user",
])
def test_authorization_valid_users(driver, authorization_url, user, password, logger):
    logger.info(f"Запуск теста на авторизацию пользователя: {user}")

    login_form = LoginPage(driver, authorization_url)
    login_form.open()
    login_form.login(user, password)

    product_form = MainPage(driver)
    product_form.logout_from_account()

    logger.info(f"Тест пройден для пользователя: {user}")