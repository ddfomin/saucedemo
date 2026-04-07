import allure
from pages.cart_page import CartPage
from pages.main_page import MainPage
from pages.login_page import LoginPage


@allure.title("Тест на удаление товара из корзины")
@allure.description("Тест проверяет, что добавленный товар можно успешно удалить из корзины")
def test_delete_item(driver, authorization_url, password, logger):
    logger.info("Запуск теста на удаление товара с главного меню и из корзины")

    # Авторизация стандартным пользователем
    login_form = LoginPage(driver, authorization_url)
    login_form.open()
    login_form.login("standard_user", password)

    # Добавление товара в корзину
    main_form = MainPage(driver)
    main_form.add_random_item_to_cart()

    # Удаление товара из корзины
    cart_form = CartPage(driver)
    cart_form.delete_item()

    logger.info("Тест пройден, добавленный товар был удален из корзины")