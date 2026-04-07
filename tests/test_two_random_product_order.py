import allure
from pages.cart_page import CartPage
from pages.confirmation_page import ConfirmationPage
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.success_order_page import SuccessOrderPage
from pages.user_info_page import UserInfoPage


def _verify_product_match(product_name, product_price, page_name, actual_name, actual_price):
    """Вспомогательная функция для проверки соответствия товара"""
    assert product_name == actual_name, \
        f"Ошибка на форме '{page_name}': название не совпадает. " \
        f"Ожидалось: '{product_name}', Получено: '{actual_name}'"
    assert product_price == actual_price, \
        f"Ошибка на форме '{page_name}': цена не совпадает. " \
        f"Ожидалось: '{product_price}', Получено: '{actual_price}'"


@allure.title("Тест покупки двух случайных товаров")
@allure.description(
    "Тест проверяет полный цикл покупки двух случайных товаров: добавление в корзину, оформление, проверка и завершение")
def test_buy_two_random_items(driver, authorization_url, password, logger):
    logger.info("Запуск теста на покупку двух случайных товаров")

    # Авторизация стандартным пользователем
    login_page = LoginPage(driver, authorization_url)
    login_page.open()
    login_page.login("standard_user", password)

    # Добавление двух случайных товаров в корзину и переход в корзину
    main_page = MainPage(driver)
    name_from_main1, price_from_main1, name_from_main2, price_from_main2 = main_page.add_two_items()
    main_page.go_to_cart()

    # Проверка количества товаров в корзине
    cart_page = CartPage(driver)
    assert cart_page.get_items_count() == 2, "В корзине не 2 товара"

    # Проверка товаров в корзине
    name_from_cart1, price_from_cart1, name_from_cart2, price_from_cart2 = cart_page.get_name_and_price_for_two_items()
    _verify_product_match(name_from_main1, price_from_main1, "корзина", name_from_cart1, price_from_cart1)
    _verify_product_match(name_from_main2, price_from_main2, "корзина", name_from_cart2, price_from_cart2)

    # Переход к оформлению заказа
    cart_page.click_on_the_checkout()

    # Заполнение данных пользователя
    user_info_page = UserInfoPage(driver)
    user_info_page.fill_in_data_user()

    # Переход к странице подтверждения
    user_info_page.go_to_next_page()

    # Проверка товаров на странице подтверждения
    confirmation_page = ConfirmationPage(driver)
    name_from_conf1, price_from_conf1, name_from_conf2, price_from_conf2 = confirmation_page.finish_check_for_two_items()
    _verify_product_match(name_from_main1, price_from_main1, "подтверждение", name_from_conf1, price_from_conf1)
    _verify_product_match(name_from_main2, price_from_main2, "подтверждение", name_from_conf2, price_from_conf2)

    # Завершение покупки
    confirmation_page.go_to_next()

    # Проверка сообщения об успешной покупке
    success_page = SuccessOrderPage(driver)
    success_page.check_success_message()

    # Возврат на главную страницу
    success_page.go_to_home_page()

    logger.info(f"Тест пройден: два товара успешно куплены")