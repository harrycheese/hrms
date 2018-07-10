from django.shortcuts import render, redirect,get_object_or_404
from django.utils import timezone
import logging
from itertools import chain
from abchrms.forms import LeaveTransactionForm
from abchrms.models import LeaveTransaction,Leave,Employee,Transactions,Product,RuleEngine,Employment

"""
The following view allows a user to mark leave
"""

logger=logging.getLogger(__name__)

def apply_leave(request,emp_id):
    if request.method == "POST":
        leavetransaction = LeaveTransactionForm(request.POST)
        if leavetransaction.is_valid():
            saved_leavetransaction = leavetransaction.save(commit=False)
            leave = get_object_or_404(
                                    Leave,
                                    emp_id = emp_id,
                                    leave_type = saved_leavetransaction.leave_type
                                )
            saved_leavetransaction.no_of_days = (saved_leavetransaction.to_date-saved_leavetransaction.from_date).days
            if(leave.leave_balance <= saved_leavetransaction.no_of_days):
                raise ValidationError({'leave_type':'You do not have sufficient leave balance'})
            else:
                leave.leave_balance = leave.leave_quota - saved_leavetransaction.no_of_days
                leave.leave_availed = saved_leavetransaction.no_of_days
#                leave.calculate_leave_balance()
                saved_leavetransaction.emp_id = Employee.objects.get(id=emp_id)
#                saved_leavetransaction.no_of_days = saved_leavetransaction.from_date-leavetransaction.to_date
                saved_leavetransaction.created_by=request.user
                saved_leavetransaction.creation_timestamp = timezone.now()
                saved_leavetransaction.save()
                leave.save()
                transaction = Transactions()
                transaction.add_ledger(emp_id=Employee.objects.get(id=emp_id),
                                    tran_type = 'leave',
                                    model_foreign_key = saved_leavetransaction.id
                )
                return redirect('leave_details',pk=saved_leavetransaction.id)
    else:
        leavetransaction = LeaveTransactionForm()
        return render(request,'employee/applyleave.html',
                        {'leavetransaction':leavetransaction,'employee':Employee.objects.get(id=emp_id)}
                )

def display_leave(request,emp_id):
    leaves = Leave.objects.filter(emp_id=emp_id)
    if leaves.exists():
        found = True
        leavedetails = LeaveTransaction.objects.filter(emp_id=emp_id)
    else:
        found = False
        leavedetails = False
    return render(request,'employee/displayleave.html',{'found':found,'leaves':leaves,'leavedetails':leavedetails,'employee':Employee.objects.get(id=emp_id)})

def display_leavetxn(request,pk):
    leavetxn = get_object_or_404(LeaveTransaction,id=pk)
    employee = leavetxn.emp_id
    employment = get_object_or_404(Employment,emp_id = leavetxn.emp_id)
    rules = RuleEngine.objects.filter(txn_type='leave')
    ti_products = Product.objects.filter(product_type = 'TI')
    li_products = Product.objects.filter(product_type = 'LI')
    pl_products = Product.objects.filter(product_type = 'PL')
    empty_prod = {}
    if ti_products.exists() and leavetxn.leave_type == "PL" and leavetxn.leave_reason == "Vacation":
        return render(request,'employee/displayleavetxn.html',{'leavetxn':leavetxn,'employee':employee,'rules':rules,'products':ti_products})
    elif li_products.exists() and leavetxn.leave_type == 'SL' and leavetxn.leave_reason == 'Sick Leave':
        return render(request,'employee/displayleavetxn.html',{'leavetxn':leavetxn,'employee':employee,'rules':rules,'products':li_products})
    elif pl_products.exists() and leavetxn.leave_type in ('PL','CL') and employment.job_band > 9:
        return render(request,'employee/displayleavetxn.html',{'leavetxn':leavetxn,'employee':employee,'rules':rules,'products':list(chain(pl_products,ti_products))})
    return render(request,'employee/displayleavetxn.html',{'leavetxn':leavetxn,'employee':employee,'rules':rules,'products':empty_prod})
