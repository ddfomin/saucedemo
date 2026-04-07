class ConfirmationPageLocators:
    """Локаторы на форме подтверждения покупки"""
    NAME_PRODUCT_CONF = ("xpath", "//div[@class='inventory_item_name']")
    PRICE_PRODUCT_CONF = ("xpath", "//div[@class='inventory_item_price']")
    TOTAL_PRICE = ("xpath", "//div[@class='summary_subtotal_label']")
    BUTTON_FINISH = ("xpath", "//button[@id='finish']")