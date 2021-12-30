# views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.

def list(response):
	prod = Product.objects.all()
	return render(response, "AmazonBotSites/list.html", {"products":prod})

def home(response):
	prodlist = Product.objects.all()
	return render(response, "AmazonBotSites/home.html", {"prodlist":prodlist})