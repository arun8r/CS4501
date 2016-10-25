from django.db import models
from django.core.validators import validate_email
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Profile(models.Model):
	#id field inherently present in django
	username = models.CharField(max_length = 50, unique = True, ) 
	first_name = models.CharField(max_length = 50)
	last_name = models.CharField(max_length = 50)
	email = models.EmailField(max_length = 254, unique = True, validators = [validate_email, ])
	active = models.BooleanField()
	date_joined = models.DateTimeField()
	location = models.CharField(max_length = 50)
	password = models.CharField(max_length = 96)


class Order(models.Model):
	#id field inherently present in django
	buyer = models.ForeignKey(Profile)
	date_ordered = models.DateTimeField()


class Product(models.Model):
	#id field inherently present in django
	name = models.CharField(max_length = 50)
	description = models.CharField(max_length = 1000)
	price = models.DecimalField(max_digits = 8, decimal_places = 2)
	date_posted = models.DateTimeField()
	sold = models.BooleanField()
	seller = models.ForeignKey(Profile)
	order = models.ForeignKey(Order, blank = True, null = True)


class Review(models.Model):
	author = models.ForeignKey(Profile)
	description = models.CharField(max_length = 1000)
	date_written = models.DateTimeField()
	rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5),])
	product = models.ForeignKey(Product)
	
class Authenticator(models.Model):
	user_id = models.PositiveIntegerField()
	authenticator = models.CharField(max_length = 255, primary_key = True)
	date_created = models.DateTimeField()
