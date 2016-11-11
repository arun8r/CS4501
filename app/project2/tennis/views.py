import datetime
from django.http import JsonResponse
from django.contrib.auth import hashers
from django.forms.models import model_to_dict
from django import db
from tennis import models
from django.shortcuts import render
from django.core import serializers
from django.contrib.auth import hashers
import random
from project2 import settings
import os
import hmac

# PROFILE API
#-------------------------------------------------------------------------------------------------------------#
def create_profile(request):
    if request.method != 'POST':
        return _error_response(request, "Must make POST request.")
    if 'username' not in request.POST or 'first_name' not in request.POST or 'last_name' not in request.POST or 'email' not in request.POST or 'location' not in request.POST or 'password' not in request.POST:
        missing = ""
        if 'username' not in request.POST:
            missing += 'username '
        if 'first_name' not in request.POST:
            missing += 'first_name '
        if 'last_name' not in request.POST:
            missing += 'last_name '
        if 'email' not in request.POST:
            missing += 'email '
        if 'location' not in request.POST:
            missing += 'location '
        if 'password' not in request.POST:
            missing += 'password '
            
        return _error_response(request, "Missing required fields: " + missing)

    u = models.Profile(username=request.POST['username'], first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], active=False, date_joined=datetime.datetime.now(), location=request.POST['location'], password = hashers.make_password(request.POST['password']))
    
    try:
        u.save()
    except db.Error:
        return _error_response(request, str(db.Error))
    return _success_response(request, {'profile_id': u.pk})


def retrieve_profile(request, profile_id):
    if request.method != 'GET':
        return _error_response(request, "Must make GET request.")

    try:
        u = models.Profile.objects.get(pk=profile_id)
    except models.Profile.DoesNotExist:
        return _error_response(request, "Profile not found.")

    return _success_response(request, {'username': u.username,      \
                                       'first_name': u.first_name,          \
                                       'last_name': u.last_name,          \
                                       'email': u.email, 			\
                                       'active': u.active,    \
                                       'date_joined': u.date_joined, 	\
                                       'location': u.location })


def update_profile(request, profile_id):
    if request.method != 'POST':
        return _error_response(request, "Must make POST request.")

    try:
        u = models.Profile.objects.get(pk=profile_id)
    except models.Profile.DoesNotExist:
        return _error_response(request, "Profile not found.")

    changed = False 
    #can't change username or email or date_joined
    if 'first_name' in request.POST:
        u.first_name = request.POST['first_name']
        changed = True
    if 'last_name' in request.POST:
        u.last_name = request.POST['last_name']
        changed = True
    if 'active' in request.POST:
        u.active = request.POST['active']
        changed = True
    if 'location' in request.POST:
        u.location = request.POST['location']        
        changed = True        

    if not changed:
        return _error_response(request, "No fields updated.")

    u.save()
    return _success_response(request)


#deleting users does not need to be accomodated for.


#PRODUCT API
#-------------------------------------------------------------------------------------------------------------#
def create_product(request, seller_id):
    if request.method != 'POST':
        return _error_response(request, "Must make POST request.")
    if 'name' not in request.POST or 'description' not in request.POST or 'price' not in request.POST:
        return _error_response(request, "Missing required fields.")   
    try:
        v = models.Profile.objects.get(pk=seller_id)
    except models.Profile.DoesNotExist:
        return _error_response(request, "Seller not found.")         

    u = models.Product(name=request.POST['name'],                         \
                    description=request.POST['description'],                             \
                    price=request.POST['price'],                             \
                    date_posted=datetime.datetime.now(),	\
                    sold=False,									\
                    seller=v)
    
    try:
    	u.save()
    except db.Error:
        return _error_response(request, "db Error")
    return _success_response(request, {'product_id': u.pk})


