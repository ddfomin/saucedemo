import allure
from selenium.common import TimeoutException
from locators.login_page_locators import LoginPageLocators
from pages.base_page import BasePage


class LoginPage(BasePage):
    locators = LoginPageLocators()

    def __init__(self, driver, url):
        super().__init__(driver, url)

    @allure.step("Заполнение учетных данных")
    def _fill_credentials(self, user, password):
        """Внутренний метод для заполнения формы авторизации"""
        user_input = self.element_is_clickable(self.locators.USERNAME_INPUT)
        pass_input = self.element_is_clickable(self.locators.PASSWORD_INPUT)
        login_button = self.element_is_clickable(self.locators.ENTER_BUTTON)

        user_input.clear()
        user_input.send_keys(user)
        self.logger.debug(f"Введен логин: {user}")

        pass_input.clear()
        pass_input.send_keys(password)
        self.logger.debug("Введен пароль")

        login_button.click()
        self.logger.debug("Нажата кнопка Login")

    @allure.step("Авторизация валидного пользователя")
    def login(self, user, password):
        allure.dynamic.parameter("username", user)

        self.logger.info(f"Попытка авторизации для пользователя: {user}")
        self._fill_credentials(user, password)

        with allure.step("Проверка успешного редиректа на главную страницу"):
            expected_url = "https://www.saucedemo.com/inventory.html"
            self.assert_url_to_be(expected_url)

        self.logger.info(f"Успешный вход под пользователем: {user}")

        # Скриншот для Allure после успешного входа
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="successful_login",
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("Авторизация заблокированного пользователя")
    def login_as_locked_user(self, user, password):
        allure.dynamic.parameter("username", user)
        self.logger.info(f"Попытка авторизации для заблокированного пользователя: {user}")
        self._fill_credentials(user, password)

        with allure.step("Проверка отсутствия редиректа на главную страницу"):
            expected_url = "https://www.saucedemo.com/inventory.html"
            if self.get_current_url() == expected_url:
                # Сохранение скриншота в Allure отчёт
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="unexpected_redirect",
                    attachment_type=allure.attachment_type.PNG
                )
                self.logger.error(f"{user} смог войти, хотя не должен")
                raise AssertionError(f"{user} смог войти, хотя не должен")

        with allure.step("Проверка появления сообщения об ошибке"):
            try:
                message_error = self.element_is_visible(self.locators.MESSAGE_ERROR).text
                self.logger.info(f"Получено сообщение об ошибке: {message_error}")

                # Сохраняем текст ошибки в Allure
                allure.attach(
                    message_error,
                    name="error_message_text",
                    attachment_type=allure.attachment_type.TEXT
                )
            except TimeoutException:
                # Сохранение скриншота в Allure отчёт
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="no_error_message",
                    attachment_type=allure.attachment_type.PNG
                )
                self.logger.error("Не появилось сообщение об ошибке")
                raise AssertionError("Не появилось сообщение об ошибке для заблокированного пользователя")

        with allure.step("Проверка текста сообщения об ошибке"):
            expected_message = "Epic sadface: Sorry, this user has been locked out."
            if message_error != expected_message:
                # Сохранение скриншота в Allure отчёт
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="wrong_error_message",
                    attachment_type=allure.attachment_type.PNG
                )
                self.logger.error(f"Неверное сообщение об ошибке: {message_error}")
                raise AssertionError(
                    f"Неверное сообщение об ошибке. Ожидалось: {expected_message}, Получено: {message_error}")
            self.logger.info(f"Сообщение об ошибке корректно: {message_error}")

    @allure.step("Проверка авторизации с неверными учетными данными")
    def login_with_invalid_credentials(self, user, password):
        """Дополнительный метод для тестирования неверных данных"""
        allure.dynamic.parameter("username", user)
        self.logger.info(f"Попытка авторизации с неверными данными: {user}")
        self._fill_credentials(user, password)

        with allure.step("Проверка сообщения об ошибке для неверных данных"):
            try:
                message_error = self.element_is_visible(self.locators.MESSAGE_ERROR).text
                expected_message = "Epic sadface: Username and password do not match any user in this service"
                assert message_error == expected_message, f"Ожидалось: {expected_message}, Получено: {message_error}"

                # Сохраняем текст ошибки в Allure
                allure.attach(
                    message_error,
                    name="error_message_text",
                    attachment_type=allure.attachment_type.TEXT
                )
                self.logger.info("Сообщение об ошибке для неверных данных корректно")

            except TimeoutException:
                # Сохранение скриншота в Allure отчёт
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="no_error_message",
                    attachment_type=allure.attachment_type.PNG
                )
                raise AssertionError("Не появилось сообщение об ошибке для неверных данных")