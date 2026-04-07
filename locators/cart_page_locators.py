class CartPageLocators:
    """Локаторы на форме корзины"""
    NAME_PRODUCT_IN_BASKET = ("xpath", "//div[@data-test='inventory-item-name']")
    PRICE_PRODUCT_IN_BASKET = ("xpath", "//div[@class='inventory_item_price']")
    BUTTON_CHECKOUT = ("xpath", "//button[@id='checkout']")
    REMOVE_BUTTON = ("xpath", "//button[contains(@name, 'remove')]")