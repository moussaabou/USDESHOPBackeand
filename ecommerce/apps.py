from django.apps import AppConfig

class EcommerceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ecommerce'

    def ready(self):
        import ecommerce.signals  # 👈 استيراد الإشارات هنا
