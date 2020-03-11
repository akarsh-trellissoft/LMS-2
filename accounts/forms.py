from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User,Group
from django import forms

from .models import Leave, Employee
from .models import *
from django.forms import ModelForm
import datetime

class createUserForm(UserCreationForm):
	groups = forms.ModelChoiceField(queryset=Group.objects.all(),required=True)
	class Meta:
		model = User
		fields = ['username','email','password1','password2','groups']
		widgets={
			'groups': forms.Select,
		}


		

class loginUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','password']

class DateInput(forms.DateInput):
    input_type = 'date'

class LeaveCreationForm(ModelForm):
	reason = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 27})) ## 33 previous
	class Meta:
		model = Leave
		fields = ['startdate','enddate','leavetype','reason']
		widgets = {
            'startdate': DateInput(),
			'enddate' : DateInput()
        }

	def clean_enddate(self):
		enddate = self.cleaned_data['enddate']
		startdate = self.cleaned_data['startdate']
		today_date = datetime.date.today()

		# if (startdate or enddate) < today_date:# both dates must not be in the past
		# 	raise forms.ValidationError("You are not genius. You can not go back in time :p")

		if startdate >= enddate:# TRUE -> FUTURE DATE > PAST DATE,FALSE other wise
			raise forms.ValidationError("Selected dates are wrong")

		return enddate


class EmployeeEditForm(forms.ModelForm):
	# employeeid = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'please enter 5 characters without RGL or slashes eg. A0025'}))
	image = forms.ImageField(widget=forms.FileInput(attrs={'onchange':'previewImage(this);'}))
	class Meta:
		model = Employee
		exclude = ['is_blocked','is_deleted','created','updated','planned_5_days','user']
		widgets = {
				'bio':forms.Textarea(attrs={'cols':10,'rows':10}),
				'birthday': DateInput(),
				'startdate': DateInput(),
				# 'image': forms.FileInput(attrs={'onchange':'previewImage(this);'})
		}


class EmployeeCreationForm(forms.ModelForm):
	# employeeid = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'please enter 5 characters without RGL or slashes eg. A0025'}))
	image = forms.ImageField(widget=forms.FileInput(attrs={'onchange':'previewImage(this);'}))
	class Meta:
		model = Employee
		exclude = ['is_blocked','is_deleted','created','updated','planned_5_days']
		widgets = {
				'bio':forms.Textarea(attrs={'cols':10,'rows':10}),
				'birthday': DateInput(),
				'startdate': DateInput()
		}
