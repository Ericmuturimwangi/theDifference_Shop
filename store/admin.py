from django.contrib import admin
from . models import Category, Customer, Product, Order, Profile
from django.contrib.auth.models import User

# Register your models here.
admin.site.register (Category)
admin.site.register (Customer)
admin.site.register (Product)
admin.site.register (Order)
admin.site.register (Profile)

# mix profile info and user info

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "firstname", "lastname", "email"]
    inlines = [ProfileInline]

# unregesiter the old way
admin.site.unregister(User)

# re-register the new way
admin.site.register(User, UserAdmin)
