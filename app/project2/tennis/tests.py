from django.test import TestCase, RequestFactory, Client
from django.db import IntegrityError
from tennis import models
import datetime
from .views import create_profile, create_product


# test
# Create your tests here.

# http://stackoverflow.com/questions/11170133/using-mysql-with-django-access-denied-for-user-localhost

# NOTE: ALL unit tests must begin with "def test_*"

# As a seller, I should be able to create an account

class CreateAccountTestCase(TestCase):
    def setUp(self):
        self.u = models.Profile(username='test user', first_name='max',
                                last_name='luo', location='Charlottesville', email='maxluo@virginia.edu', active=True,
                                date_joined=datetime.datetime.now())
        self.u.save()
        # try to create an account with no last name
        self.u1 = models.Profile(username='test user1', first_name='arun', location='Cville', email='max@virginia.edu',
                                 active=True, date_joined=datetime.datetime.now())

    def test_account_created(self):
        self.assertEqual(self.u.first_name, 'max')
        self.assertEqual(self.u.last_name, 'luo')

    def account_creation_fail(self):
        with self.assertRaises(IntegrityError):
            self.u1.save()

    def tearDown(self):
        pass


# As a user, I shouldn't be able to make an account if the username is already taken

class DuplicateAccountTestCase(TestCase):
    def setUp(self):
        pass

    def test_success_response(self):
        self.u1 = models.Profile(username='test user', first_name='max',
                                 last_name='luo', location='Charlottesville', email='maxluo@virginia.edu', active=True,
                                 date_joined=datetime.datetime.now())
        self.u1.save();

        # An account with the same username (test user) should not be allowed to be created.
        with self.assertRaises(IntegrityError):
            self.u2 = models.Profile(username='test user', first_name='arun', last_name='luo',
                                     location='Charlottesville', email='maxluo@virginia.edu', active=True,
                                     date_joined=datetime.datetime.now())
            self.u2.save();

    def tearDown(self):
        pass


# As a seller, I should be able to create a product to sell

# NOTE THIS DOESN"T WORK YET... but I'm going to commit my changes so far so you can ask Leandra in OH
class CreateProductTestCase(TestCase):
    def setUp(self):
        client = Client()
        request = client.post('/api/v1/profiles/create',
                              {'username': 'test1', 'first_name': 'arun', 'last_name': 'luo', 'location': 'Blah',
                               'email': 'asd@virginia.edu'})
        create_profile(request)

    def test_success_response(self):
        request_product = client.post('/api/v1/products/1/create',
                                      {'name': 'racquet', 'description': 'nice racquet', 'price': '150'},
                                      content_type = 'text')
        response = create_product(request_product, 1)
        self.assertEquals(response.status_code, 200)

    def tearDown(self):
        pass


"""
class GetOrdersTestCase(TestCase):
    def setUp(self):
        client = Client()
        # create an order
        u1 = models.Profile(username='test user', first_name='max',
                                 last_name='luo', location='Charlottesville', email='maxluo@virginia.edu', active=True,
                                 date_joined=datetime.datetime.now())
        u1.save()
        v = models.Profile.objects.get(pk=1)
        u = models.Order(buyer=v, date_ordered=datetime.datetime.now())
        u.save()

    def test_success_response(self):
        response = client.get('/api/v1/orders/1/retrieve')
        self.assertContains(response, 'resp')
    def tearDown(self):
        pass
"""
