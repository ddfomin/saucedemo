import allure
from selenium.common import TimeoutException
from locators.cart_page_locators import CartPageLocators
from pages.base_page import BasePage


class CartPage(BasePage):
    locators = CartPageLocators()

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Получение названия и цены товара в корзине (для одного товара)")
    def get_name_and_price_item(self):
        self.logger.info("Начинаем считывание данных товара в корзине")

        with allure.step("Получение названия товара"):
            name_item_cart = self.element_is_visible(self.locators.NAME_PRODUCT_IN_BASKET).text

        with allure.step("Получение цены товара"):
            price_item_cart = self.element_is_visible(self.locators.PRICE_PRODUCT_IN_BASKET).text

        self.logger.info(
            f"В корзине присутствует добавленный ранее товар. Название: {name_item_cart}, цена: {price_item_cart}")

        allure.attach(
            f"Товар: {name_item_cart}\nЦена: {price_item_cart}",
            name="cart_item_info",
            attachment_type=allure.attachment_type.TEXT
        )

        return name_item_cart, price_item_cart

    @allure.step("Получение количества товаров в корзине")
    def get_items_count(self):
        self.logger.info("Считаем количество товаров в корзине")

        try:
            with allure.step("Поиск всех товаров в корзине"):
                items = self.elements_are_visible(self.locators.NAME_PRODUCT_IN_BASKET)
                count = len(items)

            self.logger.info(f"Количество товаров в корзине = {count}")

            allure.attach(
                f"Количество товаров: {count}",
                name="items_count_in_cart",
                attachment_type=allure.attachment_type.TEXT
            )

            return count

        except TimeoutException:
            with allure.step("Корзина пуста"):
                self.logger.info("Корзина пуста")
                allure.attach(
                    "Корзина пуста",
                    name="empty_cart",
                    attachment_type=allure.attachment_type.TEXT
                )
                return 0

    @allure.step("Получение названий и цен двух товаров в корзине")
    def get_name_and_price_for_two_items(self):
        self.logger.info("Начинаем считывание данных двух товаров в корзине")

        with allure.step("Получение названий и цен товаров"):
            name_elements = self.elements_are_visible(self.locators.NAME_PRODUCT_IN_BASKET)
            price_elements = self.elements_are_visible(self.locators.PRICE_PRODUCT_IN_BASKET)

        with allure.step("Проверка количества товаров в корзине"):
            if len(name_elements) < 2:
                error_msg = f"Количество товаров в корзине = {len(name_elements)}, ожидалось 2"
                self.logger.error(error_msg)
                allure.attach(
                    error_msg,
                    name="error_message",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise AssertionError(error_msg)

        name1 = name_elements[0].text
        price1 = price_elements[0].text
        name2 = name_elements[1].text
        price2 = price_elements[1].text

        self.logger.info(f"Товары в корзине: 1) {name1} ({price1}), 2) {name2} ({price2})")

        allure.attach(
            f"Товар 1: {name1} ({price1})\nТовар 2: {name2} ({price2})",
            name="cart_items_info",
            attachment_type=allure.attachment_type.TEXT
        )

        return name1, price1, name2, price2

    @allure.step("Нажатие кнопки Checkout")
    def click_on_the_checkout(self):
        self.logger.info("Сейчас нажмем Checkout для перехода на вкладку заполнения данных пользователя")

        with allure.step("Нажатие кнопки Checkout"):
            button_checkout = self.element_is_clickable(self.locators.BUTTON_CHECKOUT)
            button_checkout.click()
            self.logger.debug("Кнопка Checkout нажата")

        with allure.step("Проверка перехода на страницу заполнения данных пользователя"):
            self.assert_url_to_be("https://www.saucedemo.com/checkout-step-one.html")

        self.logger.info("Переход успешно выполнен")

        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="checkout_step_one_page",
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("Удаление товара из корзины")
    def delete_item(self):
        self.logger.info("Будем удалять товар из корзины")

        with allure.step("Нажатие кнопки Remove"):
            remove_button = self.element_is_clickable(self.locators.REMOVE_BUTTON)
            remove_button.click()
            self.logger.debug("Кнопка Remove нажата")

        with allure.step("Проверка, что товар удален из корзины"):
            try:
                self.element_is_not_visible(self.locators.REMOVE_BUTTON, timeout=5)
                self.logger.info("Товар успешно удален из корзины")

                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="item_removed_successfully",
                    attachment_type=allure.attachment_type.PNG
                )

            except TimeoutException:
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="item_not_removed_error",
                    attachment_type=allure.attachment_type.PNG
                )
                allure.attach(
                    "Товар не был удален из корзины",
                    name="error_message",
                    attachment_type=allure.attachment_type.TEXT
                )
                self.logger.error("Товар не был удален из корзины")
                raise AssertionError("Товар не был удален из корзины")