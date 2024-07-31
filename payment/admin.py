from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

# Register your models on admin section
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# cretae an orderitem inline


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


# extend the order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    fields = [
        "user",
        "full_name",
        "email",
        "shipping_address",
        "amount_paid",
        "date_ordered",
        "shipped",
    ]
    inlines = [OrderItemInline]


# unregister the order model
admin.site.unregister(Order)
# re-register order
admin.site.register(Order, OrderAdmin)
