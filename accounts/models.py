from django.db import models
from .manager import LeaveManager
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.utils import timezone
from .utils import *
import datetime
from .manager import EmployeeManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext as _


# Create your models here.
NONE='none'
SICK = 'sick'
CASUAL = 'casual'
PLANNED = 'planned'
COMPOFF = 'compoff'
WORK_FROM_HOME = 'workfromhome'

LEAVE_TYPE = (
(NONE,'none'),
(CASUAL,'Casual Leave'),
(SICK,'Sick Leave'),

(PLANNED,'Planned Leave'),
(WORK_FROM_HOME,'Work From Home'),
(COMPOFF,'Compensatory Off')
)

DAYS_sick = 7
DAYS_casual = 7
DAYS_planned = 7
# DAYS = 21

class Leave(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
	startdate = models.DateField(verbose_name=_('Start Date'),null=True,blank=False)
	enddate = models.DateField(verbose_name=_('End Date'),null=True,blank=False)
	leavetype = models.CharField(choices=LEAVE_TYPE,max_length=25,default=NONE,null=True,blank=False)
	reason = models.CharField(verbose_name=_('Reason for Leave'),max_length=255,help_text='add additional information for leave',null=False,blank=False,default='Unspecified Reason')
	defaultdays_sick = models.PositiveIntegerField(verbose_name=_('Sick Leave days per year counter'),default=DAYS_sick,null=True,blank=True)
	defaultdays_casual = models.PositiveIntegerField(verbose_name=_('Casual Leave days per year counter'),default=DAYS_casual,null=True,blank=True)
	defaultdays_planned = models.PositiveIntegerField(verbose_name=_('Planned Leave days per year counter'),default=DAYS_planned,null=True,blank=True)


	# hrcomments = models.ForeignKey('CommentLeave') #hide

	status = models.CharField(max_length=12,default='pending') #pending,approved,rejected,cancelled
	is_approved = models.BooleanField(default=False) #hide

	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	created = models.DateTimeField(auto_now=False, auto_now_add=True)


	objects = LeaveManager()


	class Meta:
		verbose_name = _('Leave')
		verbose_name_plural = _('Leaves')
		ordering = ['-created'] #recent objects



	def __str__(self):
		return ('{0} - {1}'.format(self.leavetype,self.user))




	@property
	def pretty_leave(self):
		'''
		i don't like the __str__ of leave object - this is a pretty one :-)
		'''
		leave = self.leavetype
		user = self.user
		employee = user.employee_set.first().get_full_name
		return ('{0} - {1}'.format(employee,leave))



	@property
	def leave_days(self):
		days_count = ''
		startdate = self.startdate
		enddate = self.enddate
		if startdate > enddate:
			return
		dates = (enddate - startdate)
		return dates.days+1 



	@property
	def leave_approved(self):
		return self.is_approved == True




	@property
	def approve_leave(self):
		if not self.is_approved:
			self.is_approved = True
			self.status = 'approved'
			self.save()




	@property
	def unapprove_leave(self):
		if self.is_approved:
			self.is_approved = False
			self.status = 'pending'
			self.save()



	@property
	def leaves_cancel(self):
		if self.is_approved or not self.is_approved:
			self.is_approved = False
			self.status = 'cancelled'
			self.save()



	# def uncancel_leave(self):
	# 	if  self.is_approved or not self.is_approved:
	# 		self.is_approved = False
	# 		self.status = 'pending'
	# 		self.save()



	@property
	def reject_leave(self):
		if self.is_approved or not self.is_approved:
			self.is_approved = False
			self.status = 'rejected'
			self.save()



	@property
	def is_rejected(self):
		return self.status == 'rejected'


# Create your models here.
class Role(models.Model):
    '''
        Role Table eg. Staff,Manager,H.R ...
    '''
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125,null=True,blank=True)

    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)


    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ['name','created']


    def __str__(self):
        return self.name


class Department(models.Model):
    '''
     Department Employee belongs to. eg. Transport, Engineering.
    '''
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125,null=True,blank=True)

    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)


    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        ordering = ['name','created']

    def __str__(self):
        return self.name






