from django.shortcuts import render, redirect,get_object_or_404
from django.utils import timezone
import logging
from abchrms.forms import LeaveTransactionForm
from abchrms.models import LeaveTransaction,Leave,Employee

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
                return redirect('display_leave',emp_id=emp_id)
    else:
        leavetransaction = LeaveTransactionForm()
        return render(request,'employee/applyleave.html'
                    ,{'leavetransaction':leavetransaction}
                )

def display_leave(request,emp_id):
    leaves = Leave.objects.filter(emp_id=emp_id)
    if leaves.exists():
        found = True
        leavedetails = LeaveTransaction.objects.filter(emp_id=emp_id)
    else:
        found = False
        leavedetails = False
    return render(request,'employee/displayleave.html',{'found':found,'leaves':leaves,'leavedetails':leavedetails})
