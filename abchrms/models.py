from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

#Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1)
    dob = models.DateField()
    mobile_number = models.IntegerField()
    personal_email_id = models.EmailField()
    marital_status = models.BooleanField()
    marriage_anniv = models.DateField(null=True,blank=True)
    citizen = models.CharField(max_length=15)
    religion = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=4)
    created_by = models.ForeignKey('auth.User')
    creation_timestamp = models.DateTimeField(default=timezone.now)

    def clean(self):
        errordict = {}
        today = timezone.localdate()

        if self.gender not in ('m','M','f','F'):
            errordict['gender'] = 'Gender can only be M or F'

        if (self.marital_status == True and self.marriage_anniv is None):
            errordict['marriage_anniv'] = 'Marriage Date cannot be null if marital status is true'

        if (self.mobile_number < 1000000000 or self.mobile_number > 9999999999 ):
            errordict['mobile_number'] = 'Enter valid Mobile Number. Don\'t add Country code'

        if (self.blood_group not in ('A+','A-','B+','B-','AB+','AB-','O+','O-')):
            errordict['blood_group'] = 'Enter Valid Blood group. Valid Values are A+,A-,B+,B-,AB+,AB-,O+,O-'

        if ((today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))) < 18):
            errordict['dob'] = 'Employee must be atleast 18 years old'

        if (self.dob > today or today.year-self.dob.year > 60):
            errordict['dob'] = 'Enter valid Date of Birth'



        #Pass the Dictionary to raise ValidationError
        raise ValidationError(errordict)


    def calculate_age(born):
        today = timezone.localdate()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    #Overriding the default save function with a call to full_clean() function which in return
    #calls the clean() function that has all the custom validations on each model field
    def save(self,*args,**kwargs):
        self.full_clean()
        return super(Employee,self).save(*args,**kwargs)

    #This publish() is only for django admin screen
    def publish(self):
        # try :
        #     self.full_clean()
        # except ValidationError as e:
        #     non_field_errors = e.message_dict[NON_FIELD_ERRORS]
        self.creation_timestamp = timezone.now()
        self.save()

    #This __str__() is only for django admin screen
    def __str__(self):
        return self.name

#
#
class Employment(models.Model):
    emp_id = models.ForeignKey('Employee',on_delete=models.CASCADE)
    official_email_id = models.EmailField()
    doj = models.DateField()
    job_band = models.IntegerField()
    designation = models.CharField(max_length=20)
    reporting_manager_emp_id = models.ForeignKey('Employee',related_name='ReportingManager')
    hr_manager_emp_id = models.ForeignKey('Employee',related_name='HRManager')
    emp_type = models.CharField(max_length=20)
    confirmation_status = models.CharField(max_length=20)
    confirmation_date = models.DateField(blank=True, null=True)
    notice_period_in_months = models.IntegerField()
    department = models.CharField(max_length=30)
    location = models.CharField(max_length=20)
    created_by = models.ForeignKey('auth.User')
    creation_timestamp = models.DateTimeField(default=timezone.now)

    def publish(self):
        try :
            self.full_clean()
        except ValidationError as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
        self.save()

    def __str__(self):
        return self.emp_id.name

    def clean(self):
        errordict = {}
        today = timezone.localdate()
        if (self.doj > today):
            errordict['doj'] = 'Date of Joining cannot be in future'

        if ((today.year - self.doj.year - ((today.month, today.day) < (self.doj.month, self.doj.day))) >= 1):
            errordict['doj'] = 'Enter valid Joining date'

        if(1 > self.job.band > 15):
            errordict['job_band'] = 'Enter valid Job Band between 1 to 15'

        if(self.emp_type not in ('Permanent','permanent','contractual','Contractual')):
            errordict['emp_type'] = 'Valid values are Permanent or Contractual'

        if(self.confirmation_status not in ('Confirmed','confirmed','Probation','probation')):
            errordict['confirmation_status'] = 'Valid values are Confirmed or Probation'

        if(self.confirmation_status in ('confirmed','Confirmed') and self.confirmation_date is None):
            errordict['confirmation_date'] = 'Please enter Confirmation Date since the employee status is confirmed'

        if(self.confirmation_date > today or self.confirmation_date.year < today.year):
            errordict['confirmation_date'] = 'Please enter valid Confirmation Date'

        if(1 < self.notice_period_in_months < 4):
            errordict['notice_period_in_months'] = 'Please Enter Notice period in months'


        #Pass the Dictionary to raise ValidationError
        raise ValidationError(errordict)

#
#
#
class Salary(models.Model):
    emp_id = models.ForeignKey('Employee',on_delete=models.CASCADE)
    basic = models.FloatField()
    hra = models.FloatField()
    special = models.FloatField()
    education = models.FloatField()
    car_allow = models.FloatField()
    pf = models.FloatField()
    lta = models.FloatField()
    others = models.FloatField()
    annual_bonus = models.FloatField()
    vpay = models.FloatField()
    effective_from = models.DateField()
    created_by = models.ForeignKey('auth.User')
    creation_timestamp = models.DateTimeField(default=timezone.now)

    def publish(self):
        try :
            self.full_clean()
        except ValidationError as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
        self.save()

    def __str__(self):
        return self.emp_id.name

    def clean(self):
        errordict = {}
        today = timezone.localdate()
        # if (self.doj > today):
        #     errordict['doj'] = 'Date of Joining cannot be in future'

        #Pass the Dictionary to raise ValidationError
        raise ValidationError(errordict)