class Nationality(models.Model):
    name = models.CharField(max_length=125)
    flag = models.ImageField(null=True,blank=True)#work on path

    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)

    class Meta:
        verbose_name = _('Nationality')
        verbose_name_plural = _('Nationality')
        ordering = ['name','created']

    def __str__(self):
        return self.name





class Religion(models.Model):
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125,null=True,blank=True)

    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)

    class Meta:
        verbose_name = _('Religion')
        verbose_name_plural = _('Religions')
        ordering = ['name','created']

    def __str__(self):
        return self.name




class Bank(models.Model):
    # access table: employee.bank_set.
    employee = models.ForeignKey('Employee',help_text='select employee(s) to add bank account',on_delete=models.CASCADE,null=True,blank=False)
    name = models.CharField(_('Name of Bank'),max_length=125,blank=False,null=True,help_text='')
    account = models.CharField(_('Account Number'),help_text='employee account number',max_length=30,blank=False,null=True)
    branch = models.CharField(_('Branch'),help_text='which branch was the account issue',max_length=125,blank=True,null=True)
    salary = models.DecimalField(_('Starting Salary'),help_text='This is the initial salary of employee',max_digits=16, decimal_places=2,null=True,blank=False)

    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True,null=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True,null=True)


    class Meta:
        verbose_name = _('Bank')
        verbose_name_plural = _('Banks')
        ordering = ['-name','-account']


    def __str__(self):
        return ('{0}'.format(self.name))






class Emergency(models.Model):
    FATHER = 'Father'
    MOTHER = 'Mother'
    SIS = 'Sister'
    BRO = 'Brother'
    UNCLE = 'Uncle'
    AUNTY = 'Aunty'
    HUSBAND = 'Husband'
    WIFE = 'Wife'
    FIANCE = 'Fiance'
    FIANCEE = 'Fiancee'
    COUSIN = 'Cousin'
    NIECE = 'Niece'
    NEPHEW = 'Nephew'
    SON = 'Son'
    DAUGHTER = 'Daughter'

    EMERGENCY_RELATIONSHIP = (
    (FATHER,'Father'),
    (MOTHER,'Mother'),
    (SIS,'Sister'),
    (BRO,'Brother'),
    (UNCLE,'Uncle'),
    (AUNTY,'Aunty'),
    (HUSBAND,'Husband'),
    (WIFE,'Wife'),
    (FIANCE,'Fiance'),
    (COUSIN,'Cousin'),
    (FIANCEE,'Fiancee'),
    (NIECE,'Niece'),
    (NEPHEW,'Nephew'),
    (SON,'Son'),
    (DAUGHTER,'Daughter'),
    )


    # access table: employee.emergency_set.
    employee = models.ForeignKey('Employee',on_delete=models.CASCADE,null=True,blank=True)
    fullname = models.CharField(_('Fullname'),help_text='who should we contact ?',max_length=255,null=True,blank=False)
    tel = PhoneNumberField(default='+233240000000', null = False, blank=False, verbose_name='Phone Number (Example +233240000000)', help_text= 'Enter number with Country Code Eg. +233240000000')
    location = models.CharField(_('Place of Residence'),max_length= 125,null=True,blank=False)
    relationship = models.CharField(_('Relationship with Person'),help_text='Who is this person to you ?',max_length=8,default=FATHER,choices=EMERGENCY_RELATIONSHIP,blank=False,null=True)


    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)

    class Meta:
        verbose_name = 'Emergency'
        verbose_name_plural = 'Emergency'
        ordering = ['-created']


    def __str__(self):
        return self.fullname

    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True,null=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True,null=True)








