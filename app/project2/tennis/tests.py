from django.test import TestCase, RequestFactory, Client
from django.db import IntegrityError
from tennis import models
import datetime
from django.core.urlresolvers import reverse
import urllib.request
import urllib.parse
import json
import logging



class CreateProfileTestCase(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		pass
        
	def test_success_response(self):
		post_data = {'username': 'TestUser', 'first_name': 'max', 'last_name': 'luo', 'location': 'Cville', 'email': 'maxo@virginia.edu', 'password':'password'}
		c = Client()
		response = c.post('/api/v1/profiles/create', post_data)
		json_obj = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_obj["ok"], True) 
	def test_error_response(self):
		#test error message (error message is universal so one test should be sufficient, but can be added for each model method in the future)
		post_data = {'username': 'TestUser', 'last_name': 'luo', 'location': 'Cville', 'email': 'maxo@virginia.edu', 'password':'password'}
		c = Client()
		response = c.post('/api/v1/profiles/create', post_data)
		json_obj = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_obj["ok"], False) 
	def tearDown(self):
		pass  


class UpdateProfileTestCase(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		pass
		
	def test_success_response(self):
		post_data = {'username': 'TestUser', 'first_name': 'max', 'last_name': 'luo', 'location': 'Cville', 'email': 'maxo@virginia.edu', 'password':'password'}
		c = Client()
		response = c.post('/api/v1/profiles/create', post_data)
		i = json.loads((response.content).decode("utf-8"))["resp"]["profile_id"]
		post_data = {"location": "China"}
		response = c.post('/api/v1/profiles/' + str(i) + '/update', post_data)
		json_obj = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_obj["ok"], True) 
		
	def tearDown(self):
		pass

class CreateProductTestCase(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		pass
	def test_success_response(self):
		post_data = {'username': 'TestUser', 'first_name': 'max', 'last_name': 'luo', 'location': 'Cville', 'email': 'maxo@virginia.edu', 'password':'password'}
		c = Client()
		response = c.post('/api/v1/profiles/create', post_data)
		i = json.loads((response.content).decode("utf-8"))["resp"]["profile_id"]
		post_data = {'name': 'racquet', 'description': 'great racquet', 'price': '150'}
		response = c.post('/api/v1/products/' + str(i) + '/create', post_data)
		json_obj = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_obj["ok"], True) 
	def tearDown(self):
		pass



class RetrieveProductTestCase(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		pass
	def test_success_response(self):
		post_data = {'username': 'TestUser', 'first_name': 'max', 'last_name': 'luo', 'location': 'Cville', 'email': 'maxo@virginia.edu', 'password':'password'}
		c = Client()
		response = c.post('/api/v1/profiles/create', post_data)
		i = json.loads((response.content).decode("utf-8"))["resp"]["profile_id"]
		post_data = {'name': 'racquet', 'description': 'great racquet', 'price': '150'}
		response = c.post('/api/v1/products/' + str(i) + '/create', post_data)
		j = json.loads((response.content).decode("utf-8"))["resp"]["product_id"]
		response = c.get('/api/v1/products/' + str(j) + '/retrieve')
		json_obj = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_obj["ok"], True) 
	def tearDown(self):
		pass



class UpdateProductTestCase(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		pass
	def test_success_response(self):
		post_data = {'username': 'TestUser', 'first_name': 'max', 'last_name': 'luo', 'location': 'Cville', 'email': 'maxo@virginia.edu', 'password':'password'}
		c = Client()
		response = c.post('/api/v1/profiles/create', post_data)
		i = json.loads((response.content).decode("utf-8"))["resp"]["profile_id"]
		post_data = {'name': 'racquet', 'description': 'great racquet', 'price': '150'}
		response = c.post('/api/v1/products/' + str(i) + '/create', post_data)
		j = json.loads((response.content).decode("utf-8"))["resp"]["product_id"]
		post_data = {'description': 'Greatest racquet ever', 'price': '200'}
		response = c.post('/api/v1/products/' + str(j) + '/update', post_data)
		json_obj = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_obj["ok"], True) 
	def tearDown(self):
		pass

class DeleteProductTestCase(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		pass
	def test_success_response(self):
		post_data = {'username': 'TestUser', 'first_name': 'max', 'last_name': 'luo', 'location': 'Cville', 'email': 'maxo@virginia.edu', 'password':'password'}
		c = Client()
		response = c.post('/api/v1/profiles/create', post_data)
		i = json.loads((response.content).decode("utf-8"))["resp"]["profile_id"]
		post_data = {'name': 'racquet', 'description': 'great racquet', 'price': '150'}
		response = c.post('/api/v1/products/' + str(i) + '/create', post_data)
		j = json.loads((response.content).decode("utf-8"))["resp"]["product_id"]
		response = c.post('/api/v1/products/' + str(j) + '/delete')
		json_obj = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_obj["ok"], True) 
	def tearDown(self):
		pass

class CreateOrderTestCase(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		pass
	def test_success_response(self):
		post_data = {'username': 'TestUser', 'first_name': 'max', 'last_name': 'luo', 'location': 'Cville', 'email': 'maxo@virginia.edu', 'password':'password'}
		c = Client()
		response = c.post('/api/v1/profiles/create', post_data)
		i = json.loads((response.content).decode("utf-8"))["resp"]["profile_id"]

		response = c.post('/api/v1/orders/' + str(i) + '/create')
		json_obj = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_obj["ok"], True) 
	def tearDown(self):
		pass

