from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from datetime import date
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.contrib.auth.models import User
# 1. Ensure login_required is imported
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import *

# --- PROTECTED VIEW ---
@login_required
def make_payment(request):
    if request.method == 'POST':
        try:
            amount_paid_str = request.POST.get('amount_paid', '0')
            try:
                amount_paid = Decimal(amount_paid_str)
            except InvalidOperation:
                return render(request, 'submit_payment.html', {'error': 'Invalid amount paid format.'})

            student_id = request.POST.get('student_id')
            fee_type = request.POST.get('fee_type')
            payment_method = request.POST.get('payment_method')
            receipt_number = request.POST.get('receipt_number')

            student_obj = get_object_or_404(Student, pk=student_id)
            
            Payment.objects.create(
                student=student_obj, 
                fee_type=fee_type,
                amount_paid=amount_paid,
                payment_date=date.today(), 
                payment_method=payment_method,
                receipt_number=receipt_number
            )

            try:
                owing_record = Owing.objects.get(student=student_obj)
                owing_record.amount_owed -= amount_paid
                if owing_record.amount_owed <= Decimal('0.00'):
                    owing_record.delete()
                else:
                    owing_record.save()
            except Owing.DoesNotExist:
                pass 
            
            return redirect('payment_success') 
            
        except Exception as e:
            print(f"Payment processing error: {e}")
            return render(request, 'submit_payment.html', {'error': f'An unexpected error occurred: {e}'})

    return render(request, 'submit_payment.html')

# Public view (Landing page usually doesn't require login)
def home(request):
    return render(request, 'home.html')

# Public view
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # Redirect to the main dashboard after login
            return redirect('main')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')
    return render(request, 'login.html')

# Public view
# --- PROTECTED VIEW ---
@login_required
def about(request):
    return render(request, 'about.html')

# Public view
def student_info(request):
    return render(request, 'student_info.html')

# --- PROTECTED VIEW ---
@login_required
def main(request):
    return render(request, 'main.html')

# --- PROTECTED VIEW ---
@login_required
def payments(request):
    payments = Payment.objects.all().order_by('-payment_date')
    return render(request, 'payments.html', {'Payment': payments})

# --- PROTECTED VIEW ---
@login_required
def reports(request):
    owing_list = Owing.objects.all()
    payment_data = Payment.objects.aggregate(total_payments=Sum('amount_paid'))
    total_payments = payment_data.get('total_payments') or Decimal('0.00')

    owing_data = Owing.objects.aggregate(total_owing=Sum('amount_owed'))
    total_owing = owing_data.get('total_owing') or Decimal('0.00')

    context = {
        'Owing': owing_list,
        'total_payments': total_payments,
        'total_owing': total_owing,
    }
    return render(request, 'reports.html', context)

# --- NEW LOGOUT VIEW ---
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


