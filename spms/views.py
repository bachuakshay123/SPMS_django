from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone

from spms.forms import LoginForm
from spms.forms import ChangePasswordForm
from spms.forms import CategoryForm
from spms.forms import VehicleForm
from spms.models import login, Category, Vehicle

import random
from django.http import JsonResponse

def home (request):
    return render(request, 'home.html')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('login')
    parked_vehicles = Vehicle.objects.filter(
        parking_status='Parked'
    ).count()
    departed_vehicles = Vehicle.objects.filter(
        parking_status='Leaved'
    ).count()
    total_category = Category.objects.count()
    total_records = Vehicle.objects.count()
    total_earnings = 0
    paid_vehicles = Vehicle.objects.filter(
        payment_status='Paid'
    )
    for i in paid_vehicles:
        total_earnings += i.parking_charge
    total_slots = 0
    categories = Category.objects.all()
    for i in categories:
        total_slots += i.vehicle_limit
    return render(
        request,
        'dashboard.html',
        {
            'parked_vehicles': parked_vehicles,
            'departed_vehicles': departed_vehicles,
            'total_category': total_category,
            'total_earnings': total_earnings,
            'total_records': total_records,
            'total_slots': total_slots
        }
    )

def reports(request):
    if 'user_id' not in request.session:
        return redirect('login')
    data = Vehicle.objects.all()
    category = Category.objects.all()
    if request.method == "POST":
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        vehicle_type = request.POST.get('vehicle_type')
        vehicle_number = request.POST.get('vehicle_number')
        if vehicle_number:
            data = data.filter(
                vehicle_number__icontains=vehicle_number
                )
        if from_date and to_date:
            data = data.filter(
                arrival_time__date__range=[
                    from_date,
                    to_date
                ]
            )
        if vehicle_type and vehicle_type != "All":
            data = data.filter(
                vehicle_type__id=vehicle_type
            )
    total_vehicles = data.count()
    total_revenue = 0
    wrong_parking = data.filter(
        wrong_parking=True
    ).count()
    pending_payments = data.filter(
        payment_status='Pending'
    ).count()
    for i in data:
        total_revenue += i.parking_charge
    return render(
        request,
        'reports.html',
        {
            'data': data,
            'category': category,
            'total_vehicles': total_vehicles,
            'total_revenue': total_revenue,
            'wrong_parking': wrong_parking,
            'pending_payments': pending_payments
        }
    )

def search(request):
    if 'user_id' not in request.session:
        return redirect('login')
    data = None
    query = ""
    if request.method == "POST":
        query = request.POST.get('search')
        data = Vehicle.objects.filter(
            vehicle_number__icontains=query
        )
    return render(
        request,
        'Search.html',
        {
            'data': data,
            'query': query
        }
    )


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
    if 'user_id' not in request.session:
        return redirect('login')
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

def category(request):
    if 'user_id' not in request.session:
        return redirect('login')
    form = CategoryForm()
    data = Category.objects.all()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Category Added Successfully")
            return redirect('category')
    return render(
        request,
        'Category.html',
        {
            'form': form,
            'data': data
        }
    )

def edit_category(request, id):
    edit_data = Category.objects.get(id=id)
    form = CategoryForm(instance=edit_data)
    if request.method == "POST":
        form = CategoryForm(
            request.POST,
            instance=edit_data
        )
        if form.is_valid():
            form.save()
            messages.success(request,"Category Updated Successfully")
            return redirect('category')
    return render(
        request,
        'Category.html',
        {
            'form': form
        }
    )

def delete_category(request, id):
    data = Category.objects.get(id=id)
    data.delete()
    messages.success(request,"Category Deleted Successfully")
    return redirect('category')

def category_status(request, id):
    data = Category.objects.get(id=id)
    if data.status == True:
        data.status = False
    else:
        data.status = True
    data.save()
    return redirect('category')

def vehicle_entry(request):
    if 'user_id' not in request.session:
        return redirect('login')
    form = VehicleForm()
    data = Vehicle.objects.all()
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save()
            category = vehicle.vehicle_type
            total_parked = Vehicle.objects.filter(vehicle_type=category,parking_status='Parked').count()
            if total_parked >= category.vehicle_limit:
                category.status = False
                category.save()
            messages.success(request,"Vehicle Added Successfully")
            return redirect('vehicle_entry')
    return render(
        request,
        'Vehicle_Entry.html',
        {
            'form': form,
            'data': data
        }
    )

def edit_vehicle(request, id):
    edit_data = Vehicle.objects.get(id=id)
    form = VehicleForm(instance=edit_data)
    if request.method == "POST":
        form = VehicleForm(
            request.POST,
            instance=edit_data
        )
        if form.is_valid():
            form.save()
            messages.success(request,"Vehicle Updated Successfully")
            return redirect('vehicle_entry')
    return render(
        request,
        'Vehicle_Entry.html',
        {
            'form': form
        }
    )

def delete_vehicle(request, id):
    data = Vehicle.objects.get(id=id)
    data.delete()
    messages.success(request,"Vehicle Deleted Successfully")
    return redirect('vehicle_entry')
def get_vehicle_details(request):
    vehicle_type_id = request.GET.get('vehicle_type_id')
    category = Category.objects.get(
        id=vehicle_type_id
    )
    data = {
        'area_number':
        category.parking_area_number,
        'parking_charge':
        str(category.parking_charge)
    }
    return JsonResponse(data)

def vehicle_done(request, id):
    vehicle = Vehicle.objects.get(id=id)
    vehicle.parking_status = 'Leaved'
    vehicle.payment_status = 'Paid'
    vehicle.departure_time = timezone.now()
    vehicle.save()
    category = vehicle.vehicle_type
    total_parked = Vehicle.objects.filter(vehicle_type=category,parking_status='Parked').count()
    if total_parked < category.vehicle_limit:
        category.status = True
        category.save()
        messages.success(request,"Vehicle Exited Successfully")
        return redirect('manage_vehicles')

def manage_vehicles(request):
    if 'user_id' not in request.session:
        return redirect('login')
    data = Vehicle.objects.all()
    return render(
        request,
        'manage_vehicles.html',
        {
            'data': data
        }
    )

def logout_page(request):
    request.session.flush()
    return redirect('login')

