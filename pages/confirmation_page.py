import allure
from selenium.common import TimeoutException
from locators.confirmation_page_locators import ConfirmationPageLocators
from pages.base_page import BasePage


class ConfirmationPage(BasePage):
    locators = ConfirmationPageLocators()

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Получение данных товара на странице подтверждения (для одного товара)")
    def finish_check_item(self):
        self.logger.info("Начинаем считывание данных товара на странице подтверждения")

        with allure.step("Получение названия товара"):
            name_product = self.element_is_visible(self.locators.NAME_PRODUCT_CONF).text

        with allure.step("Получение цены товара"):
            price_product = self.element_is_visible(self.locators.PRICE_PRODUCT_CONF).text

        with allure.step("Получение итоговой стоимости"):
            total_price = self.element_is_visible(self.locators.TOTAL_PRICE).text.split(": ")[1]

        self.logger.info(
            f"На странице присутствует товар {name_product} с ценой = {price_product}. Итого за весь заказ = {total_price}")

        allure.attach(
            f"Товар: {name_product}\nЦена: {price_product}\nИтого: {total_price}",
            name="order_summary",
            attachment_type=allure.attachment_type.TEXT
        )

        return name_product, price_product, total_price

    @allure.step("Получение количества товаров на странице подтверждения")
    def get_items_count(self):
        self.logger.info("Считаем количество товаров")

        try:
            with allure.step("Поиск всех товаров на странице"):
                items = self.elements_are_visible(self.locators.NAME_PRODUCT_CONF)
                count = len(items)

            self.logger.info(f"На странице подтверждения {count} товаров")

            allure.attach(
                f"Количество товаров: {count}",
                name="items_count",
                attachment_type=allure.attachment_type.TEXT
            )

            return count

        except TimeoutException:
            with allure.step("Товары не найдены на странице"):
                self.logger.warning("Товары не найдены на странице подтверждения")
                allure.attach(
                    "Товары отсутствуют на странице",
                    name="no_items_found",
                    attachment_type=allure.attachment_type.TEXT
                )
                return 0

    @allure.step("Получение данных двух товаров на странице подтверждения")
    def finish_check_for_two_items(self):
        self.logger.info("Начинаем считывание данных двух товаров на странице подтверждения")

        with allure.step("Получение названий и цен товаров"):
            name_elements = self.elements_are_visible(self.locators.NAME_PRODUCT_CONF)
            price_elements = self.elements_are_visible(self.locators.PRICE_PRODUCT_CONF)

        with allure.step("Проверка количества товаров"):
            if len(name_elements) < 2:
                error_msg = f"Найдено {len(name_elements)} товара, ожидалось 2"
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

        with allure.step("Получение и проверка итоговой суммы"):
            total_price_text = self.element_is_visible(self.locators.TOTAL_PRICE).text
            total_price = float(total_price_text.split("$")[1])

            price1_float = float(price1.strip("$"))
            price2_float = float(price2.strip("$"))

            expected_total = round(price1_float + price2_float, 2)

            if expected_total != total_price:
                error_msg = f"Сумма не совпадает. {price1_float} + {price2_float} = {expected_total}, итого: {total_price}"
                allure.attach(
                    error_msg,
                    name="price_mismatch",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise AssertionError(error_msg)

        self.logger.info(f"Товары: 1) {name1} ({price1}), 2) {name2} ({price2})")

        allure.attach(
            f"Товар 1: {name1} ({price1})\nТовар 2: {name2} ({price2})\nИтоговая сумма: ${total_price}",
            name="order_summary_two_items",
            attachment_type=allure.attachment_type.TEXT
        )

        return name1, price1, name2, price2

    @allure.step("Нажатие кнопки Finish и переход на страницу успеха")
    def go_to_next(self):
        self.logger.info("Сейчас нажмем кнопку Finish")

        with allure.step("Нажатие кнопки Finish"):
            finish_button = self.element_is_clickable(self.locators.BUTTON_FINISH)
            finish_button.click()
            self.logger.info("Кнопка Finish нажата")

        with allure.step("Проверка перехода на страницу завершения заказа"):
            self.assert_url_to_be("https://www.saucedemo.com/checkout-complete.html")

        self.logger.info("Успешный переход на страницу завершения заказа")

        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="checkout_complete_page",
            attachment_type=allure.attachment_type.PNG
        )