from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from product import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), 
    path('products/', include('product.urls')),
    path('accounts/', include('accounts.urls')),
#forms

    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
