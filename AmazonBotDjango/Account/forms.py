from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate

from .models import Account

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Account
        fields = ['email', 'username', 'password1', 'password2']

class UserAuthenticationForm(forms.ModelForm):
    
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    
    class Meta:
        model = Account
        fields = ["email", "password"]
    
    def clean(self):
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("invalid email or password")