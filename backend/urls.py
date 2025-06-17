from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ecommerce.urls')),  # هذا ضروري لربط api/products/
] 

