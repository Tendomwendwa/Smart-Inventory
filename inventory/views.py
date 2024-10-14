from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import *
from .models import *

# Create your views here.
def home_view(request):
    total_requests = ItemRequest.objects.count()
    approved_requests = ItemRequest.objects.filter(request_status='Approved').count()
    pending_requests = ItemRequest.objects.filter(request_status='Pending').count()
    declined_requests = ItemRequest.objects.filter(request_status='Declined').count()

    if total_requests > 0:
        approved_percentage = int((approved_requests / total_requests) * 100)
    else:
        approved_percentage = 0

    context = {
        'total_requests': total_requests,
        'approved_percentage': approved_percentage,
        'pending_requests': pending_requests,
        'declined_requests': declined_requests,
    }
    return render(request, 'inventory/index.html', context)


def index(request):
    return render(request, 'inventory/home.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid Credentials')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  
            else:
                messages.error(request, 'Invalid username or password')
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



def approved_requests_view(request):
    approved_requests = ItemRequest.objects.filter(request_status='Approved')
    context = { 'approved_requests': approved_requests, }
    return render (request, 'requests/approved_requests.html', context)

def pending_requests_view(request):
    pending_requests = ItemRequest.objects.filter(request_status='Pending')
    context = { 'pending_requests': pending_requests, }
    return render(request, 'requests/pending_requests.html', context)

def declined_requests_view(request):
    declined_requests = ItemRequest.objects.filter(request_status='Declined')
    context = { 'declined_requests': declined_requests, }
    return render(request, 'requests/declined_requests.html', context)

def total_requests_view(request):
    total_requests = ItemRequest.objects.all()
    context = { 'total_requests': total_requests, }
    return render(request, 'requests/total_requests.html', context)