#
#
class Financials(models.Model):
    emp_id = models.ForeignKey('Employee',on_delete=models.CASCADE)
    account_no = models.IntegerField()
    ifsc_code = models.IntegerField()
    bank_name = models.CharField(max_length=15)
    bank_account_type = models.CharField(max_length=10)
    bank_holder_name = models.CharField(max_length=50)
    created_by = models.ForeignKey('auth.User')
    creation_timestamp = models.DateTimeField(default=timezone.now)

    def publish(self):
        try :
            self.full_clean()
        except ValidationError as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
        self.save()

    def __str__(self):
        return self.emp_id.name

    def clean(self):
        errordict = {}
        today = timezone.localdate()
        # if (self.doj > today):
        #     errordict['doj'] = 'Date of Joining cannot be in future'

        #Pass the Dictionary to raise ValidationError
        raise ValidationError(errordict)

#
class Education(models.Model):
    emp_id = models.ForeignKey('Employee',on_delete=models.CASCADE)
    qualification = models.CharField(max_length=30)
    year_of_passing = models.IntegerField()
    university = models.CharField(max_length=50)
    created_by = models.ForeignKey('auth.User')
    creation_timestamp = models.DateTimeField(default=timezone.now)

    def publish(self):
        try :
            self.full_clean()
        except ValidationError as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
        self.save()

    def __str__(self):
        return self.emp_id.name

    def clean(self):
        errordict = {}
        today = timezone.localdate()
        # if (self.doj > today):
        #     errordict['doj'] = 'Date of Joining cannot be in future'

        #Pass the Dictionary to raise ValidationError
        raise ValidationError(errordict)

#
class Leave(models.Model):
    emp_id = models.ForeignKey('Employee',on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=10)
    leave_quota = models.IntegerField()
    leave_availed = models.IntegerField()
    leave_balance = models.IntegerField()
    leave_carryforward = models.IntegerField()
    created_by = models.ForeignKey('auth.User')
    creation_timestamp = models.DateTimeField(default=timezone.now)

    def publish(self):
        try :
            self.full_clean()
        except ValidationError as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
        self.save()

    def __str__(self):
        return self.emp_id.name

    def clean(self):
        errordict = {}
        today = timezone.localdate()
        # if (self.doj > today):
        #     errordict['doj'] = 'Date of Joining cannot be in future'

        #Pass the Dictionary to raise ValidationError
        raise ValidationError(errordict)

#
class Dependents(models.Model):
    emp_id = models.ForeignKey('Employee',on_delete=models.CASCADE)
    dep_name = models.CharField(max_length=30)
    dep_rel = models.CharField(max_length=20)
    dep_dob = models.DateField()
    effective_from = models.DateField(default=timezone.now)
    active_flag = models.BooleanField()
    created_by = models.ForeignKey('auth.User')
    creation_timestamp = models.DateTimeField(default=timezone.now)

    def publish(self):
        try :
            self.full_clean()
        except ValidationError as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
        self.save()

    def __str__(self):
        return self.emp_id.name

    def clean(self):
        errordict = {}
        today = timezone.localdate()
        # if (self.doj > today):
        #     errordict['doj'] = 'Date of Joining cannot be in future'

        #Pass the Dictionary to raise ValidationError
        raise ValidationError(errordict)

#
class Address(models.Model):
    emp_id = models.ForeignKey('Employee',on_delete=models.CASCADE)
    add_type = models.CharField(max_length=10)
    address_line = models.TextField()
    area = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    pincode = models.IntegerField()
    active_flag=models.BooleanField()
    effective_from = models.DateField(default=timezone.now)
    created_by = models.ForeignKey('auth.User')
    creation_timestamp = models.DateTimeField(default=timezone.now)

    def publish(self):
        try :
            self.full_clean()
        except ValidationError as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
        self.save()

    def __str__(self):
        return self.emp_id.name

    def clean(self):
        errordict = {}
        today = timezone.localdate()
        # if (self.doj > today):
        #     errordict['doj'] = 'Date of Joining cannot be in future'

        #Pass the Dictionary to raise ValidationError
        raise ValidationError(errordict)

#
class Attendance(models.Model):
    emp_id = models.ForeignKey('Employee',on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    day_off_flag = models.BooleanField()
    check_in_timestamp = models.DateTimeField()
    created_by = models.ForeignKey('auth.User')
    creation_timestamp = models.DateTimeField(default=timezone.now)

    def publish(self):
        try :
            self.full_clean()
        except ValidationError as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
        self.save()

    def __str__(self):
        return self.emp_id.name

    def clean(self):
        errordict = {}
        today = timezone.localdate()
        # if (self.doj > today):
        #     errordict['doj'] = 'Date of Joining cannot be in future'

        #Pass the Dictionary to raise ValidationError
        raise ValidationError(errordict)

#
class Transactons(models.Model):
    emp_id = models.ForeignKey('Employee',on_delete=models.CASCADE)
    model_foreign_key = models.IntegerField()
    tran_date = models.DateField()
    def publish(self):
        try :
            self.full_clean()
        except ValidationError as e:
            non_field_errors = e.message_dict[NON_FIELD_ERRORS]
        self.save()

    def __str__(self):
        return self.emp_id.name

    def clean(self):
        errordict = {}
        today = timezone.localdate()
        # if (self.doj > today):
        #     errordict['doj'] = 'Date of Joining cannot be in future'

        #Pass the Dictionary to raise ValidationError
        raise ValidationError(errordict)
