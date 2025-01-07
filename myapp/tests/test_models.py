from django.test import TestCase
from myapp.models import Product, Customer, Order
from django.core.exceptions import ValidationError
from decimal import Decimal


class ProductModelTest(TestCase):
    def test_create_product_with_valid_data(self):
        temp_product = Product.objects.create(name='Temporary product', price=Decimal('1.99'), available=True)
        temp_product.full_clean()
        self.assertEqual(temp_product.name, 'Temporary product')
        self.assertEqual(temp_product.price, Decimal('1.99'))
        self.assertTrue(temp_product.available)

    def test_create_product_with_negative_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='Invalid product', price=Decimal('-1.99'), available=True)
            temp_product.full_clean()

    def test_create_product_with_blank_name(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='', price=Decimal('1.99'), available=True)
            temp_product.full_clean()

    def test_create_product_with_edge_values_name(self):
        product = Product.objects.create(name='a' * 255, price=Decimal('10.99'), available=True)
        self.assertEqual(product.name, 'a' * 255)

        with self.assertRaises(ValidationError):
            long_name_product = Product(name='a' * 256, price=Decimal('10.99'), available=True)
            long_name_product.full_clean()

    def test_create_product_with_max_price(self):
        valid_product = Product(name='Valid product', price=Decimal('99999999.99'), available=True)
        valid_product.full_clean()
        self.assertEqual(valid_product.price, Decimal('99999999.99'))

        with self.assertRaises(ValidationError):
            invalid_product = Product(name='Invalid product', price=Decimal('100000000.00'), available=True)
            invalid_product.full_clean()

    def test_create_product_with_min_price(self):
        valid_product = Product(name='Valid product', price=Decimal('0.01'), available=True)
        valid_product.full_clean()
        self.assertEqual(valid_product.price, Decimal('0.01'))

        with self.assertRaises(ValidationError):
            zero_price_product = Product(name='Invalid product', price=Decimal('0.00'), available=True)
            zero_price_product.full_clean()

class CustomerModelTest(TestCase):
    def test_create_customer_with_valid_data(self):
        temp_customer = Customer.objects.create(name='Temporary customer', address='123 Test Street')
        temp_customer.full_clean()
        self.assertEqual(temp_customer.name, 'Temporary customer')
        self.assertEqual(temp_customer.address, '123 Test Street')

    def test_create_customer_with_missing_name(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer(name='', address='123 Test Street')
            temp_customer.full_clean()

    def test_create_customer_with_blank_address(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer.objects.create(name='Addressless Customer', address='')
            temp_customer.full_clean()
            self.assertEqual(temp_customer.address, '')

    def test_create_customer_with_edge_value_name(self):
        temp_customer = Customer.objects.create(name='a' * 100, address='123 Test Street')
        temp_customer.full_clean()

        temp_customer = Customer(name='a' * 101, address='123 Test Street')
        with self.assertRaises(ValidationError):
            temp_customer.full_clean()


class OrderModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(name="Test Customer", address="123 Test Street")

        self.product1 = Product.objects.create(name="Product 1", price=Decimal("10.99"), available=True)
        self.product2 = Product.objects.create(name="Product 2", price=Decimal("5.50"), available=False)

        self.order = Order.objects.create(customer=self.customer, status="New")
        self.order.products.add(self.product1, self.product2)

    def test_order_creation_with_valid_data(self):
        self.assertEqual(self.order.customer.name, "Test Customer")
        self.assertEqual(self.order.status, "New")
        self.assertIn(self.product1, self.order.products.all())
        self.assertIn(self.product2, self.order.products.all())

    def test_order_creation_missing_customer(self):
        with self.assertRaises(ValidationError):
            order = Order(status="New")
            order.full_clean()

    def test_order_creation_invalid_status(self):
        with self.assertRaises(ValidationError):
            order = Order(customer=self.customer, status="Invalid Status")
            order.full_clean()

    def test_calculate_total_price_with_valid_products(self):
        total_price = self.order.calculate_total_price()
        self.assertEqual(total_price, Decimal("16.49"))  # 10.99 + 5.50

    def test_calculate_total_price_with_no_products(self):
        empty_order = Order.objects.create(customer=self.customer, status="New")
        self.assertEqual(empty_order.calculate_total_price(), Decimal("0.00"))

    def test_can_be_fulfilled_with_available_products(self):
        self.assertFalse(self.order.can_be_fulfilled())  # One product is unavailable

        # Making all products available
        self.product2.available = True
        self.product2.save()
        self.assertTrue(self.order.can_be_fulfilled())

    def test_can_be_fulfilled_with_unavailable_products(self):
        self.product1.available = False
        self.product1.save()
        self.product2.available = False
        self.product2.save()

        self.assertFalse(self.order.can_be_fulfilled())