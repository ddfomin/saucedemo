import allure
from pages.login_page import LoginPage


@allure.title("Тест авторизации заблокированного пользователя")
@allure.description(
    "Тест проверяет, что заблокированный пользователь не может авторизоваться и видит соответствующее сообщение об ошибке")
def test_authorization_locked_user(driver, authorization_url, locked_user, password, logger):
    logger.info("Запуск теста на авторизацию заблокированного пользователя")

    login_form = LoginPage(driver, authorization_url)
    login_form.open()
    login_form.login_as_locked_user(locked_user, password)

    logger.info("Тест пройден")