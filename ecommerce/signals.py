from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Admin

@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    if Admin.objects.count() == 0:
        Admin.objects.create(
            name='المدير',
            surname='الافتراضي',
            email='admin@shop.com',
            password='admin123',  # ⚠️ لاحقًا ضعها مشفرة!
        )
        print("✅ تم إنشاء إدمن افتراضي")
