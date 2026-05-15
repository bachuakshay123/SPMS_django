from django.shortcuts import render, redirect
from django.contrib import messages

from spms.forms import LoginForm
from spms.forms import ChangePasswordForm
from spms.models import login

import random
from django.http import JsonResponse

def home (request):
    return render(request, 'home.html')
def dashboard (request):
    return render(request, 'dashboard.html')
def category_2 (request):
    return render(request, 'Category_2.html')
def category (request):
    return render(request, 'Category.html')
def manage_vehicles(request):
    return render(request, 'manage_vehicles.html')
def reports (request):
    return render(request, 'reports.html')
def search (request):
    return render(request, 'Search.html')
def vehicle_entry (request):
    return render(request, 'Vehicle_Entry.html')

def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            mobile_number = form.cleaned_data['mobile_number']
            users = login.objects.all()
            valid_user = None
            for user in users:
                if (user.username == username and user.password == password and user.mobile_number == mobile_number):
                    valid_user = user
                    break
            if valid_user:
                request.session['user_id'] = valid_user.id
                return redirect('dashboard')
            else:
                messages.error(
                    request,
                    "Enter Valid Details"
                )
    return render(
        request,
        'home.html',
        {'form': form}
    )

def change_password(request):
    form = ChangePasswordForm()
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            user = login.objects.filter(
                id=user_id
            ).first()
            if user and user.password == current_password:
                if new_password == confirm_password:
                    user.password = new_password
                    user.save()
                    messages.success(
                        request,
                        "Password Changed Successfully"
                    )
                    return redirect('login')
                else:
                    messages.error(
                        request,
                        "New Password and Confirm Password do not match"
                    )
            else:
                messages.error(
                    request,
                    "Current Password Incorrect"
                )
    return render(
        request,
        'account_Setting.html',
        {'form': form}
    )

def forgot_password(request):
    if request.method == "POST":
        mobile_number = request.POST.get('mobile_number')
        user = login.objects.filter(
            mobile_number=mobile_number
        ).first()
        if user:
            otp = random.randint(100000, 999999)
            request.session['reset_mobile'] = mobile_number
            request.session['otp'] = str(otp)
            print("\n===================================")
            print("YOUR OTP IS :", otp)
            print("===================================\n")
            return JsonResponse({
                'status': 'success'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Mobile Number Not Found'
            })


def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        if entered_otp == session_otp:
            return JsonResponse({
                'status': 'success'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid OTP'
            })


def reset_password(request):
    if request.method == "POST":
        new_password = request.POST.get('new_password')
        mobile_number = request.session.get('reset_mobile')
        user = login.objects.filter(
            mobile_number=mobile_number
        ).first()
        if user:
            user.password = new_password
            user.save()
            del request.session['otp']
            del request.session['reset_mobile']
            return JsonResponse({
                'status': 'success'
            })
    return JsonResponse({
        'status': 'error'
    })