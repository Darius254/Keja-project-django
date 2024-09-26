# models.py
from django.db import models
from django.contrib.auth.models import User

def product_image_path(instance, filename):
    return f'products/{instance.id}/{filename}'

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=product_image_path, null=True, blank=True)
    
    city = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    num_bedrooms = models.PositiveIntegerField(blank=True, null=True)
    square_feet = models.PositiveIntegerField(blank=True, null=True)
    num_floors = models.PositiveIntegerField(blank=True, null=True)
    booked = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} booked {self.product.title} on {self.booking_date}'


