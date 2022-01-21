from django import forms

from .models import ProductList


class ProductListForm(forms.ModelForm):

    name = forms.CharField(label="name")


    class Meta:
        model = ProductList
        fields = ["name", "target_price"]