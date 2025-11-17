from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings



class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')


class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.item_name}"
    
class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    is_store = models.BooleanField(default=False)

    store_name = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.username
    
