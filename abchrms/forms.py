from django import forms
from abchrms.models import Employee,Employment,LeaveTransaction

class DateInput(forms.DateInput):
    input_type = 'date'

# class ChoiceInput(forms.ChoiceInput):
#     input_type = 'dropdown'

class EmployeeForm(forms.ModelForm):

    class Meta:
        GENDER_CHOICE = (
                ('M','Male'),
                ('F','Female'),
            )
        BLOOD_GROUP_CHOICE = (
                ('A+','A+'),
                ('B+','B+'),
                ('AB+','AB+'),
                ('A-','A-'),
                ('B-','B-'),
                ('AB-','AB-'),
        )
        MARITAL_CHOICE = (
                ('True','Married'),
                ('False','Unmarried'),
        )
        model = Employee
        exclude = ('created_by','creation_timestamp')
        widgets = {'dob': DateInput(),
                    'marriage_anniv': DateInput(),
                    'gender': forms.Select(choices=GENDER_CHOICE),
                    'blood_group': forms.Select(choices=BLOOD_GROUP_CHOICE),
                    'marital_status': forms.Select(choices=MARITAL_CHOICE)
        }

class EmploymentForm(forms.ModelForm):

    class Meta:
        EMPLOYMENT_TYPE_CHOICE = (
                    ('Full-time','Full-time'),
                    ('Contractual','Contractual'),
        )
        CONFIRMATION_STATUS_CHOICE = (
                    ('Confirmed','Confirmed'),
                    ('Probation','Probation'),
        )
        model = Employment
        exclude = ('emp_id','created_by','creation_timestamp')
        widgets = {
                'doj' : DateInput(),
                'confirmation_date' : DateInput(),
                'emp_type' : forms.Select(choices=EMPLOYMENT_TYPE_CHOICE),
                'confirmation_status' : forms.Select(choices=CONFIRMATION_STATUS_CHOICE)
        }


class LeaveTransactionForm(forms.ModelForm):
     class Meta:
         LEAVE_TYPE_CHOICES = (
                         ('PL','Privelege Leave'),
                         ('CL','Casual Leave'),
                         ('SL','Sick Leave'),
         )
         LEAVE_REASON_CHOICES = (
                         ('Personal','Personal'),
                         ('Vacation','Vacation'),
                         ('Marriage','Marriage'),
                         ('Sick Leave','Sick Leave'),
                         ('Family','Family'),
                         ('Others','Others'),
         )
         model = LeaveTransaction
         exclude = ('emp_id','created_by','creation_timestamp','no_of_days')
         widgets = {
                'from_date' : DateInput(),
                'to_date' : DateInput(),
                'leave_reason' : forms.Select(choices=LEAVE_REASON_CHOICES),
                'leave_type' : forms.Select(choices = LEAVE_TYPE_CHOICES)
         }
