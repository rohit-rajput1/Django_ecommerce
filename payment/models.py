from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    shipping_full_name = models.CharField(max_length=100)
    shipping_email = models.CharField(max_length=100)
    shipping_address1 = models.CharField(max_length=255)
    shipping_address2 = models.CharField(max_length=255, blank=True, null=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100, blank=True, null=True)
    shipping_zip_code = models.CharField(max_length=10, blank=True, null=True)
    shipping_country = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Shipping Addresses'
    
    def __str__(self):
        return f"Shipping Address - {str(self.id)}"

# Assuming you have a Profile model defined elsewhere
@receiver(post_save, sender=User)
def create_shipping(sender, instance, created, **kwargs):
    if created:
        ShippingAddress.objects.create(user=instance)
        

# Now we will automate the profile 
post_save.connect(create_shipping, sender=User)


# Create Order Model:
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    full_name =models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order - {str(self.id)}"


# Create OrderItem Model:
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=8,decimal_places=2)

    def __str__(self):
        return f"Order Item - {str(self.id)}"