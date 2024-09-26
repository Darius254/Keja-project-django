from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Booking
from .forms import ProductSearchForm, GeneralSearchForm, PriceRangeFilterForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.contrib.auth.decorators import login_required

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})

def home(request):
    form = GeneralSearchForm(request.GET)
    
    if request.method == 'GET' and 'search' in request.GET:
        if form.is_valid():
            search_request = request.GET.urlencode()
            search_keyword = search_request.split('=')[1].replace('+', ' ')
            search_keyword = search_keyword.replace('%2C', ',')
            products = Product.objects.all()

            zip_code_list = list(products.filter(zip_code=search_keyword))
            city_list = list(products.filter(city__icontains=search_keyword))
            address_list = list(products.filter(address__icontains=search_keyword))

            query_params = ''
            if len(zip_code_list) != 0:
                query_params = f'zip_code={zip_code_list[0].zip_code}&city=&address='
            elif len(city_list) != 0:
                query_params = f'zip_code=&city={city_list[0].city}&address='
            elif len(address_list) != 0:
                query_params = f'zip_code=&city=&address={address_list[0].address}'
            return redirect(f'/products/?{query_params}')

    return render(request, 'home.html', {'form': form})

def product_list(request):
    form = ProductSearchForm(request.GET)
    price_filter_form = PriceRangeFilterForm(request.GET)
    products = Product.objects.all()

    if price_filter_form.is_valid():
        min_price = price_filter_form.cleaned_data.get('min_price')
        max_price = price_filter_form.cleaned_data.get('max_price')

        if min_price is not None:
            products = products.filter(price__gte=min_price)
        if max_price is not None:
            products = products.filter(price__lte=max_price)

    if form.is_valid():
        zip_code = form.cleaned_data.get('zip_code')
        city = form.cleaned_data.get('city')
        address = form.cleaned_data.get('address')

        if zip_code:
            products = products.filter(zip_code=zip_code)
        if city:
            products = products.filter(city__icontains=city)
        if address:
            products = products.filter(address__icontains=address)
    
    return render(request, 'product_list.html', {'products': products, 'form': form})

def about_us(request):
    return render(request, 'about_us.html')

def contact_us(request):
    success = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send email (adjust the email settings as needed)
            send_mail(
                f"Contact Form Submission from {name}",
                message,
                email,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            success = True
    else:
        form = ContactForm()
    return render(request, 'contact_us.html', {'form': form, 'success': success})

@login_required  # Ensure the user is logged in before booking
def book_house(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if not product.booked:
        # Create a booking entry
        Booking.objects.create(user=request.user, product=product)
        product.booked = True
        product.save()
    
    return redirect('product_list')

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/book/', views.book_house, name='book_house'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
]
