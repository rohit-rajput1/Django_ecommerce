from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)

    # Since we don't pularalize the model name, we will add this class Meta to the model.
    class Meta:
        verbose_name_plural = 'Shipping Address'
    
    def __str__(self):
        return f"Shipping Address - {str(self.id)}"