def retrieve_product(request, product_id):
    if request.method != 'GET':
        return _error_response(request, "Must make GET request.")

    try:
        u = models.Product.objects.get(pk=product_id)
    except models.Product.DoesNotExist:
        return _error_response(request, "Product not found.")

    if u.order is None:
	    return _success_response(request, {'name': u.name,      \
	                                       'description': u.description,          \
	                                       'price': u.price,          \
	                                       'date_posted': u.date_posted, 	\
	                                       'sold': u.sold, 			\
	                                       'seller': u.seller.username,    \
	                                       'order': u.order})    	

    return _success_response(request, {'name': u.name,      \
                                       'description': u.description,          \
                                       'price': u.price,          \
                                       'date_posted': u.date_posted, 	\
                                       'sold': u.sold, 			\
                                       'seller': u.seller.username,    \
                                       'order': {'order_id':u.order.pk, 'buyer':  u.order.buyer.username, 'date_ordered': u.order.date_ordered}})


def update_product(request, product_id):
    if request.method != 'POST':
        return _error_response(request, "Must make POST request.")

    try:
        u = models.Product.objects.get(pk=product_id)
    except models.Product.DoesNotExist:
        return _error_response(request, "Product not found.")

    changed = False
    if 'name' in request.POST:
        u.name = request.POST['name']
        changed = True
    if 'description' in request.POST:
        u.description = request.POST['description']
        changed = True
    if 'price' in request.POST:
        u.price = request.POST['price']
        changed = True
    if 'sold' in request.POST:
        u.sold = request.POST['sold']        
        changed = True    
    if 'order_id' in request.POST:
    	try:
    		v = models.Order.objects.get(pk=request.POST['order_id'])
    	except models.Order.DoesNotExist:
    		return _error_response(request, "Order not found.")
    	u.order = v
    	changed = True                        

    if not changed:
        return _error_response(request, "No fields updated.")

    u.save()
    return _success_response(request)


def delete_product(request, product_id):
    if request.method != 'POST':
        return _error_response(request, "Must make POST request.")

    try:
        u = models.Product.objects.get(pk=product_id)
    except models.Product.DoesNotExist:
        return _error_response(request, "Product not found.")

    u.delete()    

    return _success_response(request)


#ORDER API
#-------------------------------------------------------------------------------------------------------------#
def create_order(request, buyer_id):
    if request.method != 'POST':
        return _error_response(request, "Must make POST request.")
    try:
        v = models.Profile.objects.get(pk=buyer_id)
    except models.Profile.DoesNotExist:
        return _error_response(request, "Buyer not found.") 


    u = models.Order(buyer=v, date_ordered=datetime.datetime.now())

    try:
        u.save()
    except db.Error:
        return _error_response(request, "db Error")
    return _success_response(request, {'order_id': u.pk})


def retrieve_order(request, order_id):
    if request.method != 'GET':
        return _error_response(request, "Must make GET request.")

    try:
        u = models.Order.objects.get(pk=order_id)
    except models.Order.DoesNotExist:
        return _error_response(request, "Order not found.")


    if not hasattr(u, 'product_set'): return _success_response(request, {'buyer': u.buyer.username, 'date_ordered': u.date_ordered})
    l = dict()
    for product in u.product_set.all():
    	l[str(product.pk)] = {'product_name': product.name, 'product_id': product.pk}
    return _success_response(request, {'buyer': u.buyer.username,      \
                                       'date_ordered': u.date_ordered,          \
                                       'product': l})


#Updating and deleting orders do not need to be accomodated for.


#REVIEW API
#-------------------------------------------------------------------------------------------------------------#
def create_review(request, author_id, product_id):
    if request.method != 'POST':
        return _error_response(request, "Must make POST request.")
    if 'description' not in request.POST or 'rating' not in request.POST:
        return _error_response(request, "Missing required fields.")

    try:
        v = models.Profile.objects.get(pk=author_id)
    except models.Profile.DoesNotExist:
        return _error_response(request, "Profile not found.") 

    try:
        y = models.Product.objects.get(pk=product_id)
    except models.Product.DoesNotExist:
        return _error_response(request, "Product not found.")         




    u = models.Review(author=v,                         \
                    description=request.POST['description'],                             \
                    date_written=datetime.datetime.now(),                             \
                    rating=request.POST['rating'],						\
                    product=y)
    
    try:
    	u.save()
    except db.Error:
        return _error_response(request, "db Error")
    return _success_response(request, {'review_id': u.pk})


