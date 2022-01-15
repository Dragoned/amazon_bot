# views.py
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


from .models import *

# Create your views here.

def home(request):
	prodlist = Product.objects.all()
	return render(request, "AmazonBotSites/home.html", {"prodlist":prodlist})

def list(request):

	if request.method == 'POST':
		serch = request.POST['searchinput']
		prod = Product.objects.filter(name__icontains=serch)
	else:
		prod = Product.objects.all()
  
	return render(request, "AmazonBotSites/list.html", {"prodlist":prod})

def pdoductdetails(request, id):
    product = Product.objects.get(id=id)
    print(product)
    return render(request, "AmazonBotSites/proddetails.html", {"product":product})

def prodpricedata(request, id, *keyword, **kwargs):
    
	prices = Price.objects.filter(ID_Product__exact=id)

	print(prices)

	data = {
		"prices": [i.price for i in prices],
  		"date": [i.datetime for i in prices]
	}
	return JsonResponse(data)