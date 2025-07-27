from django import forms
from .models import OxapayInvoice as Invoice

class PaymentInitiateForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['currency']