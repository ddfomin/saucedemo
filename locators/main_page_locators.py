class MainPageLocators:
    """Локаторы на форме выбора товара"""
    BURGER_MENU = ("xpath", "//button[@id='react-burger-menu-btn']")
    LOGOUT_BUTTON = ("xpath", "//a[@id='logout_sidebar_link']")
    NAME_SELECTED_PRODUCT = ("xpath", "//div[@data-test='inventory-item-name']")
    PRICE_SELECTED_PRODUCT = ("xpath", "//div[@class='inventory_item_price']")
    BUTTON_ADD_TO_CARD = ("xpath", "//button[contains(@class, 'btn')]")
    BUTTON_BASKET = ("xpath", "//a[@class='shopping_cart_link']")
    REMOVE_ITEM = ("xpath", "//button[contains(@name, 'remove')]")