# shop/admin.py
from django.contrib import admin
from .models import Product,Category

@admin.register(Product)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name', 'description')
