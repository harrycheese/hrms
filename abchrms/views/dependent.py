from django.shortcuts import render, redirect,get_object_or_404
from django.utils import timezone
import logging
from abchrms.forms import DependentsForm
from abchrms.models import Dependents,Employee,Transactions,DependentTransaction

"""
The following view allows a user to add dependents
"""

logger=logging.getLogger(__name__)

def add_dependent(request,emp_id):
    if request.method == "POST":
        dependent = DependentsForm(request.POST)
        if dependent.is_valid():
            savedependent = dependent.save(commit=False)
            savedependent.emp_id = Employee.objects.get(id=emp_id)
            savedependent.effective_from = timezone.now()
            savedependent.active_flag = True
            savedependent.created_by = request.user
            savedependent.creation_timestamp = timezone.now()
            savedependent.save()
            deptran = DependentTransaction()
            deptran.emp_id = Employee.objects.get(id=emp_id)
            deptran.dep_id = savedependent
            deptran.dep_txn_type = 'add'
            deptran.save()
            transaction = Transactions()
            transaction.add_ledger(emp_id=Employee.objects.get(id=emp_id),
                                tran_type = 'dependent',
                                model_foreign_key = deptran.id
            )
            return redirect('list_dependent',emp_id=emp_id)
    else:
        dependent = DependentsForm()
    return render(request,'employee/editdependent.html',{'dependent':dependent,'employee':Employee.objects.get(id=emp_id)})

def edit_dependent(request,emp_id,pk):
    dep = get_object_or_404(Dependents,emp_id=emp_id,id=pk)
    if request.method == "POST":
        dependent = DependentsForm(request.POST,instance=dep)
        if dependent.is_valid():
            savedependent = dependent.save(commit=False)
            savedependent.emp_id = Employee.objects.get(id=emp_id)
            savedependent.effective_from = timezone.now()
            savedependent.active_flag = True
            savedependent.created_by = request.user
            savedependent.creation_timestamp = timezone.now()
            deptran = DependentTransaction()
            deptran.emp_id = Employee.objects.get(id=emp_id)
            deptran.dep_id = savedependent
            deptran.dep_txn_type = 'edit'
            savedependent.save()
            deptran.save()
            transaction = Transactions()
            transaction.add_ledger(emp_id=Employee.objects.get(id=emp_id),
                                tran_type = 'dependent',
                                model_foreign_key = deptran.id
            )
            return redirect('list_dependent',emp_id=emp_id)
    else:
        dependent = DependentsForm(instance=dep)
    return render(request,'employee/editdependent.html',{'dependent':dependent,'employee':Employee.objects.get(id=emp_id)})

def display_dependent(request,emp_id):
    dependents = Dependents.objects.filter(emp_id=emp_id)
    if dependents.exists():
        found = True
    else:
        found = False
    return render(request,'employee/displaydependent.html',{'dependents':dependents,'found':found,'emp_id':emp_id,'employee':Employee.objects.get(id=emp_id)})

# def remove_dependent(request,emp_id,pk):
#     dependents = Dependent.objects.filter(emp_id=emp_id)
#     if dependent.exists():
#         dependents.

def display_dependenttxn(request,pk):
    dependenttxn = get_object_or_404(DependentTransaction,id=pk)
    employee = get_object_or_404(Employee,id=dependenttxn.emp_id.id)
    return render(request,'employee/displaydependenttxn.html',{'dependenttxn':dependenttxn,'employee':employee})
