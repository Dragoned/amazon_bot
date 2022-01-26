# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse


from .models import *
from .forms import *

# Create your views here.

def home(request): 
	if response.method == "POST":
		#print(request.POST.get("2"))
		pass

	prodlist = Product.objects.all()
	return render(request, "AmazonBotSites/home.html", {"prodlist":prodlist})

def createprodlist(request):
	if request.method == "POST":

		form = ProductListForm(request.POST)

		if form.is_valid():
			ProductList = form.save(commit=False)

			ProductList.ID_User = request.user

			ProductList.save()
   
			return redirect("grouplis")

	form = ProductListForm()
	return render(request, "AmazonBotSites/createprodlist.html", {"form":form})

def grouplis(request):
	grouplist = ProductList.objects.filter(ID_User=request.user)
	return render(request, "AmazonBotSites/prodlistview.html", {"grouplist":grouplist})

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