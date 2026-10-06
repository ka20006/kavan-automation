from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"

class Shop(models.Model):
    name = models.CharField(max_length=150)
    owner_name = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    shop_photo = models.ImageField(upload_to="shops/", blank=True, null=True)
    card_photo = models.ImageField(upload_to="cards/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    PAYMENT_CHOICES = [
        ("cash","Cash"), ("upi","UPI"), ("credit","Credit"), ("partial","Partial")
    ]
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="orders")
    salesman = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default="cash")
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def pending_amount(self):
        return max(self.total_amount - self.paid_amount, 0)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
