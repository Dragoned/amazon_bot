# views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.

def index(response, id):
	prod = Product.objects.get(id=id)
	return render(response, "AmazonBotSites/list.html", {"prod":prod})

def home(response):
	prodlist = Product.objects.all()
	return render(response, "AmazonBotSites/home.html", {"prodlist":prodlist})