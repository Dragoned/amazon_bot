# views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.

def index(response, id):
	prod = Product.objects.get(id=id)
	return render(response, "AmazonBotSites/list.html", {"prod":prod})

def home(response):
	return render(response, "AmazonBotSites/home.html", {})