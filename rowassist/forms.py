from django import forms
from django.contrib.auth.models import User
from rowassist.models import Athlete, Club, Session, SessionInterval, SessionEntryInterval, SessionEntry
import datetime


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password', 'first_name', 'last_name')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = Athlete
		fields = ('is_coach', 'picture')

class AccountForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email') 

class CreateClubForm(forms.ModelForm):
	class Meta:
		model = Club
		fields = ('name', 'url', 'short_name')

class JoinClubForm(forms.ModelForm):
	class Meta:
		model = Athlete
		fields = ('requested_club',)

class CreateSessionForm(forms.ModelForm):
	date = forms.DateField(initial=datetime.date.today)

	class Meta:
		model = Session
		fields = ('description', 'name', 'distance', 'time', 'rate', 'rest', 'intervalNo', 'date', 'type')

class CreateSessionIntervalForm(forms.ModelForm):
	class Meta:
		model = SessionInterval
		fields = ('distance', 'time', 'rest', 'rate')

		
class AddSessionEntryIntervalForm(forms.ModelForm):
	class Meta:
		model = SessionEntryInterval
		fields = ('time', 'distance', 'strokes_per_minute')


class AddSessionEntryForm(forms.ModelForm):
	class Meta:
		model = SessionEntry
		fields = ('session', 'athlete')
