import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.logger import get_logger


@pytest.fixture(scope="function")
def driver():
    options = Options()
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
        "profile.default_content_setting_values.notifications": 2,
        "autofill.profile_enabled": False,
        "autofill.credit_card_enabled": False
    }
    options.add_experimental_option("prefs", prefs)

    # Дополнительные аргументы
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    # Дополнительные аргументы

    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--disable-password-generation")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def password():
    """Общий пароль для всех пользователей"""
    return "secret_sauce"

@pytest.fixture(scope="function")
def authorization_url():
    """Базовый URL"""
    return "https://www.saucedemo.com/"

@pytest.fixture(scope="function")
def logger():
    """Фикстура для логирования в тестах"""
    return get_logger("tests")

