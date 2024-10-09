from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import *
from .models import *

# Create your views here.
def home_view(request):
    return render(request, 'inventory/index.html')

def index(request):
    return render(request, 'inventory/home.html')

# SignUp View
def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to homepage after login
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')



def items_view(request):
    item_list = Item.objects.all()
    return render(request, 'inventory/items.html', {'items': item_list})

def create_items_view(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('items')
    else:
        form = ItemForm()
    return render(request, 'inventory/create_items.html', {'form': form})

def edit_items_view(request, item_id):
    item = Item.objects.get(pk=item_id)
    form = ItemForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('items')
    return render(request, 'inventory/edit_items.html',
        {'item':item,
        'form':form})
    
def delete_items_view(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect('items')
    



def staff_view(request):
    staff_list = Staff.objects.all()
    return render(request, 'inventory/staff.html', {'staff': staff_list})

def create_staff_view(request):
    if request.method == "POST":
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff')
    else:
        form = StaffForm()
    return render(request, 'inventory/create_staff.html', {'form': form})

def edit_staff_view(request, staff_id):
    staff = Staff.objects.get(pk=staff_id)
    form = StaffForm(request.POST or None, instance=staff)
    if form.is_valid():
        form.save()
        return redirect('staff')
    return render(request, 'inventory/edit_staff.html', {'item':staff, 'form':form})

def delete_staff_view(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    staff.delete()
    return redirect('staff')



def item_requests_view(request):
    item_requests_list = ItemRequest.objects.all()
    return render(request, 'inventory/item_requests.html', {'item_requests': item_requests_list})

def create_item_requests_view(request):
    if request.method == "POST":
        form = ItemRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_requests')
    else:
        form = ItemRequestForm()
    return render(request, 'inventory/create_item_requests.html', {'form': form})

def edit_item_requests_view(request, item_requests_id):
    item_requests =ItemRequest.objects.get(pk=item_requests_id)
    form = ItemRequestForm(request.POST or None, instance=item_requests)
    if form.is_valid():
        form.save()
        return redirect('item_requests')
    return render(request, 'inventory/edit_item_requests.html', {'item_requests':item_requests, 'form': form})

def delete_item_requests_view(request, item_requests_id ):
    item_requests = get_object_or_404(ItemRequest, id=item_requests_id)
    item_requests.delete()
    return redirect('item_requests')



def restocks_view(request):
    restocks_list =Restock.objects.all()
    return render(request, 'inventory/restocks.html', {'restocks': restocks_list})

def create_restocks_view(request):
    if request.method == "POST":
        form = RestockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('restocks')
    else:
        form = RestockForm()
    return render(request, 'inventory/create_restocks.html', {'form': form})

def edit_restocks_view(request, restock_id):
    restock = Restock.objects.get(pk=restock_id)
    form = RestockForm(request.POST or None, instance=restock)
    if form.is_valid():
        form.save()
        return redirect('restocks')
    return render(request, 'inventory/edit_restocks.html', {'restock':restock, 'form': form})

def delete_restocks_view(request, restock_id):
    restocks = get_object_or_404(Restock, id=restock_id)
    restocks.delete()
    return redirect('restocks')