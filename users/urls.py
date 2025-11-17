from django.urls import path
from . import views

urlpatterns = [
    path("shop/", views.shop, name="shop"),
    path("cart/", views.cart, name="cart"),  # <-- lowercase 'cart'
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("order-history/", views.order_history, name="order_history"),
    path("verify/<str:amount>/", views.manual_verify_payment, name="manual_verify_payment"),
]
