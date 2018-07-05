from django.contrib import admin
from .models import Employee,Employment,Leave,Product,RuleEngine
from django import forms

# Register your models here.



class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

    # def clean(self) :
    #     marital_status = self.cleaned_data.get('marital_status')
    #     marriage_anniv = self.cleaned_data.get('marriage_anniv')
    #     # if self.cleaned_data.get('gender') not in ('m','M','f','F'):
    #     #     raise forms.ValidationError("Gender can only be M or F")
    #     if (marital_status == True and marriage_anniv is None):
    #         raise forms.ValidationError("Marriage Date cannot be null if marital status is true")
    #     return self.cleaned_data

class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeForm
    list_display = ('name','gender','dob','mobile_number','personal_email_id','marital_status','marriage_anniv','citizen','religion','blood_group','created_by','creation_timestamp')

class LeaveForm(forms.ModelForm):
    class Meta:
        model=Leave
        fields=('emp_id','leave_type','leave_quota','leave_availed','created_by')

class LeaveAdmin(admin.ModelAdmin):
    form = LeaveForm
    list_display = ('emp_id','leave_type','leave_quota','leave_balance')


admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Leave,LeaveAdmin)
admin.site.register(Employment)
admin.site.register(Product)
admin.site.register(RuleEngine)