def retrieve_review(request, review_id):
    if request.method != 'GET':
        return _error_response(request, "Must make GET request.")

    try:
        u = models.Review.objects.get(pk=review_id)
    except models.Review.DoesNotExist:
        return _error_response(request, "Review not found.")

    return _success_response(request, {'author': u.author.username,      \
                                       'description': u.description,          \
                                       'date_written': u.date_written,          \
                                       'rating': u.rating, 	\
                                       'product': u.product.name })


def update_review(request, review_id):
    if request.method != 'POST':
        return _error_response(request, "Must make POST request.")

    try:
        u = models.Review.objects.get(pk=review_id)
    except models.Review.DoesNotExist:
        return _error_response(request, "Review not found.")

    changed = False
    if 'description' in request.POST:
        u.description = request.POST['description']
        changed = True
    if 'rating' in request.POST:
        u.rating = request.POST['rating']        
        changed = True                          

    if not changed:
        return _error_response(request, "No fields updated.")

    u.save()
    return _success_response(request)


def delete_review(request, review_id):
    if request.method != 'POST':
        return _error_response(request, "Must make POST request.")

    try:
        u = models.Review.objects.get(pk=review_id)
    except models.Review.DoesNotExist:
        return _error_response(request, "Review not found.")

    u.delete()    

    return _success_response(request)


#STATISTICS API
#--------------0-----------------------------------------------------------------------------------------------#


def stats(request):
	if request.method != 'GET':
		return _error_response(request, "Must make GET request.")
	else:
		return _success_response(request, {'profileCount': models.Profile.objects.count(),      \
											   'productCount': models.Product.objects.count(),          \
											   'orderCount': models.Order.objects.count(),          \
											   'reviewCount': models.Review.objects.count(), 	})



#AUTHENTICATION API
#-------------------------------------------------------------------------------------------------------------#
def create_authenticator(request):
	if request.method != 'POST':
		return _error_response(request, "Must make POST request.")	
	
	
	try:
		w = models.Profile.objects.get(username = request.POST["username"])
	except models.Profile.DoesNotExist:
		return _error_response(request, "Authentication failed.(1)")
	
	
	if not hashers.check_password(request.POST["password"], w.password):
		return _error_response(request, "Authentication failed.(2)")
	
	try:
		v = models.Authenticator.objects.get(user_id=w.pk)
		delete_authenticator(request, v.authenticator)
	except models.Authenticator.DoesNotExist:
		pass
	k = hmac.new(key = settings.SECRET_KEY.encode('utf-8'), msg = os.urandom(32), digestmod = 'sha256').hexdigest()
	try:
		v = models.Authenticator.objects.get(authenticator=k)
		delete_authenticator(request, v.authenticator)
	except models.Authenticator.DoesNotExist:
		pass	
	u = models.Authenticator(user_id = w.pk, authenticator = k, date_created = datetime.datetime.now())
	try:
		u.save()
	except db.Error:
		return _error_response(request, "Authentication failed. (3)")
	return _success_response(request, {"auth": k, "id": w.pk})

def authenticate(request, authenticator):
	try:
		u = models.Authenticator.objects.get(pk=authenticator)			
	except models.Authenticator.DoesNotExist:
		return _error_response(request, "Authentication error.")		
	return _success_response(request, "Authentication successful.")

def delete_authenticator(request, authenticator):
    try:
        u = models.Authenticator.objects.get(authenticator = authenticator)
    except models.Authenticator.DoesNotExist:
        return _error_response(request, "User not authenticated.")

    u.delete()    

    return _success_response(request, resp = "Successfully deleted.")	
	
#JSON Response Methods

def _error_response(request, error_msg):
    return JsonResponse({'ok': False, 'error': error_msg})

def _success_response(request, resp=None):
    if resp:
    	return JsonResponse({'ok': True, 'resp': resp})
    else:
    	return JsonResponse({'ok': True})
