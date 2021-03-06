# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse


from .models import *
from .forms import *

# Create your views here.

def home(request): 
	if request.method == "POST":
		itemid = request.POST.get("item")
		target_price = request.POST.get("pricetarget")
		item = Product.objects.get(id=itemid)

		if not Traking.objects.filter(ID_Product__exact = item, ID_User__exact = request.user):
			Traking.objects.create(ID_Product = item, ID_User = request.user, target_price=target_price)
		else:
			return redirect("tracked")

	prodlist = Product.objects.all()[:3]
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

	if request.method == "POST" and 'search' in request.POST:
		serch = request.POST['searchinput']
		product = Product.objects.filter(name__icontains=serch)
  
	elif request.method == "POST" and 'item' in request.POST:
		itemid = request.POST.get("item")
		target_price = request.POST.get("pricetarget")
		item = Product.objects.get(id=itemid)

		if not Traking.objects.filter(ID_Product__exact = item, ID_User__exact = request.user):
			Traking.objects.create(ID_Product = item, ID_User = request.user, target_price=target_price)
		else:
			return redirect("tracked")

		product = Product.objects.all()
  
	else:
		product = Product.objects.all()
  
	return render(request, "AmazonBotSites/list.html", {"prodlist":product})

def pdoductdetails(request, id):
    product = Product.objects.get(id=id)
    print(product)
    return render(request, "AmazonBotSites/proddetails.html", {"product":product})

def trackproduct(request):
    traked = Traking.objects.filter(ID_User__exact = request.user)
    print(traked)
    return render(request, "AmazonBotSites/traked.html", {"traked":traked})

    

def prodpricedata(request, id, *keyword, **kwargs):
    
	prices = Price.objects.filter(ID_Product__exact=id)

	print(prices)

	data = {
		"prices": [i.price for i in prices],
  		"date": [i.datetime.strftime("%Y-%m-%d") for i in prices]
	}

	return JsonResponse(data)