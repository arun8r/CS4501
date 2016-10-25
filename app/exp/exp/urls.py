"""exp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin
from expLayer import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/profiles/(\d+)/retrieve$', views.retrieve_profile), 
    url(r'^api/v1/products/(\d+)/retrieve$', views.retrieve_product), 
    url(r'^api/v1/products/retrieve/recent$', views.retrieve_recent), 
    url(r'^api/v1/orders/(\d+)/retrieve$', views.retrieve_order), 
    url(r'^api/v1/reviews/(\d+)/retrieve$', views.retrieve_review),
    
	url(r'^api/v1/home$', views.home)    
    
]
