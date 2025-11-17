from django.shortcuts import render
from django.shortcuts import render, redirect
from adminis.forms import ProductForm
from users.models import Product


# Create your views here.
def admin_dashboard(request):
    return render(request, 'adminis/dashboard.html')


def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'adminis/add_product.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'adminis/product_list.html', {'products': products})

