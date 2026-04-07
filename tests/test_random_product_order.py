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


@allure.title("Тест покупки случайного товара")
@allure.description(
    "Тест проверяет полный цикл покупки одного случайного товара: добавление в корзину, оформление, проверка и завершение")
def test_buy_random_item(driver, authorization_url, password, logger):
    logger.info("Запуск теста на покупку одного случайного товара")

    # Авторизация стандартным пользователем
    login_form = LoginPage(driver, authorization_url)
    login_form.open()
    login_form.login("standard_user", password)

    # Добавление случайного товара в корзину и переход в корзину
    main_form = MainPage(driver)
    name_main, price_main = main_form.add_random_item_to_cart()
    main_form.go_to_cart()

    # Проверка товара в корзине
    cart_form = CartPage(driver)
    name_cart, price_cart = cart_form.get_name_and_price_item()
    _verify_product_match(name_main, price_main, "корзина", name_cart, price_cart)

    # Переход к оформлению заказа
    cart_form.click_on_the_checkout()

    # Заполнение данных пользователя
    user_info_form = UserInfoPage(driver)
    user_info_form.fill_in_data_user()

    # Переход к странице подтверждения
    user_info_form.go_to_next_page()

    # Проверка данных на странице подтверждения
    conf_form = ConfirmationPage(driver)
    name_conf, price_conf, total_price = conf_form.finish_check_item()
    _verify_product_match(name_main, price_main, "подтверждение", name_conf, price_conf)

    # Проверка итоговой суммы
    assert price_main == total_price, \
        f"Итоговая сумма не совпадает с ценой товара. Цена: '{price_main}', Итого: '{total_price}'"

    # Завершение покупки
    conf_form.go_to_next()

    # Проверка сообщения об успешной покупке
    success_form = SuccessOrderPage(driver)
    success_form.check_success_message()

    # Возврат на главную страницу
    success_form.go_to_home_page()

    logger.info(f"Тест пройден: товар {name_main} успешно куплен")