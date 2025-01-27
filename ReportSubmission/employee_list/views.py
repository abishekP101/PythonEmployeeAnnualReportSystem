from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import AnnualReport, Employee
from .forms import AnnualReportForm, EmployeeForm, AnnualReportScoreForm
from django.contrib import messages
from django.contrib.auth.models import User
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Associate the registered user with an employee based on username
            employee = Employee.objects.filter(name=user.username).first()
            if employee:
                employee.user = user
                employee.save()
            login(request, user)
            # Redirect to a pending association page after registration and login
            return redirect('pending_activation')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


# User Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Employee, AnnualReport

@login_required(login_url='/')
def home(request):
    # Ensure that the employee is correctly linked with the user
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        messages.error(request, 'No associated employee profile found.')
        return redirect('home')

    # Fetch the report based on the employee's association with the user
    reports = AnnualReport.objects.filter(employee=employee).order_by('-year')

    # Iterate over reports to check the status and score
    report_data = []
    for report in reports:
        report_status = report.status if report.status == 'viewed' else 'Pending'
        report_data.append({
            'report': report,
            'score': report.score if report.status == 'viewed' else 'Pending',
            'status': report_status
        })

    # Count the total number of employees
    employee_count = Employee.objects.count()

    # Count the total number of reports with status 'submitted' (or whatever status represents submission)
    report_count = AnnualReport.objects.filter(status='submitted').count()

    # Pass the counts and report data to the template
    return render(request, 'home.html', {
        'report_data': report_data,
        'employee_count': employee_count,
        'report_count': report_count,
    })


# Employee List View (Only Accessible by Superusers)
@login_required(login_url='/')
def employee_list(request):
    if not request.user.is_superuser:
        return redirect('home')
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

# List of Annual Reports View (Superuser Access)
@login_required(login_url='/')
def annual_reports_list(request):
    if not request.user.is_superuser:
        return redirect('home')

    # Optionally filter by employee or year
    employee_id = request.GET.get('employee')
    year = request.GET.get('year')
    reports = AnnualReport.objects.all()

    if employee_id:
        reports = reports.filter(employee__id=employee_id)

    if year:
        reports = reports.filter(year=year)

    return render(request, 'annual_reports_list.html', {'reports': reports})

# Add Employee View
@login_required(login_url='/')
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee added successfully!')
            return redirect('employee_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmployeeForm()
    return render(request, 'add_employee.html', {'form': form})

# Edit Employee View (Only Accessible by Superusers)
@login_required(login_url='/')
def edit_employee(request, employee_id):
    if not request.user.is_superuser:
        return redirect('home')
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'edit_employee.html', {'form': form})

# Delete Employee View (Only Accessible by Superusers)
@login_required(login_url='/')
def delete_employee(request, employee_id):
    if not request.user.is_superuser:
        return redirect('home')
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'confirm_delete.html', {'employee': employee})

# Employee Submitting Annual Report
@login_required(login_url='/')
def submit_annual_report(request):
    employee = getattr(request.user, 'employee', None)
    if not employee:
        messages.error(request, 'You are not associated with any employee profile.')
        return redirect('home')

    if request.method == 'POST':
        form = AnnualReportForm(request.POST)
        if form.is_valid():
            annual_report = form.save(commit=False)
            annual_report.employee = employee
            annual_report.save()
            return redirect('home')
    else:
        form = AnnualReportForm()
    return render(request, 'submit_annual_report.html', {'form': form})

# Employee Viewing their Own Report Details
@login_required(login_url='/')
def employee_report_detail(request):
    employee = getattr(request.user, 'employee', None)
    if not employee:
        messages.error(request, 'No associated employee profile found.')
        return redirect('home')

    # Get the most recent annual report of the employee
    try:
        report = AnnualReport.objects.filter(employee=employee).latest('year')
    except AnnualReport.DoesNotExist:
        messages.info(request, 'You have no reports submitted. Please submit one.')
        return redirect('submit_annual_report')

    score = report.score if report.status == 'viewed' else 'Pending'

    return render(request, 'employee_report_detail.html', {'report': report, 'score': score})


# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import AnnualReport
from .forms import AnnualReportScoreForm


def annual_report_detail(request, report_id):
    report = get_object_or_404(AnnualReport, id=report_id)

    if request.method == 'POST':
        form = AnnualReportScoreForm(request.POST)
        if form.is_valid():
            score = form.cleaned_data.get('score')
            report.score = score
            report.status = 'Viewed'  # Change the status after scoring
            report.save()
            return redirect('home')  # Redirect to home or another page after saving the score
    else:
        form = AnnualReportScoreForm()  # Initialize the form for GET request

    context = {
        'report': report,
        'form': form,  # Pass the form to the template
    }
    return render(request, 'annual_report_detail.html', context)


# User Logout
def logout_view(request):
    logout(request)
    return redirect('login')

def pending_activation(request):
    return render(request, 'pending_activation.html')
