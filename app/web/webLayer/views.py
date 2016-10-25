from django.shortcuts import render
import urllib
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from webLayer.forms import UserSignUpForm, UserLoginForm, ProductCreationForm


def index(request):
	template = loader.get_template('webLayer/index.html')
	context = {}
	if request.method != 'GET':
		return HttpResponse(template.render(context, request))
	try:
		req = urllib.request.Request('http://exp-api:8000/api/v1/home')
	except e:
		return HttpResponse(template.render(context, request))
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	context = resp["resp"]
	return HttpResponse(template.render(context, request))	
	
def signup(request):
	form = UserSignUpForm(request.POST or None)	
	if request.method == "GET":
		return render(request, "webLayer/signup.html", {"form":form})
	
	if not form.is_valid():
		return render(request, "webLayer/signup.html", {"form":form})
	
	username = form.cleaned_data["username"]
	password = form.cleaned_data["password"]
	fname = form.cleaned_data["fname"]
	lname = form.cleaned_data["lname"]
	email = form.cleaned_data["email"]
	location = form.cleaned_data["location"]
		
	data = {"username": username, "password": password, "first_name":fname, "last_name":lname, "email":email, "location":location,}
	
	postData = urllib.parse.urlencode(data).encode("utf-8")
	try:
		req = urllib.request.Request('http://exp-api:8000/api/v1/signup', data = postData, method = "POST", headers={'Content-Type': 'application/json'})
	except e:
		return render(request, "webLayer/signup.html", {"form":form})
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	
	if not resp or not resp["ok"]:
		return render(request, "webLayer/signup.html", {"form":form})
					
	return redirect('login')

def login(request):
	form = UserLoginForm(request.POST or None)
	if request.method == "GET":
		return render(request, "webLayer/login.html", {"form":form})
	if not form.is_valid():
		return render(request, "webLayer/login.html", {"form": form})
	username = form.cleaned_data["username"]
	password = form.cleaned_data["password"]
	data = {"username": username, "password": password}
	postData = urllib.parse.urlencode(data).encode("utf-8")
	try:
		req = urllib.request.Request('http://exp-api:8000/api/v1/signup', data = postData, method = "POST", headers={'Content-Type': 'application/json'})
	except e:
		return render(request, "webLayer/login.html", {"form":form})
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)

	if not resp or not resp["ok"]:
		return render(request, "webLayer/login.html", {"form":form})

	return redirect('/')

def create_listing(request):
	form = ProductCreationForm(request.POST or None)
	if request.method == "GET":
		return render(request, "webLayer/create-listing.html", {"form": form})
	if not form.is_valid():
		return render(request, "webLayer/create-listing.html", {"form": form})
	name = form.cleaned_data["name"]
	description = form.cleaned_data["description"]
	price = form.cleaned_data["price"]
	data = {"name": name, "description": description, "price": price}
	postData = urllib.parse.urlencode(data).encode("utf-8")
	try:
		req = urllib.request.Request('http://exp-api:8000/api/v1/signup', data = postData, method = "POST", headers = {'Content-Type': 'application/json'})
	except e:
		return render(request, "webLayer/create-listing.html", {"form": form})
	resp_json = urllib.request.urlopen(req).read().decode("utf-8")
	resp - json.loads(resp_json)
	if not resp or not resp["ok"]:
		return render(request, "webLayer/create-listing.html", {"form": form})

	return redirect('/')

def product(request, product_id):
    template = loader.get_template('webLayer/product.html')
    prod = None
    while True:
        response = retrieve_product(request, product_id)
        json_obj = json.loads((response.content).decode("utf-8"))
        if not json_obj["resp"]["resp"]["ok"]:
            return HttpResponse(template.render({"product":"Product not found."}, request))
        prod = json_obj["resp"]["resp"]["resp"]
        break
    return HttpResponse(template.render({"product":prod}, request))

def retrieve_profile(request, profile_id):
    if request.method != 'GET':
        return _error_response(request, "Must make GET request.")
    try:
    	req = urllib.request.Request('http://exp-api:8000/api/v1/profiles/' + str(profile_id) + '/retrieve')
    except e:
    	return _error_response(request, "Profile not found.")		
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return _success_response(request, resp)	

def retrieve_product(request, product_id):
    if request.method != 'GET':
    	return _error_response(request, "Must make GET request.")
    try:
    	req = urllib.request.Request('http://exp-api:8000/api/v1/products/' + str(product_id) + '/retrieve')
    except e:
    	return _error_response(request, "Product not found.")
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return _success_response(request, resp)        















def retrieve_order(request, order_id):
	if request.method != 'GET':
		return _error_response(request, "Must make GET request.")
	try:
		req = urllib.request.Request('http://exp-api:8000/api/v1/orders/' + str(order_id) + '/retrieve')
	except e:
		return _error_response(request, "Order not found.")
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	return _success_response(request, resp) 

def retrieve_review(request, review_id):
	if request.method != 'GET':
		return _error_response(request, "Must make GET request.")
	try:
		req = urllib.request.Request('http://exp-api:8000/api/v1/reviews/' + str(review_id) + '/retrieve')
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


