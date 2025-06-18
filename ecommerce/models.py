from django.db import models

class Admin(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=255)
    profile_picture = models.ImageField(
        upload_to='admin_pics/',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.name} {self.surname}"

class Seller(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=254, unique=True)
    address = models.CharField(max_length=255)
    birth_date = models.DateField()
    password = models.CharField(max_length=255)
    profile_picture = models.ImageField(
        upload_to='seller_pics/',
        null=True,
        blank=True,
        default='https://res.cloudinary.com/<cloud_name>/image/upload/v1234567890/seller_pics/PIO.jpg'
    )

    def __str__(self):
        return f"{self.name} {self.surname}"

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    image1 = models.ImageField(upload_to='product_images/', null=True, blank=True)
    image2 = models.ImageField(upload_to='product_images/', null=True, blank=True)
    image3 = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return self.name
