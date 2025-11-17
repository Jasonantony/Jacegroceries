from django.shortcuts import render,redirect
from .models import StoreSales
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from adminis.models import Store
from .forms import StoreForm
from adminis.models import Store, Landlord, VendorRegistration, HiringRequest, Firing


def store_dashboard(request, store_name):
    return render(request, "store/home.html", {"store_name": store_name})

def sales_page(request):

    # Total stores
    total_stores = Store.objects.count()

    # Calculate totals
    totals = StoreSales.objects.aggregate(
        total_sales=Sum('sales_amount'),
        total_expenses=Sum('expenses_amount'),
    )

    total_sales = totals['total_sales'] or 0
    total_expenses = totals['total_expenses'] or 0
    total_profit = total_sales - total_expenses

    # Store-wise breakdown
    store_stats = StoreSales.objects.values(
        'store__store_name'
    ).annotate(
        store_sales=Sum('sales_amount'),
        store_expenses=Sum('expenses_amount'),
        store_profit=Sum(
            ExpressionWrapper(
                F('sales_amount') - F('expenses_amount'),
                output_field=DecimalField()
            )
        )
    )

    context = {
        'total_stores': total_stores,
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'total_profit': total_profit,
        'store_stats': store_stats
    }

    return render(request, 'store/sales_dashboard.html', context)


def add_store(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store_list')  # redirect after saving
    else:
        form = StoreForm()
    return render(request, 'store/add_store.html', {'form': form})

def store_list(request):

    stores = Store.objects.all()
    return render(request, 'store/store_list.html', {'stores': stores})



def admin_dashboard(request):
    stores = Store.objects.all()
    landlords = Landlord.objects.all()
    vendors = VendorRegistration.objects.all()
    hires = HiringRequest.objects.all()
    terminations = Firing.objects.all()

    context = {
        'stores': stores,
        'landlords': landlords,
        'vendors': vendors,
        'hires': hires,
        'terminations': terminations,
    }
    return render(request, "adminis/dashboard.html", context)