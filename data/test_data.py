from random import randint
from faker import Faker
fake = Faker()

def get_random_user():
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "zip_code": fake.zipcode()
    }

ITEMS_ON_PAGE = 6  # количество товаров на главной
def get_random_item_index():
    """Получить случайный индекс товара (0 до ITEMS_ON_PAGE-1)"""
    return randint(0, ITEMS_ON_PAGE - 1)