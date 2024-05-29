from django.contrib import admin

from .models import Category, Customer, Product, Order, Profile

from django.contrib.auth.models import User
# Register your models here.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)


# Mix the profile into user information
class ProfileInline(admin.StackedInline):
    model = Profile
    

# Extend the User model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username","first_name","last_name","email"]
    # This will import the user model and add the profile information to the user model
    inlines = [ProfileInline]

# In Django we need to unregister the 
admin.site.unregister(User)

# Re-register the new way
admin.site.register(User,UserAdmin)