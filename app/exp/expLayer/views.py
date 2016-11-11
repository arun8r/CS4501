from django.shortcuts import render
from elasticsearch import Elasticsearch
from kafka import KafkaProducer, KafkaConsumer
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse
from django.core.urlresolvers import reverse
producer = KafkaProducer(bootstrap_servers=['kafka:9092'])

def home(request):
	response = retrieve_recent(request, 10)
	json_obj = json.loads((response.content).decode("utf-8"))
	if not json_obj["ok"]:
		return _error_response(request, "Request failed.")
	homePageItems = {}
	homePageItems["products"] = json_obj["resp"]["products"]
	return _success_response(request, homePageItems)
	
	
def create_listing(request, name, description, price, user_id):
	data = {"name":name, "description":description,"price": price, "user_id":user_id}
	postData = urllib.parse.urlencode(data).encode("utf-8")
	producer.send('new-listings-topic', json.dumps(data).encode('utf-8'))
	try:
		req = urllib.request.Request('http://models-api:8000/api/v1/products/' + str(user_id) + '/create', postData)
	except e:
		return _error_response(request, "Sign up failed.")	
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	return _success_response(request, resp)			

def signup(request, username, password, first_name, last_name, email, location):
	data = {"username": username, "password": password, "first_name":first_name, "last_name":last_name, "email":email, "location":location}
	
	postData = urllib.parse.urlencode(data).encode("utf-8")
		
	try:
		req = urllib.request.Request('http://models-api:8000/api/v1/profiles/create', postData)
	except e:
		return _error_response(request, "Sign up failed.")	
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	return _success_response(request, resp)	
	
def login(request, username, password):
	data = {"username": username, "password": password}
	
	postData = urllib.parse.urlencode(data).encode("utf-8")
		
	try:
		req = urllib.request.Request('http://models-api:8000/api/v1/authentication/create', postData)
	except e:
		return _error_response(request, "Login failed.")	
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	if not resp["ok"]:
		return _error_response(request, "Login failed.")
	return _success_response(request, resp["resp"])		


def logout(request, authenticator):
	try:
		req = urllib.request.Request('http://models-api:8000/api/v1/authentication/deauthenticate/' + str(authenticator))
	except e:
		return _error_response(request, "Authenticate failed.")	
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	if not resp["ok"]:
		return _error_response(request, "User not logged out.")
	return _success_response(request, resp["resp"])	



def authenticate(request, authenticator):
	try:
		req = urllib.request.Request('http://models-api:8000/api/v1/authentication/authenticate/' + str(authenticator))
	except e:
		return _error_response(request, "Authenticate failed.")	
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	if not resp["ok"]:
		return _error_response(request, "Authenticate failed.")
	return _success_response(request, resp["resp"])	
		


def retrieve_recent(request, num):
	response = retrieve_stats(request)
	json_obj = json.loads((response.content).decode("utf-8"))
	if not json_obj["ok"] or not json_obj["resp"]["ok"]:
		return _error_response(request, "Request failed.")
	j = int(json_obj["resp"]["resp"]["productCount"])
	i = 0
	prods = []
	while i < int(num):
		response = retrieve_product(request, j - i)
		json_obj = json.loads((response.content).decode("utf-8"))
		if not json_obj["resp"]["ok"]:
			break
		json_obj["resp"]["resp"]["product_id"] = j - i
		prods.append(json_obj["resp"]["resp"])
		i = i + 1	
	return _success_response(request, {"products": prods})

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



def retrieve_stats(request):
	if request.method != 'GET':
		return _error_response(request, "Must make GET request.")
	try:
		req = urllib.request.Request('http://models-api:8000/api/v1/stats')
	except e:
		return _error_response(request, "Request failed.")
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	return _success_response(request, resp)

def search(request):
    if request.method != "POST" or not request.POST.get('query'):
        return HttpResponseBadRequest()
        
    string = request.POST.get('query')
    
    result = elasticsearch.search(index = 'listing-indexer',
    body={
        'query':{
        'query_string':{
            'query':string
        }
    }})
    
    
    searchresults = []
    for product in result['hits']['hits']:
        if '_source' in product:
            searchresults.append(product['_source'])
    return HttpResponse(json.dumps(searchresults))

def _error_response(request, error_msg):
    return JsonResponse({'ok': False, 'error': error_msg})

def _success_response(request, resp=None):
    if resp:
    	return JsonResponse({'ok': True, 'resp': resp})
    else:
    	return JsonResponse({'ok': True})


