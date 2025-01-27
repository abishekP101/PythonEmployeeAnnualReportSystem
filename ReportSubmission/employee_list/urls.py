from django.urls import path
from . import views

urlpatterns = [
    # User authentication views
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Employee home page
    path('home/', views.home, name='home'),

    # Employee report submission
    path('submit_annual_report/', views.submit_annual_report, name='submit_annual_report'),
    path('pending-activation/', views.pending_activation, name='pending_activation'),
    # Employee report detail (view by employee)
    path('employee/report/', views.employee_report_detail, name='employee_report_detail'),

    # Superuser-only employee management
    path('employee/', views.employee_list, name='employee_list'),
    path('employee/add/', views.add_employee, name='add_employee'),
    path('employee/edit/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('employee/delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),

    # Annual report list (superuser)
    path('annual-reports/', views.annual_reports_list, name='annual_reports_list'),
    path('annual-report/<int:report_id>/', views.annual_report_detail, name='annual_report_detail'),



]
