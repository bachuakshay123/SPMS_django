from django.shortcuts import render, redirect
from django.contrib import messages

from spms.forms import LoginForm
from spms.forms import ChangePasswordForm
from spms.models import login

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
    form=LoginForm()
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=login.objects.filter(
                username=username,
                password=password
            ).exists()
        if user:
            return redirect('dashboard')
        else:
            messages.error(
                request,"Invalid Username or Password"
            )
    return render(
        request,'home.html',{'form':form}
    )

def change_password(request):
    form = ChangePasswordForm()
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            user = login.objects.filter(
                password=current_password
            ).first()
            if user:
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