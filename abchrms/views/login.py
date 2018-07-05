from django.shortcuts import render, redirect,get_object_or_404
from django.utils import timezone
import logging
from abchrms.models import Employee
from django.core.exceptions import ValidationError



def loginuser(request):
    if request.method == "POST":
        username = request.POST['lg_username']
        password = request.POST['lg_password']
        if Employee.objects.filter(id=username).exists() and password == '1234':
            return redirect('welcome',emp_id=username)
        else:
#            loginform = request.POST['login_form']
            raise ValidationError({'login_form':'Invalid Username or password'})
    return render(request,'employee/login.html')
