from django.urls import path
from spms import views

urlpatterns=[
    path('',views.login_page,name='login'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('category_2/',views.category_2,name='category_2'),
    path('category/',views.category,name='category'),
    path('manage_vehicles/',views.manage_vehicles,name='manage_vehicles'),
    path('reports/',views.reports,name='reports'),
    path('search/',views.search,name='search'),
    path('vehicle_entry/',views.vehicle_entry,name='vehicle_entry'),
    path('account_setting/',views.change_password,name='account_setting'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('edit_category/<int:id>/',views.edit_category,name='edit_category'),
    path('delete_category/<int:id>/',views.delete_category,name='delete_category'),
    path('vehicle_entry/',views.vehicle_entry,name='vehicle_entry'),
    path('edit_vehicle/<int:id>/',views.edit_vehicle,name='edit_vehicle'),
    path('delete_vehicle/<int:id>/',views.delete_vehicle,name='delete_vehicle'),
    path('get_vehicle_details/',views.get_vehicle_details,name='get_vehicle_details'),
]