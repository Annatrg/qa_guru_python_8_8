"""
Протестируйте классы из модуля homework/models.py
"""
import random

import pytest

from homework.models import Product
from homework.models import Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def cart():
    return Cart()

class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity

        books_in_stock = product.quantity

        # Максимально допустимое количество
        assert product.check_quantity(books_in_stock) == True

        # Проверка граничных значений
        assert product.check_quantity(books_in_stock-1) == True
        assert product.check_quantity(books_in_stock+1) == False

        # Желаемое количество меньше, чем есть в наличии
        permissible_quantity = random.randint(0, books_in_stock)
        assert product.check_quantity(permissible_quantity) == True

        # Желаемое количество больше, чем есть в наличии
        non_permissible_quantity = random.randint(books_in_stock, books_in_stock+100)
        assert product.check_quantity(non_permissible_quantity) == False

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy

        books_in_stock = product.quantity
        quantity = random.randint(1, books_in_stock)
        product.buy(quantity)

        assert product.quantity >= 0

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии

        books_in_stock = product.quantity
        quantity = random.randint(books_in_stock+1, books_in_stock+10)
        with pytest.raises(ValueError):
            product.buy(quantity)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, product, cart):

    # Проверка на добавление 1 штуки товара в корзину
        cart.add_product(product)

        assert product in cart.products
        assert cart.products[product] == 1

    # Проверка на добавление к уже имеющемуся еще нескольких штук
        # Проверка сколько осталось на складе
        books_in_stock = product.quantity
        # Проверяем сколько уже есть в корзине после предыдущего теста
        books_in_basket = cart.products[product]
        # Добавляем в корзину имеющееся количество книг на складе
        basket_add = random.randint(1, books_in_stock)
        cart.add_product(product, basket_add)
        assert cart.products[product] == basket_add + books_in_basket

    # Попытаться добавить больше товара, чем есть на складе
        books_in_stock = product.quantity
        # Определяем диапазон больше, чем есть на складе
        books_in_basket = random.randint(books_in_stock + 1, books_in_stock+100)
        cart.add_product(product, books_in_basket)

        with pytest.raises(ValueError):
            cart.buy()

    def test_remove_product(self, product, cart):

    # Проверка на добавление и удаление 1 штуки товара из корзины
        cart.add_product(product)
        cart.remove_product(product)

        assert product not in cart.products

    # Проверка на удаление того же числа товара, сколько было добавлено
        books_in_stock = product.quantity
        quantity = random.randint(1, books_in_stock)
        cart.add_product(product, quantity)
        cart.remove_product(product, quantity)

        assert product not in cart.products

    # Проверка на частичное удаление товара из корзины
        # Проверка сколько осталось на складе
        books_in_stock = product.quantity
        # Добавлено в корзину несколько книг со склада
        quantity = random.randint(1, books_in_stock)
        cart.add_product(product, quantity)
        cart.remove_product(product, 1)

        assert cart.products[product] == quantity - 1
        
        # Проверка на удаление бОльшего количества, чем есть в корзине
        books_in_basket = cart.products[product]
        cart.remove_product(product, books_in_basket+1)

        assert product not in cart.products

    def test_clear(self, product, cart):
        books_in_stock = product.quantity
        quantity = random.randint(1, books_in_stock)
        cart.add_product(product, quantity)
        cart.clear()

        assert product not in cart.products

    def test_total_price(self, product, cart):

        # Если корзина пуста, то итоговая стоимость равна нулю
        cart.clear()
        assert cart.get_total_price() == 0

        # Расчет итоговой стоимости корзины, если там есть товары
        books_in_stock = product.quantity
        quantity = random.randint(1, books_in_stock)
        cart.add_product(product, quantity)

        assert cart.get_total_price() == quantity * product.price

        # Проверка итоговой стоимости без рандома
        cart.clear()
        cart.add_product(product, 5)

        assert cart.get_total_price() == 500

    def test_buy(self, product, cart):

        # Успешная покупка товара
        books_in_stock = product.quantity
        books_in_order = random.randint(1, books_in_stock)
        cart.add_product(product, books_in_order)
        cart.buy()

        assert product not in cart.products
        assert product.quantity == books_in_stock - books_in_order


        # Попытаться купить товар, который закончился
        product.quantity = 0
        cart.add_product(product)

        with pytest.raises(ValueError):
            cart.buy()
