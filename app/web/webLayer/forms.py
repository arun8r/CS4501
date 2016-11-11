from django import forms


class UserLoginForm(forms.Form):
	username = forms.CharField(max_length = 50)
	password = forms.CharField(widget = forms.PasswordInput)

# Do not include fields active and date_joined, set automatically when user presses submit
class UserSignUpForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)
	fname = forms.CharField()
	lname = forms.CharField()
	email = forms.CharField()
	location = forms.CharField()

class ProductCreationForm(forms.Form):
	name = forms.CharField(max_length = 100)
	description = forms.CharField(max_length = 1000)
	price = forms.DecimalField(max_digits = 8, decimal_places = 2)

class SearchForm(forms.Form):
	query = forms.CharField(max_length = 100)


