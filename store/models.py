from django.db import models
from django.conf import settings

class Store(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.store_name


class StoreSales(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    sales_amount = models.DecimalField(max_digits=10, decimal_places=2)
    expenses_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date= models.DateTimeField(auto_now_add= True )

    @property
    def profit(self):
        return self.sales_amount - self.expenses_amount
