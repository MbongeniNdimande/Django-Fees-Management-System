from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student_id', 'amount_paid,' 'payment_date', 'payment_method', 'receipt_number']