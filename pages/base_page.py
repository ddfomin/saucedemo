from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import get_logger

class BasePage:

    def __init__(self, driver, url=None):
        self.driver = driver
        self.url = url
        self.logger = get_logger(self.__class__.__name__)
        self.logger.debug(f"Инициализация страницы: {self.__class__.__name__}")

    # Открытие ссылки в браузере
    def open(self):
        self.logger.debug(f"Открываем URL: {self.url}")
        self.driver.get(self.url)

    # Элемент(ы) виден или видны на странице пользователю
    def element_is_visible(self, locator, timeout=10):
        self.logger.debug(f"Ожидание видимости элемента: {locator}")
        try:
            return wait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        except Exception as e:
            self.logger.error(f"Элемент не стал видимым: {locator}")
            raise

    def elements_are_visible(self, locator, timeout=10):
        self.logger.debug(f"Ожидание видимости элементов: {locator}")
        try:
            return wait(self.driver, timeout).until(EC.visibility_of_all_elements_located(locator))
        except Exception as e:
            self.logger.error(f"Элементы не стали видимыми: {locator}")
            raise

    # Элемент(ы) есть в HTML (DOM)
    def element_is_present(self, locator, timeout=10):
        self.logger.debug(f"Ожидание присутствия элемента: {locator}")
        try:
            return wait(self.driver, timeout).until(EC.presence_of_element_located(locator))
        except Exception as e:
            self.logger.error(f"Элемент не появился в DOM: {locator}")
            raise

    def elements_are_present(self, locator, timeout=10):
        self.logger.debug(f"Ожидание присутствия элементов: {locator}")
        try:
            return wait(self.driver, timeout).until(EC.presence_of_all_elements_located(locator))
        except Exception as e:
            self.logger.error(f"Элементы не появились в DOM: {locator}")
            raise

    # Элемент невидимый
    def element_is_not_visible(self, locator, timeout=10):
        self.logger.debug(f"Ожидание невидимости элемента: {locator}")
        try:
            return wait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
        except Exception as e:
            self.logger.error(f"Элемент все еще видим: {locator}")
            raise

    # Элемент кликабельный
    def element_is_clickable(self, locator, timeout=10):
        self.logger.debug(f"Ожидание кликабельности элемента: {locator}")
        try:
            return wait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
        except Exception as e:
            self.logger.error(f"Элемент не стал кликабельным: {locator}")
            raise

    # Перемещение к элементу
    def go_to_element(self, element):
        self.logger.debug("Скролл к элементу")
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    # Переключение между окнами или вкладками
    def switch_to_new_window(self, number):
        self.logger.debug(f"Переключение на окно с индексом {number}")
        self.driver.switch_to.window(self.driver.window_handles[number])

    """ActionChains"""
    # Двойной клик
    def action_double_click(self, element):
        self.logger.debug("Двойной клик")
        action = ActionChains(self.driver)
        action.double_click(element)
        action.perform()

    # Правый клик
    def action_right_click(self, element):
        self.logger.debug("Правый клик")
        action = ActionChains(self.driver)
        action.context_click(element)
        action.perform()

    # Перетаскивание по координатам
    def action_drag_and_drop_by_offset(self, element, x_coords, y_coords):
        self.logger.debug(f"Drag and drop по координатам: ({x_coords}, {y_coords})")
        action = ActionChains(self.driver)
        action.drag_and_drop_by_offset(element, x_coords, y_coords)
        action.perform()

    # Перетаскивание на другой элемент
    def action_drag_and_drop_by_element(self, what, where):
        self.logger.debug("Drag and drop на элемент")
        action = ActionChains(self.driver)
        action.drag_and_drop(what, where)
        action.perform()

    # Наведение курсора
    def action_move_to_element(self, element):
        self.logger.debug("Наведение курсора")
        action = ActionChains(self.driver)
        action.move_to_element(element)
        action.perform()

    """Проверка URL"""
    # Проверка открытия корректного URL
    def assert_url_to_be(self, url, timeout=10):
        """Проверка URL"""
        self.logger.debug(f"Ожидание URL: {url}")
        try:
            wait(self.driver, timeout).until(EC.url_to_be(url))
            self.logger.debug(f"Успешный переход на URL: {url}")
        except Exception as error:
            self.logger.error(f"Переход не произошел. Ожидалось: {url}, Текущий: {self.driver.current_url}")
            raise AssertionError(
                f"Переход не произошел. Ожидалось: {url}, "
                f"Текущий: {self.driver.current_url}"
            )

    # Получение текущего URL
    def get_current_url(self):
        current_url = self.driver.current_url
        self.logger.debug(f"Текущий URL: {current_url}")
        return current_url