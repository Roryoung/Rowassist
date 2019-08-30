from django import forms
from django.contrib.auth.models import User

from RA.models import UserProfile, Club

from registration.forms import RegistrationFormUniqueEmail

class registratonForm(RegistrationFormUniqueEmail):
	firstName = forms.CharField()
	lastName = forms.CharField()

	def __init__(self, *args, **kwargs):
		super(registratonForm, self).__init__(*args, **kwargs)
		self.fields['firstName'].widget.attrs['class'] = 'validate'
		self.fields['lastName'].widget.attrs['class'] = 'validate'
		self.fields['username'].widget.attrs['class'] = 'validate'
		self.fields['email'].widget.attrs['class'] = 'validate'
		self.fields['password1'].widget.attrs['class'] = 'validate'
		self.fields['password2'].widget.attrs['class'] = 'validate'

class joinClubForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('requestedClub',)

class createClubForm(forms.ModelForm):
	class Meta:
		model = Club
		fields = ('name', 'shortName',)

	def __init__(self, *args, **kwargs):
		super(createClubForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs['class'] = 'validate'
		self.fields['shortName'].widget.attrs['class'] = 'validate'



