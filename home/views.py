from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Product,Purchase
from django.contrib.auth.decorators import login_required
from datetime import timedelta, date
from django.contrib.auth import get_user_model


User = get_user_model()


def custom_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)

            # admin
            if user.is_admin:
                return redirect('admin_dashboard')

            # vendor
            elif user.is_vendor:
                return redirect('vendor_dashboard')

            # store
            elif user.is_store:
                store_name = user.store_name or user.username.split('@')[0]
                return redirect(f"/store/{store_name}/dashboard/")

            # default
            else:
                return redirect('home')

        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")
    return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("signup")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        # assign roles
        if role == "admin":
            user.is_admin = True
            user.is_superuser = True
            user.is_staff = True

        if role == "vendor":
            user.is_vendor = True

        if role == "store":
            user.is_store = True
            user.store_name = email.split('@')[0]

        user.save()

        messages.success(request, "Account created! Please login.")
        return redirect("login")

    return render(request, "signup.html")
# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    cart[product_id] = cart.get(product_id, 0) + 1

    request.session['cart'] = cart
    return redirect('shop')

def shop(request):
    products = Product.objects.all()
    return render(request, "home/shop.html", {"products": products})

def sales(request):
    return render (request, "adminis/sales.html")

def vendor_dashboard(request):
    return render(request, "vendor/vendor_dashboard.html")

@login_required
def dashboard(request):
    user = request.user

    # Get past purchases
    history = Purchase.objects.filter(user=user).order_by('-date')

    # Suggest items based on items purchased in the last 30 days
    one_month_ago = date.today() - timedelta(days=30)
    last_month_items = Purchase.objects.filter(user=user, date__gte=one_month_ago)

    # Take unique item names as monthly suggestion
    suggested_items = last_month_items.values_list("item_name", flat=True).distinct()

    context = {
        "user": user,
        "history": history,
        "suggestions": suggested_items,
    }

    return render(request, "dashboard.html", context)

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')