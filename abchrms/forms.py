from django import forms
from abchrms.models import Employee

class DateInput(forms.DateInput):
    input_type = 'date'

class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        exclude = ('created_by','creation_timestamp')
        widgets = {'dob': DateInput(),
                    'marriage_anniv': DateInput()
        }
