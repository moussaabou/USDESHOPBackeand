from django.db import models

class Admin(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='admin_pics/', null=True, blank=True)  # صورة الإدمن

    def __str__(self):
        return self.name

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
        default='seller_pics/PIO.jpg'  # تعيين صورة افتراضية إذا لم يتم رفع صورة
    )

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # السعر
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    image1 = models.ImageField(upload_to='product_images/', null=True, blank=True)  # الصورة الأولى
    image2 = models.ImageField(upload_to='product_images/', null=True, blank=True)  # الصورة الثانية
    image3 = models.ImageField(upload_to='product_images/', null=True, blank=True)  # الصورة الثالثة

    def __str__(self):
        return self.name
