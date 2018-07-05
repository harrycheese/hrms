from django.shortcuts import render, redirect,get_object_or_404
from django.utils import timezone
import logging
from abchrms.forms import EmployeeForm
from abchrms.models import Employee
"""
The following views allow a user to Create, Update and Remove
Employee basis the Employee.id Primary Key defined in the
Employee Model
"""

#Using the Logger to display messages in Server Console
#for debugging loops
logger = logging.getLogger(__name__)

def create_emp(request):

    if request.method == "POST":#This if block is where the actual employee is created
        employee = EmployeeForm(request.POST)
        logger.error('firstif in create_emp')
        if employee.is_valid():#This if block validates if there are no validation errors
            logger.error('secondif in create_emp')
            saved_emp = employee.save(commit=False)#commit is set to false so that we can update createdby and created timestamp fields
            saved_emp.created_by = request.user
            saved_emp.creation_timestamp = timezone.now()
            saved_emp.save()
            return redirect('list_emp')
    else: #this else block is where screen is blank form is displayed
        logger.error('else in create_emp')
        employee = EmployeeForm()
    return render(request,'employee/createemp.html',{'employee':employee})


def update_emp(request,pk):
    #gets object basis id field of Employee else if not found returns HTTP404
    emp = get_object_or_404(Employee,id=pk)
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


def welcome(request,emp_id):
    employee=get_object_or_404(Employee,id=emp_id)
    return render(request,'employee/welcome.html',{'employee':employee})
