from django.urls import path
from . import views

urlpatterns = [
    path('<str:store_name>/dashboard/', views.store_dashboard, name='store_dashboard'),
    path('sales/', views.sales_page, name='sales'),
     path('add/', views.add_store, name='add_store'),
    path('list/', views.store_list, name='store_list'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
