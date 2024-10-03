# forms.py
from django import forms
from .models import ContactMessage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class ProductSearchForm(forms.Form):
    zip_code = forms.CharField(required=False)
    city = forms.CharField(required=False)
    address = forms.CharField(required=False)

class GeneralSearchForm(forms.Form):
    value = forms.CharField(required=False)

class PriceRangeFilterForm(forms.Form):
    min_price = forms.DecimalField(min_value=0, required=False, label="Minimum Price")
    max_price = forms.DecimalField(min_value=0, required=False, label="Maximum Price")

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

###
class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True, help_text="Enter your phone number.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            phone_number = self.cleaned_data['phone_number']
            Profile.objects.create(user=user, phone_number=phone_number)
        return user

    
