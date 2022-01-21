# urls.py
from django.urls import path

from . import views

urlpatterns = [
path("list", views.list, name="list"),
path("createprodlist", views.createprodlist, name="createprodlist"),
path("grouplis", views.grouplis, name="grouplis"),
path("", views.home, name="home"),
path("<int:id>", views.pdoductdetails, name="pdoductdetails"),
path("api/chart/data/<int:id>", views.prodpricedata),
]