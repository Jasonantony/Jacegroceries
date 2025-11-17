from django.db import models
from django.conf import settings



class Vendor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.store_name
