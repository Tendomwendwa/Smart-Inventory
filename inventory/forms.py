from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import SetPasswordForm as DjangoSetPasswordForm


from .models import *
  
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data.get('full_name')
        if commit:
            user.save()
        return user
    
        
        
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Add an email field for the user

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Fields for registration

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
 
class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(max_length=254)

class SetPasswordForm(DjangoSetPasswordForm):
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput)
    

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
    
    
class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'quantity']
        
class EditStaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'department']
        
