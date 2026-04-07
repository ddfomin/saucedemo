import allure
from locators.success_order_page_locators import SuccessOrderPageLocators
from pages.base_page import BasePage


class SuccessOrderPage(BasePage):
    locators = SuccessOrderPageLocators()

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Возврат на главную страницу")
    def go_to_home_page(self):
        self.logger.info("Будем возвращаться на главную страницу")

        with allure.step("Нажатие кнопки Back Home"):
            button_back_home = self.element_is_clickable(self.locators.BUTTON_BACK_HOME)
            button_back_home.click()
            self.logger.debug("Кнопка Back Home нажата")

        with allure.step("Проверка редиректа на главную страницу"):
            self.assert_url_to_be("https://www.saucedemo.com/inventory.html")

        self.logger.info("Выполнен возврат на главную страницу")

        # Скриншот главной страницы после возврата
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="home_page_after_return",
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("Проверка сообщения об успешной покупке")
    def check_success_message(self):
        self.logger.info("Будем проверять наличие корректного сообщения об успешной покупке")

        with allure.step("Получение текста сообщения"):
            message = self.element_is_visible(self.locators.SUCCESS_MESSAGE).text
            expected_message = "Thank you for your order!"

        with allure.step(f"Проверка сообщения: ожидается '{expected_message}'"):
            if message != expected_message:

                # Скриншот ошибки в Allure
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="wrong_success_message",
                    attachment_type=allure.attachment_type.PNG
                )

                # Текст ошибки в Allure
                allure.attach(
                    f"Ожидалось: {expected_message}\nПолучено: {message}",
                    name="error_details",
                    attachment_type=allure.attachment_type.TEXT
                )

                self.logger.error(f"Неверное сообщение: {message}")
                raise AssertionError(f"Неверное сообщение. Ожидалось: {expected_message}, Получено: {message}")

        self.logger.info(f"Сообщение об успешной покупке корректно: {message}")

        # Прикрепляем успешное сообщение в отчёт
        allure.attach(
            message,
            name="success_message_text",
            attachment_type=allure.attachment_type.TEXT
        )

        # Скриншот успешного заказа
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="successful_order_page",
            attachment_type=allure.attachment_type.PNG
        )

