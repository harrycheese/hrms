from django.shortcuts import render, redirect
from django.utils import timezone
import logging
from abchrms.forms import EmployeeForm,EmploymentForm
from abchrms.models import Employee,Employment
from django.http import Http404
"""
The following views allow a user to add or edit
Employment details  basis the Employment.emp_id.id
which is Foreign Key of Employee Model
"""

logger = logging.getLogger(__name__)

def update_employment(request,emp_id):
    #The first try block is to catch DoesNotExist errors
    #thrown by the get() if employee id passed DoesNotExist
    try:
        employ = Employment.objects.get(emp_id=emp_id)
        if request.method=="POST":
        #The first if block is entered if employee exists and
        #the form field is submitted after an update
            employment = EmploymentForm(request.POST,instance=employ)
            logger.error('first if in create employment')
            if employment.is_valid():
            #the second if block validates if any errors
                logger.error('second if in update employment')
                saved_employment = employment.save(commit=False)
                saved_employment.created_by = request.user
                saved_employment.creation_timestamp = timezone.now()
                saved_employment.save()
                return redirect('list_employment')
        else:
        #the else block is entered if employee and employment
        #record also exists
            logger.error('else in update employment')
            employment=EmploymentForm(instance=employ)
    except Employment.DoesNotExist :
    #the except block is entered if employment record does not exist
        if request.method=="POST":
            employment = EmploymentForm(request.POST)
            logger.error("first if of Except")
            if employment.is_valid():
                logger.error("second if of except")
                saved_employment = employment.save(commit=False)
                saved_employment.emp_id = Employee.objects.get(id=emp_id)
                saved_employment.created_by = request.user
                saved_employment.creation_timestamp = timezone.now()
                saved_employment.save()
                return redirect('list_employment')
        else:
        #the else block is run for the employment form to load if
        #there is no employment information for the particular employee
            logger.error("ELse of except")
            try:
            #this try catches if employee does not exist and will
            #give 404 page error if employee does not exist
                employee = Employee.objects.get(id=emp_id)
                employment=EmploymentForm()
            except Employee.DoesNotExist:
                raise Http404("No Employee exists with Employee id "+emp_id)
    return render(request,'employee/edit-employment-details.html',{'employment':employment})

def list_employment(request,emp_id):
    employments = Employment.objects.filter(emp_id=emp_id)
#    employee = Employee.objects.get(id=employment.emp_id)
    if employments.exists():
        found = True
    else:
        found = False
    return render(request,'employee/employment-details.html',{'found' : found, 'employments' : employments,'employee_id':emp_id})
