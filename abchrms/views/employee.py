from django.shortcuts import render, redirect
from django.utils import timezone
import logging
from abchrms.forms import EmployeeForm
from abchrms.models import Employee


logger = logging.getLogger(__name__)

def create_emp(request):

    if request.method == "POST":
        employee = EmployeeForm(request.POST)
        logger.error('firstif in create_emp')
        if employee.is_valid():
            logger.error('secondif in create_emp')
            saved_emp = employee.save(commit=False)
            saved_emp.created_by = request.user
            saved_emp.creation_timestamp = timezone.now()
            saved_emp.save()
            return redirect('list_emp')
    else:
        logger.error('else in create_emp')
        employee = EmployeeForm()
    return render(request,'employee/createemp.html',{'employee':employee})


def update_emp(request,pk):
    emp = Employee.objects.get(id=pk)
    if request.method == "POST":
        logger.error('firstif')
        employee = EmployeeForm(request.POST, instance=emp)
        if employee.is_valid():
            logger.error('secondif')
            saved_emp = employee.save(commit=False)
            saved_emp.created_by = request.user
            saved_emp.creation_timestamp = timezone.now()
            saved_emp.save()
            return redirect('list_emp')
    else:
        logger.error('insideelse')
        employee = EmployeeForm(instance=emp)
    return render(request,'employee/createemp.html',{'employee':employee})

def list_emp(request):
   employees = Employee.objects.order_by('-creation_timestamp')
   if not employees:
        found = len(employees)>0
   else:
        found = False
   return render(request, 'employee/list.html', {'found' : found, 'employees' : employees})

def remove_emp(request, employee_id):
   employee = Employee.objects.get(id=employee_id)
   employee.delete()
   return redirect('list_emp')