class Relationship(models.Model):
    MARRIED = 'Married'
    SINGLE = 'Single'
    DIVORCED = 'Divorced'
    WIDOW = 'Widow'
    WIDOWER = 'Widower'

    STATUS = (
    (MARRIED,'Married'),
    (SINGLE,'Single'),
    (DIVORCED,'Divorced'),
    (WIDOW,'Widow'),
    (WIDOWER,'Widower'),
    )

    FATHER = 'Father'
    MOTHER = 'Mother'
    SIS = 'Sister'
    BRO = 'Brother'
    UNCLE = 'Uncle'
    AUNTY = 'Aunty'
    HUSBAND = 'Husband'
    WIFE = 'Wife'
    FIANCE = 'Fiance'
    FIANCEE = 'Fiancee'
    COUSIN = 'Cousin'
    NIECE = 'Niece'
    NEPHEW = 'Nephew'
    SON = 'Son'
    DAUGHTER = 'Daughter'

    NEXTOFKIN_RELATIONSHIP = (
    (FATHER,'Father'),
    (MOTHER,'Mother'),
    (SIS,'Sister'),
    (BRO,'Brother'),
    (UNCLE,'Uncle'),
    (AUNTY,'Aunty'),
    (HUSBAND,'Husband'),
    (WIFE,'Wife'),
    (FIANCE,'Fiance'),
    (COUSIN,'Cousin'),
    (FIANCEE,'Fiancee'),
    (NIECE,'Niece'),
    (NEPHEW,'Nephew'),
    (SON,'Son'),
    (DAUGHTER,'Daughter'),
    )




    # access table: employee.relationship_set.or related_name = 'relation' employee.relation.***
    employee = models.ForeignKey('Employee',on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(_('Marital Status'),max_length=10,default=SINGLE,choices=STATUS,blank=False,null=True)
    spouse = models.CharField(_('Spouse (Fullname)'),max_length=255,blank=True,null=True)
    occupation = models.CharField(_('Occupation'),max_length=125,help_text='spouse occupation',blank=True,null=True)
    tel = PhoneNumberField(default=None, null = True, blank=True, verbose_name='Spouse Phone Number (Example +233240000000)', help_text= 'Enter number with Country Code Eg. +233240000000')
    children = models.PositiveIntegerField(_('Number of Children'),null=True,blank=True,default=0)

    #recently added - 29/03/19
    nextofkin = models.CharField(_('Next of Kin'),max_length=255,blank=False,null=True,help_text='fullname of next of kin')
    contact = PhoneNumberField(verbose_name='Next of Kin Phone Number (Example +233240000000)',null=True,blank=True,help_text='Phone Number of Next of Kin')
    relationship = models.CharField(_('Relationship with Next of Person'),help_text='Who is this person to you ?',max_length=15,choices=NEXTOFKIN_RELATIONSHIP,blank=False,null=True)

    # close recent

    father = models.CharField(_('Father\'s Name'),max_length=255,blank=True,null=True)
    foccupation = models.CharField(_('Father\'s Occupation'),max_length=125,help_text='',blank=True,null=True)

    mother = models.CharField(_('Mother\'s Name'),max_length=255,blank=True,null=True)
    moccupation = models.CharField(_('Mother\'s Occupation'),max_length=125,help_text='',blank=True,null=True)


    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True,null=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True,null=True)

    class Meta:
        verbose_name = 'Relationship'
        verbose_name_plural = 'Relationships'
        ordering = ['created']


    def __str__(self):
        if self.status == 'Married':
            return self.spouse
        return self.status