class RetrieveOrderTestCase(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		pass
	def test_success_response(self):
		post_data = {'username': 'TestUser', 'first_name': 'max', 'last_name': 'luo', 'location': 'Cville', 'email': 'maxo@virginia.edu', 'password':'password'}
		c = Client()
		response = c.post('/api/v1/profiles/create', post_data)
		i = json.loads((response.content).decode("utf-8"))["resp"]["profile_id"]

		response = c.post('/api/v1/orders/' + str(i) + '/create')
		j = json.loads((response.content).decode("utf-8"))["resp"]["order_id"]


		response = c.get('/api/v1/orders/' + str(j) + '/retrieve')        
		json_obj = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_obj["ok"], True) 
	def tearDown(self):
		pass



class CreateReviewTestCase(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		pass
	def test_success_response(self):
		post_data = {'username': 'TestUser', 'first_name': 'max', 'last_name': 'luo', 'location': 'Cville', 'email': 'maxo@virginia.edu', 'password':'password'}
		c = Client()
		response = c.post('/api/v1/profiles/create', post_data)
		i = json.loads((response.content).decode("utf-8"))["resp"]["profile_id"]
		
		post_data = {'name': 'racquet', 'description': 'great racquet', 'price': '150'}
		response = c.post('/api/v1/products/' + str(i) + '/create', post_data)
		j = json.loads((response.content).decode("utf-8"))["resp"]["product_id"]

		post_data = {'description': 'A fantastic racquet', 'rating': '5'}
		response = c.post('/api/v1/reviews/' + str(i) + '/' + str(j) + '/create', post_data)
		json_obj = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_obj["ok"], True) 



		json_obj = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_obj["ok"], True) 


	def tearDown(self):
		pass



class RetrieveReviewTestCase(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		pass

	def test_success_response(self):
		post_data = {'username': 'TestUser', 'first_name': 'max', 'last_name': 'luo', 'location': 'Cville', 'email': 'maxo@virginia.edu', 'password':'password'}
		c = Client()
		response = c.post('/api/v1/profiles/create', post_data)
		i = json.loads((response.content).decode("utf-8"))["resp"]["profile_id"]
		
		post_data = {'name': 'racquet', 'description': 'great racquet', 'price': '150'}
		response = c.post('/api/v1/products/' + str(i) + '/create', post_data)
		j = json.loads((response.content).decode("utf-8"))["resp"]["product_id"]

		post_data = {'description': 'A fantastic racquet', 'rating': '5'}
		response = c.post('/api/v1/reviews/' + str(i) + '/' + str(j) + '/create', post_data)
		k = json.loads((response.content).decode("utf-8"))["resp"]["review_id"]

		response = c.get('/api/v1/reviews/' + str(k) + '/retrieve')
		json_obj = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_obj["ok"], True) 


	def tearDown(self):
		pass



class UpdateReviewTestCase(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		pass

	def test_success_response(self):
		post_data = {'username': 'TestUser', 'first_name': 'max', 'last_name': 'luo', 'location': 'Cville', 'email': 'maxo@virginia.edu', 'password':'password'}
		c = Client()
		response = c.post('/api/v1/profiles/create', post_data)
		i = json.loads((response.content).decode("utf-8"))["resp"]["profile_id"]
		
		post_data = {'name': 'racquet', 'description': 'great racquet', 'price': '150'}
		response = c.post('/api/v1/products/' + str(i) + '/create', post_data)
		j = json.loads((response.content).decode("utf-8"))["resp"]["product_id"]

		post_data = {'description': 'A fantastic racquet', 'rating': '5'}
		response = c.post('/api/v1/reviews/' + str(i) + '/' + str(j) + '/create', post_data)
		k = json.loads((response.content).decode("utf-8"))["resp"]["review_id"]


		post_data = {'description': 'This racquet is a fake!!!!! Changing rating.', 'rating':'1'}
		response = c.post('/api/v1/reviews/' + str(k) + '/update', post_data)
		json_obj = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_obj["ok"], True) 





	def tearDown(self):
		pass

class DeleteReviewTestCase(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		pass

	def test_success_response(self):
		post_data = {'username': 'TestUser', 'first_name': 'max', 'last_name': 'luo', 'location': 'Cville', 'email': 'maxo@virginia.edu', 'password':'password'}
		c = Client()
		response = c.post('/api/v1/profiles/create', post_data)
		i = json.loads((response.content).decode("utf-8"))["resp"]["profile_id"]
		
		post_data = {'name': 'racquet', 'description': 'great racquet', 'price': '150'}
		response = c.post('/api/v1/products/' + str(i) + '/create', post_data)
		j = json.loads((response.content).decode("utf-8"))["resp"]["product_id"]

		post_data = {'description': 'A fantastic racquet', 'rating': '5'}
		response = c.post('/api/v1/reviews/' + str(i) + '/' + str(j) + '/create', post_data)
		k = json.loads((response.content).decode("utf-8"))["resp"]["review_id"]

		response = c.post('/api/v1/reviews/' + str(k) + '/delete')
		json_obj = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_obj["ok"], True) 


	def tearDown(self):
		pass

class CreateAuthenticatorTestCase(TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		pass
	def test_success_response(self):
		post_data = {'username': 'TestUser', 'first_name': 'max', 'last_name': 'luo', 'location': 'Cville', 'email': 'maxo@virginia.edu', 'password':'password'}
		c = Client()
		response = c.post('/api/v1/profiles/create', post_data)
		
		post_data = {'username': 'TestUser', 'password':'password'}
		response = c.post('/api/v1/authentication/create', post_data)
		json_obj = json.loads((response.content).decode("utf-8"))
		self.assertEquals(json_obj["ok"], True) 
	def tearDown(self):
		pass
