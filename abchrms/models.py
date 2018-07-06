from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

#Create your models here.
class Employee(models.Model):
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
    # MARITAL_CHOICE = (
    #         ('True','Married'),
    #         ('False','Unmarried'),
    # )

    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICE)
    dob = models.DateField()
    mobile_number = models.IntegerField()
    personal_email_id = models.EmailField()
    marital_status = models.BooleanField()
    marriage_anniv = models.DateField(null=True,blank=True)
    citizen = models.CharField(max_length=15)
    religion = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=4,choices=BLOOD_GROUP_CHOICE)
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
    EMPLOYMENT_TYPE_CHOICE = (
                ('Full-time','Full-time'),
                ('Contractual','Contractual'),
    )
    CONFIRMATION_STATUS_CHOICE = (
                ('Confirmed','Confirmed'),
                ('Probation','Probation'),
    )

    emp_id = models.ForeignKey('Employee',on_delete=models.CASCADE)
    official_email_id = models.EmailField()
    doj = models.DateField()
    job_band = models.IntegerField()
    designation = models.CharField(max_length=20)
    reporting_manager_emp_id = models.ForeignKey('Employee',related_name='ReportingManager')
    hr_manager_emp_id = models.ForeignKey('Employee',related_name='HRManager')
    emp_type = models.CharField(max_length=20,choices=EMPLOYMENT_TYPE_CHOICE)
    confirmation_status = models.CharField(max_length=20,choices=CONFIRMATION_STATUS_CHOICE)
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

    # def __str__(self):
    #     return self.emp_id.name

    def clean(self):
        errordict = {}
        today = timezone.localdate()
        if (self.doj > today):
            errordict['doj'] = 'Date of Joining cannot be in future'

        # if ((today.year - self.doj.year - ((today.month, today.day) < (self.doj.month, self.doj.day))) >= 1):
        #     errordict['doj'] = 'Enter valid Joining date'

        if(1 > self.job_band > 15):
            errordict['job_band'] = 'Enter valid Job Band between 1 to 15'

        if(self.emp_type not in ('Full-time','full-time','contractual','Contractual')):
            errordict['emp_type'] = 'Valid values are Permanent or Contractual'

        if(self.confirmation_status not in ('Confirmed','confirmed','Probation','probation')):
            errordict['confirmation_status'] = 'Valid values are Confirmed or Probation'

        if(self.confirmation_status in ('confirmed','Confirmed') and self.confirmation_date is None):
            errordict['confirmation_date'] = 'Please enter Confirmation Date since the employee status is confirmed'

        # if(self.confirmation_date > today or self.confirmation_date.year < today.year):
        #     errordict['confirmation_date'] = 'Please enter valid Confirmation Date'

        # if(1 < self.notice_period_in_months < 4):
        #     errordict['notice_period_in_months'] = 'Please Enter Notice period in months'


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
    LEAVE_TYPE_CHOICE = (
                    ('PL','Privelege Leave'),
                    ('CL','Casual Leave'),
                    ('SL','Sick Leave'),
    )
    emp_id = models.ForeignKey('Employee',on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=2,choices=LEAVE_TYPE_CHOICE)
    leave_quota = models.IntegerField()
    leave_availed = models.IntegerField(default=0)
    leave_balance = models.IntegerField()
    leave_carryforward = models.IntegerField(default=0)
    created_by = models.ForeignKey('auth.User')
    creation_timestamp = models.DateTimeField(default=timezone.now)

    def calculate_leave_balance(self):
        '''Re-calculates and sets the correct values for
            all the fields in the Leave Model
        '''
        self.leave_balance = self.leave_quota - self.leave_availed
        self.save()

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
        self.calculate_leave_balance()
        raise ValidationError(errordict)

#    def applyLeave(self):

class LeaveTransaction(models.Model):
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
    emp_id = models.ForeignKey('Employee',on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=2,choices=LEAVE_TYPE_CHOICES)
    from_date = models.DateField()
    to_date = models.DateField()
    no_of_days = models.IntegerField()
    leave_reason = models.CharField(max_length=20,choices=LEAVE_REASON_CHOICES)
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
        if (self.from_date > self.to_date):
             errordict['from_date'] = 'From Date cannot be greater than To date'
        if (self.leave_reason == 'Marriage' and self.emp_id.marital_status == True):
            errordict['leave_reason'] = 'You are already married'
        #Pass the Dictionary to raise ValidationError
        raise ValidationError(errordict)


#
class Dependents(models.Model):
    RELATION_CHOICES=(
                ('spouse','Spouse'),
                ('son','Son'),
                ('daughter','Daughter'),
                ('father','Father'),
                ('mother','Mother'),
    )
    emp_id = models.ForeignKey('Employee',on_delete=models.CASCADE)
    dep_name = models.CharField(max_length=30)
    dep_rel = models.CharField(max_length=20,choices=RELATION_CHOICES)
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

class DependentTransaction(models.Model):
    DEPENDENT_TRANSACTION_TYPE = (
                            ('add','add'),
                            ('remove','remove'),
                            ('edit','edit'),
    )
    emp_id = models.ForeignKey('Employee',on_delete=models.CASCADE)
    dep_id = models.ForeignKey('Dependents',on_delete=models.CASCADE)
    dep_txn_type = models.CharField(max_length=10,choices=DEPENDENT_TRANSACTION_TYPE)
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
class Transactions(models.Model):
    TRANSACTION_TYPE_CHOICE=(
                    ('leave','leave'),
                    ('dependent','dependent'),
    )
    emp_id = models.ForeignKey('Employee',on_delete=models.CASCADE)
    model_foreign_key = models.IntegerField()
    tran_date = models.DateField()
    tran_type = models.CharField(max_length=20,
                        choices=TRANSACTION_TYPE_CHOICE
    )

    def add_ledger(self,emp_id,tran_type,model_foreign_key):
        self.emp_id = emp_id
        self.tran_type = tran_type
        self.model_foreign_key = model_foreign_key
        self.tran_date = timezone.now()
        self.save()

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

class Product(models.Model):
    PRODUCT_VALUES=(
                ('TI','Travel Insurance'),
                ('ULIP','Child Plan'),
                ('EQMF','Equity MF SIP'),
                ('LI','Term Life Insurance'),
    )
    PIFA_CHOICES=(
                ('P','Protecting'),
                ('I','Investing'),
                ('F','Financing'),
                ('A','Advising'),
    )

    product_type = models.CharField(max_length=10,choices=PRODUCT_VALUES)
    product_name = models.CharField(max_length=50)
    product_disp_text = models.TextField()
    product_cat = models.CharField(max_length=1,choices=PIFA_CHOICES)


class RuleEngine(models.Model):
    TRANSACTION_TYPE_CHOICE=(
                    ('leave','leave'),
                    ('dependent','dependent'),
    )
    product=models.CharField(max_length=50)
    txn_type = models.CharField(max_length=20,choices=TRANSACTION_TYPE_CHOICE)
    rules = models.CharField(max_length=500)
