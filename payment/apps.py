from django.apps import AppConfig


class PaymentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "payment"

    # setup payap ipn signal

    def ready(self):
        import payment.hooks
