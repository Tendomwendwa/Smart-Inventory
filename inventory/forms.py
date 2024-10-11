from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        for field_name in self.fields:
            self.fields[field_name].help_text = None
        
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"


class LoginForm(forms.Form):
    username = forms.CharField()
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