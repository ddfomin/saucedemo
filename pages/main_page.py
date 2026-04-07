import allure
from data.test_data import get_random_item_index
from locators.main_page_locators import MainPageLocators
from pages.base_page import BasePage


class MainPage(BasePage):
    locators = MainPageLocators()

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Выход из аккаунта")
    def logout_from_account(self):
        self.logger.info("Будем выходить из аккаунта")

        with allure.step("Открытие бургер-меню"):
            burger_menu = self.element_is_clickable(self.locators.BURGER_MENU)
            burger_menu.click()
            self.logger.debug("Клик на главное меню")

        with allure.step("Нажатие кнопки Logout"):
            logout_button = self.element_is_clickable(self.locators.LOGOUT_BUTTON)
            logout_button.click()
            self.logger.debug("Клик на кнопку Logout")

        self.logger.info("Успешно вышли из аккаунта")

        # Скриншот после выхода
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="after_logout",
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("Переход в корзину")
    def go_to_cart(self):
        self.logger.info("Будем переходить в корзину")

        button_basket = self.element_is_visible(self.locators.BUTTON_BASKET)
        button_basket.click()
        self.logger.debug("Клик по корзине")

        with allure.step("Проверка URL корзины"):
            self.assert_url_to_be("https://www.saucedemo.com/cart.html")

        self.logger.info("Успешно перешли в корзину")

        # Скриншот корзины
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name="cart_page",
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("Поиск случайного товара")
    def find_random_item(self):
        random_item = get_random_item_index()
        self.logger.debug(f"Выбран случайный индекс: {random_item + 1}")

        with allure.step("Получение списка товаров"):
            name_elements = self.elements_are_visible(self.locators.NAME_SELECTED_PRODUCT)
            price_elements = self.elements_are_visible(self.locators.PRICE_SELECTED_PRODUCT)

        # Проверка индекса
        if random_item >= len(name_elements):
            error_msg = f"Индекс {random_item} вне диапазона. Доступно товаров: {len(name_elements)}"
            allure.attach(
                error_msg,
                name="error_message",
                attachment_type=allure.attachment_type.TEXT
            )
            raise IndexError(error_msg)

        name_product = name_elements[random_item].text
        price_product = price_elements[random_item].text
        self.logger.info(f"Выбран товар: {name_product}, цена: {price_product}")

        allure.attach(
            f"Товар: {name_product}\nЦена: {price_product}",
            name="selected_item_info",
            attachment_type=allure.attachment_type.TEXT
        )

        return name_product, price_product, random_item

    @allure.step("Добавление товара по индексу {item_index}")
    def add_item_by_index(self, item_index):
        self.logger.debug(f"Попытка добавить товар в корзину с индексом {item_index + 1}")

        with allure.step("Получение списка кнопок добавления"):
            buttons = self.elements_are_visible(self.locators.BUTTON_ADD_TO_CARD)

        # Проверка индекса
        if item_index >= len(buttons):
            error_msg = f"Индекс {item_index} вне диапазона. Доступно кнопок: {len(buttons)}"
            allure.attach(
                error_msg,
                name="error_message",
                attachment_type=allure.attachment_type.TEXT
            )
            raise IndexError(error_msg)

        buttons[item_index].click()
        self.logger.info(f"Выбранный товар добавлен в корзину")

        # Скриншот после добавления
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=f"after_adding_item_{item_index + 1}",
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("Добавление товара с выбором от пользователя")
    def add_selection_item(self):
        self.logger.info("Будем добавлять товар в корзину по выбору пользователя")

        try:
            item_index = int(input("Выберите товар и введите его номер: ")) - 1
            self.add_item_by_index(item_index)
            name = self.elements_are_visible(self.locators.NAME_SELECTED_PRODUCT)[item_index].text
            price = self.elements_are_visible(self.locators.PRICE_SELECTED_PRODUCT)[item_index].text
            self.go_to_cart()
            return name, price
        except ValueError:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="invalid_input_error",
                attachment_type=allure.attachment_type.PNG
            )
            allure.attach(
                "Введено некорректное число",
                name="error_message",
                attachment_type=allure.attachment_type.TEXT
            )
            self.logger.error("Введено некорректное число")
            raise AssertionError("Введите корректное число")

    @allure.step("Добавление в корзину случайного товара в корзину")
    def add_random_item_to_cart(self):
        self.logger.info("Будем добавлять один случайный товар в корзину")
        name_product, price_product, random_item = self.find_random_item()
        self.add_item_by_index(random_item)
        return name_product, price_product

    @allure.step("Добавление двух случайных товаров в корзину")
    def add_two_items(self):
        self.logger.info("Будем добавлять в корзину два случайных товара")

        with allure.step("Проверка количества товаров на странице"):
            items_count = len(self.elements_are_visible(self.locators.NAME_SELECTED_PRODUCT))
            if items_count < 2:
                error_msg = f"Недостаточно товаров. Доступно: {items_count}, нужно: 2"
                allure.attach(
                    error_msg,
                    name="error_message",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise AssertionError(error_msg)

        with allure.step("Добавление первого товара"):
            name1, price1, index1 = self.find_random_item()
            self.add_item_by_index(index1)

        with allure.step("Добавление второго товара (отличного от первого)"):
            name2, price2, index2 = self.find_random_item()

            # Защита от бесконечного цикла (максимум 10 попыток)
            attempts = 0
            while index2 == index1 and attempts < 10:
                self.logger.debug("Повторный выбор, ищем другой товар")
                name2, price2, index2 = self.find_random_item()
                attempts += 1

            if index2 == index1:
                error_msg = "Не удалось выбрать другой товар (возможно, на странице только 1 товар)"
                allure.attach(
                    error_msg,
                    name="error_message",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise AssertionError(error_msg)

            self.add_item_by_index(index2)
            self.logger.info(f"Второй товар «{name2}» успешно добавлен в корзину")

        allure.attach(
            f"Первый товар: {name1}, Цена: {price1}\nВторой товар: {name2}, Цена: {price2}",
            name="added_items_info",
            attachment_type=allure.attachment_type.TEXT
        )

        return name1, price1, name2, price2