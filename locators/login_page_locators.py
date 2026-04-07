class LoginPageLocators:
    """Локаторы на форме авторизации"""
    USERNAME_INPUT = ("xpath", "//input[@id='user-name']")
    PASSWORD_INPUT = ("xpath", "//input[@id='password']")
    ENTER_BUTTON = ("xpath", "//input[@id='login-button']")
    MESSAGE_ERROR = ("xpath", "//h3[@data-test='error']")