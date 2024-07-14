from django.contrib import admin
from .models import Product
from .models import ContactMessage

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price') 
    search_fields = ('title',)  
    list_display = ('title', 'price', 'city', 'booked')  # Display the booked field in the admin panel
    list_filter = ('booked',)  # Add a filter to easily filter booked houses     

admin.site.register(Product, ProductAdmin)


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'sent_at')
    search_fields = ('name', 'email')

admin.site.register(ContactMessage, ContactMessageAdmin)
