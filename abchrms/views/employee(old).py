from django.shortcuts import render, redirect
from abchrms.models import Employee
from django.utils import timezone
from django import forms
from django.contrib import auth

def list(request):
   employees = Employee.objects.all()
   if not employees:
        found = len(employees)>0
   else:
        found = False
   return render(request, 'employee/list.html', {'found' : found, 'employees' : employees})

def create(request):
   return render(request, 'employee/create.html')

def save(request):
    employee = Employee()
    employee.name=request.POST.get('name')
    employee.gender=request.POST.get('gender')
    employee.dob=request.POST.get('dob')
    employee.mobile_number=request.POST.get('mobile_number')
    employee.personal_email_id=request.POST.get('personal_email_id')
    employee.marital_status=request.POST.get('marital_status')
    employee.marriage_anniv=request.POST.get('marriage_anniv')
    employee.citizen=request.POST.get('citizen')
    employee.religion=request.POST.get('religion')
    employee.blood_group=request.POST.get('blood_group')
    employee.created_by=request.user
#    employee.creation_timestamp=timezone.now()
    employee.save()
    return redirect('/hrms/list-employees')

def remove(request, employee_id):
   employee = Employee.objects.get(id=employee_id)
   employee.delete()
   return redirect('/hrms/list-employees')

def edit(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    request.session['employee_id'] = employee_id   # put employee to edit in session
    return render(request, 'employee/edit.html', {'employee': employee})

def update(request):
   employee = Employee.objects.get(id=request.session['employee_id'])
   if employee:
        employee.name = request.POST.get('name')
        employee.gender = request.POST.get('gender')
        employee.dob=request.POST.get('dob')
        employee.mobile_number=request.POST.get('mobile_number')
        employee.personal_email_id=request.POST.get('personal_email_id')
        employee.marital_status=request.POST.get('marital_status')
        employee.marriage_anniv=request.POST.get('marriage_anniv')
        employee.citizen=request.POST.get('citizen')
        employee.religion=request.POST.get('religion')
        employee.blood_group=request.POST.get('blood_group')
        employee.created_by=request.user
#        employee.creation_timestamp=timezone.now()
        # try :
        employee.save()
        return redirect('/hrms/list-employees')
        # except forms.ValidationError as e:
        #     redirecturl = '/hrms/edit-employee/'+str(employee.id)
        #     return redirect(request,redirecturl,e)
   else:
       return redirect('/error')
