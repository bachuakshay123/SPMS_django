from django.shortcuts import render
def home (request):
    return render(request, 'home.html')
def dashboard (request):
    return render(request, 'dashboard.html')
def account_setting (request):
    return render(request, 'account_setting.html')
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