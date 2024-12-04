from django.db import models
from django.core.exceptions import ValidationError


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def clean(self):
        if self.price <= 0:
            raise ValidationError("Price must be positive.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (${self.price})"


class Order(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In Process', 'In Process'),
        ('Sent', 'Sent'),
        ('Completed', 'Completed'),
    ]

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Product, related_name="orders")
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')

    """Calculate the total price of the order based on individual product prices."""
    def calculate_total_price(self):
        return sum(product.price for product in self.products.all())

    """Check if the order can be fulfilled based on product availability."""
    def can_be_fulfilled(self):
        return all(product.available for product in self.products.all())

    def __str__(self):
        return f"Order {self.id} - {self.status} ({self.customer.name})"
