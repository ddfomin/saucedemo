import allure
from pages.main_page import MainPage
from pages.login_page import LoginPage

@allure.title("Тест авторизации всех валидных пользователей")
@allure.description("Тест проверяет, что все валидные пользователи из списка могут успешно авторизоваться")
def test_authorization_valid_users(driver, authorization_url, valid_users_list, password, logger):
    logger.info("Запуск теста на авторизацию всех валидных пользователей")
    # Шаг 1: Открытие страницы авторизации
    login_form = LoginPage(driver, authorization_url)
    login_form.open()
    # Шаг 2: Проходимся по списку пользователей
    for user in valid_users_list:
        login_form.login(user, password)
        # Выход из аккаунта
        product_form = MainPage(driver)
        product_form.logout_from_account()

    logger.info("Тест пройден")