# forms.py
from django import forms

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