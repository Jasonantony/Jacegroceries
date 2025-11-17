from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CartItem, Order, Product, Cart, Category
import qrcode, io, base64

# -------------------------------
# Shop View
# -------------------------------
@login_required
def shop(request):
    products = Product.objects.all()
    return render(request, "users/shop.html", {"products": products})

# -------------------------------
# Add to Cart
# -------------------------------
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')  # Redirect to cart page

# -------------------------------
# Cart View
# -------------------------------
@login_required
def cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()  # CartItem queryset
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, "users/cart.html", {
        "cart": cart,
        "items": items,
        "total": total,
    })

# -------------------------------
# Remove Item from Cart
# -------------------------------
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart!")
    return redirect("cart")  # Redirect to correct cart view

# -------------------------------
# Checkout & Payment
# -------------------------------
@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if cart.items.count() == 0:
        messages.error(request, "Cart is empty!")
        return redirect("shop")

    total = cart.total

    # Generate QR code
    upi_link = f"upi://pay?pa=yourupi@ok&pn=Jace%20Groceries&am={total}&cu=INR"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(upi_link)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_url = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"

    if request.method == "POST":
        order = Order.objects.create(user=request.user, total_amount=total)
        for item in cart.items.all():
            order.items.add(item)
        order.save()
        cart.items.all().delete()
        messages.success(request, "Order placed!")
        return redirect("order_history")

    return render(request, "users/qr_payment.html", {"cart_total": total, "qr_url": qr_url})

# -------------------------------
# Order History
# -------------------------------
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "users/order_history.html", {"orders": orders})

# -------------------------------
# Manual Payment Verification
# -------------------------------
@login_required
def manual_verify_payment(request, amount):
    amount = float(amount)
    orders = Order.objects.filter(user=request.user, total_amount=amount)
    for order in orders:
        order.status = "Paid"
        order.save()
    messages.success(request, "Payment verified successfully!")
    return redirect("order_history")
