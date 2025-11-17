from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path("about/", views.about, name='about'),
    path("shop/", views.shop, name="shop"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
     path('login/', views.custom_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('venor_dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('adminis/', include('adminis.urls')),
    path('logout/',views.logout_view, name='logout'),
    path('custom_login/', views.custom_login, name='custom_login'),
    path('sales',views.sales,name='sales'),
]