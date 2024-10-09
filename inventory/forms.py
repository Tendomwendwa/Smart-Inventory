from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import *


# Signup Form
class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

# Login Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)
    
    


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'item_status', 'quantity']

        
class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'department']     


class RestockForm(forms.ModelForm):
    class Meta:
        model = Restock
        fields = ['item', 'quantity']
        

class ItemRequestForm(forms.ModelForm):
    class Meta:
        model = ItemRequest
        fields = ['staff', 'item', 'request_status']