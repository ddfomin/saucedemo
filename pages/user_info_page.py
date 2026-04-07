import allure
from locators.user_info_page_locators import UserInfoPageLocators
from pages.base_page import BasePage
from data.test_data import get_random_user


class UserInfoPage(BasePage):
    locators = UserInfoPageLocators()

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Заполнение данных пользователя")
    def fill_in_data_user(self):
        self.logger.info("Начинаем заполнять данные пользователя")

        with allure.step("Поиск полей ввода"):
            first_name_input = self.element_is_clickable(self.locators.FIRST_NAME_INPUT)
            last_name_input = self.element_is_clickable(self.locators.LAST_NAME_INPUT)
            postal_code_input = self.element_is_clickable(self.locators.POSTAL_CODE_INPUT)

        with allure.step("Генерация случайных пользовательских данных"):
            user_data = get_random_user()
            self.logger.debug(f"Сгенерированы данные: {user_data}")

            # Прикрепляем данные в отчёт
            allure.attach(
                f"Имя: {user_data['first_name']}\nФамилия: {user_data['last_name']}\nПочтовый индекс: {user_data['zip_code']}",
                name="user_data_generated",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Заполнение полей формы"):
            first_name_input.send_keys(user_data["first_name"])
            last_name_input.send_keys(user_data["last_name"])
            postal_code_input.send_keys(user_data["zip_code"])
            self.logger.debug("Поля заполнены")

        with allure.step("Проверка корректности введенных данных"):
            assert first_name_input.get_attribute("value") == user_data["first_name"], "Имя не ввелось"
            assert last_name_input.get_attribute("value") == user_data["last_name"], "Фамилия не ввелась"
            assert postal_code_input.get_attribute("value") == user_data["zip_code"], "Код почты не ввелся"
            self.logger.debug("Проверка ввода данных прошла успешно")

        self.logger.info(
            f"Данные заполнены: first_name - {user_data['first_name']}, last_name - {user_data['last_name']}, zip_code - {user_data['zip_code']}")

        # Скриншот после заполнения формы
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="filled_user_info_form",
            attachment_type=allure.attachment_type.PNG
        )

        return user_data

    @allure.step("Переход на страницу подтверждения заказа")
    def go_to_next_page(self):
        self.logger.debug("Переход на страницу подтверждения")

        with allure.step("Нажатие кнопки Continue"):
            continue_button = self.element_is_clickable(self.locators.CONTINUE_BUTTON)
            continue_button.click()
            self.logger.debug("Кнопка Continue нажата")

        with allure.step("Проверка URL страницы подтверждения"):
            self.assert_url_to_be("https://www.saucedemo.com/checkout-step-two.html")

        self.logger.info("Переход на страницу подтверждения")

        # Скриншот страницы подтверждения
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="checkout_step_two_page",
            attachment_type=allure.attachment_type.PNG
        )