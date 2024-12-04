from django.core.management.base import BaseCommand
from myapp.models import Product, Customer, Order


class Command(BaseCommand):
    help = "Create sample data for Product, Customer, and Order models"

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()

        product1 = Product.objects.create(
            name='Starbucks - Verona Roast',
            price=45.99,
            available=True
        )
        product2 = Product.objects.create(
            name='Lykke - BAM BAM Espresso',
            price=89.99,
            available=True
        )
        product3 = Product.objects.create(
            name='Etno - Yirgacheffe',
            price=39.00,
            available=False
        )

        customer1 = Customer.objects.create(
            name='Arantxa Castilla-La Mancha',
            address='Maple Calle 123, Barcelona'
        )
        customer2 = Customer.objects.create(
            name='Łukasz Stecyk',
            address='Kamienna 135/13, Wroclaw'
        )
        customer3 = Customer.objects.create(
            name='Hirokazu Koreeda',
            address='2/89 Shibuya 2nd Street, Tokyo'
        )

        order1 = Order.objects.create(
            customer=customer1,
            status='New'
        )
        order2 = Order.objects.create(
            customer=customer2,
            status='In Process'
        )
        order3 = Order.objects.create(
            customer=customer3,
            status='Completed'
        )

        order1.products.add(product1, product2, product3)
        order2.products.add(product2)
        order3.products.add(product2, product3)

        self.stdout.write(self.style.SUCCESS("Sample data created successfully."))