class Employee(models.Model):

    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    NOT_KNOWN = 'Not Known'

    GENDER = (
    (MALE,'Male'),
    (FEMALE,'Female'),
    (OTHER,'Other'),
    (NOT_KNOWN,'Not Known'),
    )

    MR = 'Mr'
    MRS = 'Mrs'
    MSS = 'Mss'
    DR = 'Dr'
    SIR = 'Sir'
    MADAM = 'Madam'

    TITLE = (
    (MR,'Mr'),
    (MRS,'Mrs'),
    (MSS,'Mss'),
    (DR,'Dr'),
    (SIR,'Sir'),
    (MADAM,'Madam'),
    )


    FULL_TIME = 'Full-Time'
    PART_TIME = 'Part-Time'
    CONTRACT = 'Contract'
    INTERN = 'Intern'

    EMPLOYEETYPE = (
    (FULL_TIME,'Full-Time'),
    (PART_TIME,'Part-Time'),
    (CONTRACT,'Contract'),
    (INTERN,'Intern'),
    )


    OLEVEL = 'O-LEVEL'
    SENIORHIGH = 'Senior High'
    JUNIORHIGH = 'Junior High'
    TERTIARY = 'Tertiary'
    PRIMARY = 'Primary Level'
    OTHER = 'Other'

    EDUCATIONAL_LEVEL = (
    (SENIORHIGH,'Senior High School'),
    (JUNIORHIGH,'Junior High School'),
    (PRIMARY,'Primary School'),
    (TERTIARY,'Tertiary/University/Polytechnic'),
    (OLEVEL,'OLevel'),
    (OTHER,'Other'),
    )


    AHAFO = 'Ahafo'
    ASHANTI = 'Ashanti'
    BONOEAST = 'Bono East'
    BONO = 'Bono'
    CENTRAL = 'Central'
    EASTERN = 'Eastern'
    GREATER = 'Greater Accra'
    NORTHEAST = 'North East'
    NORTHERN = 'Northen'
    OTI = 'Oti'
    SAVANNAH = 'Savannah'
    UPPEREAST = 'Upper East'
    UPPERWEST = 'Upper West'
    VOLTA = 'Volta'
    WESTERNNORTH = 'Western North'
    WESTERN = 'Western'


    GHANA_REGIONS = (
    (AHAFO,'Ahafo'),
    (ASHANTI,'Ashanti'),
    (BONOEAST,'Bono East'),
    (BONO,'Bono'),
    (CENTRAL,'Central'),
    (EASTERN,'Eastern'),
    (GREATER,'Greater Accra'),
    (NORTHEAST,'Northen East'),
    (NORTHERN,'Northen'),
    (OTI,'Oti'),
    (SAVANNAH,'Savannah'),
    (UPPEREAST,'Upper East'),
    (UPPERWEST,'Upper West'),
    (VOLTA,'Volta'),
    (WESTERNNORTH,'Western North'),
    (WESTERN,'Western'),
    )




    # PERSONAL DATA
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    title = models.CharField(_('Title'),max_length=4,default=MR,choices=TITLE,blank=False,null=True)
    image = models.ImageField(_('Profile Image'),upload_to='profiles',blank=True,null=True)#work on path username-date/image
    firstname = models.CharField(_('Firstname'),max_length=125,null=False,blank=False)
    lastname = models.CharField(_('Lastname'),max_length=125,null=False,blank=False)
    # othername = models.CharField(_('Othername (optional)'),max_length=125,null=True,blank=True)
    sex = models.CharField(_('Gender'),max_length=8,default=MALE,choices=GENDER,blank=False)
    email = models.CharField(_('Email (optional)'),max_length=255,default=None,blank=True,null=True)
    tel = PhoneNumberField(default='+233240000000', null = False, blank=False)
    bio = models.CharField(_('Bio'),max_length=255,default='',null=True,blank=True)
    birthday = models.DateField(_('Birthday'),blank=False,null=False)
    # religion = models.ForeignKey(Religion,verbose_name =_('Religion'),on_delete=models.SET_NULL,null=True,default=None)
    # nationality = models.ForeignKey(Nationality,verbose_name =_('Nationality'),on_delete=models.SET_NULL,null=True,default=None)
    hometown = models.CharField(_('Hometown'),max_length=125,null=True,blank=True)
    # region = models.CharField(_('Region'),help_text='what region of the country(Ghana) are you from ?',max_length=20,default=GREATER,choices=GHANA_REGIONS,blank=False,null=True)
    # residence = models.CharField(_('Current Residence'),max_length=125,null=False,blank=False)
    address = models.TextField(_('Address'),max_length=125,null=True,blank=True)

    education = models.CharField(_('Education'),max_length=40,default=SENIORHIGH,choices=EDUCATIONAL_LEVEL,blank=False,null=True)
    lastwork = models.CharField(_('Last Place of Work'),max_length=125,null=True,blank=True)
    position = models.CharField(_('Position Held'),max_length=255,null=True,blank=True)
    # ssnitnumber = models.CharField(_('SSNIT Number'),max_length=30,null=True,blank=True)
    # tinnumber = models.CharField(_('TIN'),max_length=15,null=True,blank=True)

    planned_5_days = models.BooleanField(_("Once applied for 5 days or not?"),default=True,blank=False)

    # employee_type = models.CharField(_('Employee Type'),max_length=20)
    # email_id = models.EmailField(_("Email ID"), max_length=254)
    # reporting_to = models.ForeignKey(Employee,on_delete=models.SET_NULL)

    reporting_to = models.ForeignKey('self', related_name='subordinates', blank=True, null=True, help_text='Reporting To',on_delete=models.SET_NULL)


    last_login=models.DateTimeField(blank=True,null=True)

    # COMPANY DATA
    department =  models.ForeignKey(Department,verbose_name =_('Department'),on_delete=models.SET_NULL,null=True,default=None)
    role =  models.ForeignKey(Role,verbose_name =_('Role'),on_delete=models.SET_NULL,null=True,default=None)
    startdate = models.DateField(_('Employement Date'),help_text='date of employement',blank=False,null=True)
    employeetype = models.CharField(_('Employee Type'),max_length=15,default=FULL_TIME,choices=EMPLOYEETYPE,blank=False,null=True)
    # employeeid = models.CharField(_('Employee ID Number'),max_length=10,null=True,blank=True)
    # dateissued = models.DateField(_('Date Issued'),blank=False,null=True)

    #app related
    is_blocked = models.BooleanField(_('Is Blocked'),help_text='button to toggle employee block and unblock',default=False)
    is_deleted = models.BooleanField(_('Is Deleted'),help_text='button to toggle employee deleted and undelete',default=False)

    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True,null=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True,null=True)


    #PLUG MANAGERS
    objects = EmployeeManager()



    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ['-created']



    def __str__(self):
        return self.get_full_name



    @property
    def get_full_name(self):
        fullname = ''
        firstname = self.firstname
        lastname = self.lastname
        # othername = self.othername

        if (firstname and lastname) is not None:
            fullname = firstname +' '+ lastname
            return fullname
       
        return


    @property
    def get_age(self):
        current_year = datetime.date.today().year
        dateofbirth_year = self.birthday.year
        if dateofbirth_year:
            return current_year - dateofbirth_year
        return



    @property
    def can_apply_leave(self):
        pass




    @property
    def get_pretty_birthday(self):
        if self.birthday:
            return self.birthday.strftime('%A,%d %B') # Thursday,04 May -> staffs age privacy
        return




    @property
    def birthday_today(self):
        '''
        returns True, if birthday is today else False
        '''
        return self.birthday.day == datetime.date.today().day



    @property
    def days_check_date_fade(self):
        '''
        Check if Birthday has already been celebrated ie in the Past     ie. 4th May  & today 8th May 4 < 8 -> past else present or future '''
        return self.birthday.day < datetime.date.today().day #Assumption made,If that day is less than today day,in the past




    def birthday_counter(self):
        '''
        This method counts days to birthday -> 2 day's or 1 day
        '''
        today = datetime.date.today()
        current_year = today.year

        birthday = self.birthday # eg. 5th May 1995

        future_date_of_birth = datetime.date(current_year,birthday.month,birthday.day)#assuming born THIS YEAR ie. 5th May 2019

        if birthday:
            if (future_date_of_birth - today).days > 1:

                return str((future_date_of_birth - today).days) + ' day\'s'

            else:

                return ' tomorrow'

        return





#    def save(self,*args,**kwargs):
#         '''
#         overriding the save method - for every instance that calls the save method
#         perform this action on its employee_id
#         added : March, 03 2019 - 11:08 PM

#         '''
#         # get_id = self.employeeid #grab employee_id number from submitted form field
#         data = code_format(get_id)
#         self.employeeid = data #pass the new code to the employee_id as its orifinal or actual code
#         super().save(*args,**kwargs) # call the parent save method
#         # print(self.employeeid)


class MailingGroup(models.Model):
    group_name = models.CharField(_('Group Name'),max_length=30,blank=False,null=False)

    group_mail = models.EmailField(_('Email'),max_length=255,default=None,)

    is_active = models.BooleanField(_("Is Active"),default=False)

    def __str__(self):
        return self.group_name
