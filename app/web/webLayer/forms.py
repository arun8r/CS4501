from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate, get_user_model, login


class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)


class UserSignUpForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)
	fname = forms.CharField()
	lname = forms.CharField()
	email = forms.CharField()
	location = forms.CharField()
	
	

