from django.shortcuts import render, redirect
from django.utils import timezone
import logging
from abchrms.forms import EmployeeForm,EmploymentForm
from abchrms.models import Employee,Employment


logger = logging.getLogger(__name__)

# def create_employment(request):
#     if request.method=="POST":
#         employment = EmploymentForm(request.POST)
#         logger.error('first if in create employment')
#         if employment.is_valid():
#             logger.error('second if in create employment')
#             saved_employment = employment.save(commit=False)
#             saved_employment.created_by = request.user
#             saved_employment.creation_timestamp = timezone.now()
#             saved_employment.save()
#             return redirect('list_employment')
#     else:
#         logger.error('else in create employment')
#         employment=EmploymentForm()
#     return render(request,'employee/create-employment-details.html',{'employment':employment})


def update_employment(request,emp_id):
    try:
        employ = Employment.objects.get(emp_id=emp_id)
        if request.method=="POST":
            employment = EmploymentForm(request.POST,instance=employ)
            logger.error('first if in create employment')
            if employment.is_valid():
                logger.error('second if in update employment')
                saved_employment = employment.save(commit=False)
                saved_employment.created_by = request.user
                saved_employment.creation_timestamp = timezone.now()
                saved_employment.save()
                return redirect('list_employment')
        else:
            logger.error('else in update employment')
            employment=EmploymentForm(instance=employ)
    except Employment.DoesNotExist :
        if request.method=="POST":
            employment = EmploymentForm(request.POST)
            logger.error("first if of Except")
            if employment.is_valid():
                logger.error("second if of except")
                saved_employment = employment.save(commit=False)
                try:
                    saved_employment.emp_id = Employee.objects.get(id=emp_id)
                    saved_employment.created_by = request.user
                    saved_employment.creation_timestamp = timezone.now()
                    saved_employment.save()
                    return redirect('list_employment')
                except Exception as e:
                    raise e
        else:
            logger.error("ELse of except")
            employment=EmploymentForm()
    return render(request,'employee/edit-employment-details.html',{'employment':employment})

def list_employment(request):
    employment = Employment.objects.order_by('-creation_timestamp')
#    employee = Employee.objects.get(id=employment.emp_id)
    if not employment:
        found = len(employment)>0
    else:
        found = False
    return render(request,'employee/employment-details.html',{'found' : found, 'employment' : employment})
