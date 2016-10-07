from django.shortcuts import render

import urllib.request
import urllib.parse
import json
from django.http import JsonResponse



def retrieve_profile(request, profile_id):
    if request.method != 'GET':
        return _error_response(request, "Must make GET request.")
    try:
    	req = urllib.request.Request('http://models-api:8000/api/v1/profiles/' + str(profile_id) + '/retrieve')
    except e:
    	return _error_response(request, "Profile not found.")		
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return _success_response(request, resp)	

def retrieve_product(request, product_id):
    if request.method != 'GET':
    	return _error_response(request, "Must make GET request.")
    try:
    	req = urllib.request.Request('http://models-api:8000/api/v1/products/' + str(product_id) + '/retrieve')
    except e:
    	return _error_response(request, "Product not found.")
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return _success_response(request, resp)        

def retrieve_order(request, order_id):
	if request.method != 'GET':
		return _error_response(request, "Must make GET request.")
	try:
		req = urllib.request.Request('http://models-api:8000/api/v1/orders/' + str(order_id) + '/retrieve')
	except e:
		return _error_response(request, "Order not found.")
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	return _success_response(request, resp) 

def retrieve_review(request, review_id):
	if request.method != 'GET':
		return _error_response(request, "Must make GET request.")
	try:
		req = urllib.request.Request('http://models-api:8000/api/v1/reviews/' + str(review_id) + '/retrieve')
	except e:
		return _error_response(request, "Review not found.")
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	return _success_response(request, resp) 



def _error_response(request, error_msg):
    return JsonResponse({'ok': False, 'error': error_msg})

def _success_response(request, resp=None):
    if resp:
    	return JsonResponse({'ok': True, 'resp': resp})
    else:
    	return JsonResponse({'ok': True})

