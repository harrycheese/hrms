from django.contrib import admin
from .models import Employee,Employment
from django import forms

# Register your models here.

admin.site.register(Employment)

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

admin.site.register(Employee,EmployeeAdmin)
