from django.urls import path
from spms import views

urlpatterns=[
    path('',views.home,name='home'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('account_setting/',views.account_setting,name='account_setting'),
    path('category_2/',views.category_2,name='category_2'),
    path('category/',views.category,name='category'),
    path('manage_vehicles/',views.manage_vehicles,name='manage_vehicles'),
    path('reports/',views.reports,name='reports'),
    path('search/',views.search,name='search'),
    path('vehicle_entry/',views.vehicle_entry,name='vehicle_entry'),
]