from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.conf import settings
from .decorators import login_required
from django.contrib.auth import get_user_model
from .forms import *
from .models import *

from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

UserModel = get_user_model()

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


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_staff:  
                login(request, user)
                return redirect('home')  
            else:
                messages.error(request, "Invalid credentials or not authorized.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True  # Make the user staff so they can access Django admin
            user.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')  # Redirect to login page
        else:
            messages.error(request, "Error during registration. Please try again.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})



def logout_view(request):
    request.session.flush()  
    return redirect('login')  


#@login_required
def items_view(request):
    item_list = Item.objects.all()
    return render(request, 'inventory/items.html', {'items': item_list})

def create_items_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        item_status = request.POST.get('item_status')
        quantity = request.POST.get('quantity')

        if not name or not item_status or quantity is None:
            return render(request, 'inventory/create_items.html', {
                'error': 'All fields are required.'
            })

        Item.objects.create(name=name, item_status=item_status, quantity=quantity)

        return redirect('items') 

    return render(request, 'inventory/create_items.html')



def edit_items(request, item_id):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Item, id=item_id)
        item.name = request.POST.get('name')
        item.quantity = request.POST.get('quantity')
        item.item_status = request.POST.get('status')
        
        item.save()
        return redirect('items')
    return render(request, 'inventory/items.html')  
    
def delete_items(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == "POST":
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('items')
    

#@login_required
def staff_view(request):
    staff_list = Staff.objects.all()
    return render(request, 'inventory/staff.html', {'staff': staff_list})

def create_staff_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        department = request.POST.get('department')
        
        if not first_name or not last_name or not email or not phone_number or not department:
            return render(request, 'inventory/create_staff.html', {
                'error': 'All fields are required.'
            })
        
        Staff.objects.create(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, department=department)
        
        return redirect('staff')
    
    return render(request, 'inventory/create_staff.html')

def edit_staff_view(request, staff_id):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')

        staff = get_object_or_404(Staff, id=staff_id)

        staff.first_name = request.POST.get('first_name')
        staff.last_name = request.POST.get('last_name')
        staff.email = request.POST.get('email')
        staff.phone_number = request.POST.get('phone_number')
        staff.department = request.POST.get('department')

        staff.save()

        return redirect('staff') 
    else:
        return render(request, 'inventory/staff.html')


def delete_staff_view(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == "POST":
        staff.delete()
        return redirect('staff')


#@login_required
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
    item_request = get_object_or_404(ItemRequest, id=item_requests_id)
    if request.method == "POST":
        form = ItemRequestForm(request.POST, instance=item_request)
        if form.is_valid():
            form.save()
            return redirect('item_requests')
    else:
        form = ItemRequestForm(instance=item_request)
    return render(request, 'inventory/item_requests.html', {'form': form})


def delete_item_requests_view(request, item_requests_id):
    item_request = get_object_or_404(ItemRequest, id=item_requests_id)
    if request.method == "POST":
        item_request.delete()
        return redirect('item_requests')
    return render(request, 'inventory/item_requests.html')



#@login_required
def restocks_view(request):
    restocks_list =Restock.objects.all()
    return render(request, 'inventory/restocks.html', {'restocks': restocks_list})

def create_restocks_view(request):
    if request.method == "POST":
        item = request.POST.get('item')
        quantity = request.POST.get('quantity')

        if not item or not quantity:
            return render(request, 'inventory/create_restocks.html', {
                'error': 'All fields are required.'
            })

        Restock.objects.create(item=item, quantity=quantity)
        return redirect('restocks')

    return render(request, 'inventory/create_restocks.html')

def edit_restocks_view(request, restock_id):
    restock = Restock.objects.get(pk=restock_id)
    if request.method == "POST":
        restock.item = request.POST.get('item')
        restock.quantity = request.POST.get('quantity')
        restock.save()
        return redirect('restocks')
    return render(request, 'inventory/edit_restocks.html', {'restock': restock})

def delete_restocks_view(request, restock_id):
    restock = get_object_or_404(Restock, id=restock_id)
    if request.method == "POST":
        restock.delete()
        messages.success(request, 'Record deleted successfully!')
        return redirect('restocks')

def delete_items(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == "POST":
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('items')
    



#@login_required
def approved_requests_view(request):
    approved_requests = ItemRequest.objects.filter(request_status='Approved')
    context = { 'approved_requests': approved_requests, }
    return render (request, 'requests/approved_requests.html', context)

#@login_required
def pending_requests_view(request):
    pending_requests = ItemRequest.objects.filter(request_status='Pending')
    context = { 'pending_requests': pending_requests, }
    return render(request, 'requests/pending_requests.html', context)

#@login_required
def declined_requests_view(request):
    declined_requests = ItemRequest.objects.filter(request_status='Declined')
    context = { 'declined_requests': declined_requests, }
    return render(request, 'requests/declined_requests.html', context)

#@login_required
def total_requests_view(request):
    total_requests = ItemRequest.objects.all()
    context = { 'total_requests': total_requests, }
    return render(request, 'requests/total_requests.html', context)




def password_reset_view(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = UserModel.objects.filter(email=email)
            if users.exists():
                for user in users: 
                    subject = 'Password Reset Requested'
                    email_template_name = 'accounts/password_reset.html'
                    context = {
                        'email': user.email,
                        'domain': request.get_host(),
                        'site_name': 'Smart Inventory',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, context)
                    send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email])
                
                return redirect('password_reset_done')
            else:
                form.add_error('email', 'No user is associated with this email address.')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'accounts/password_reset.html', {'form': form})


def password_reset_confirm_view(request, uidb64=None, token=None):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')
        else:
            form = SetPasswordForm(user)
    else:
        form = None
    return render(request, 'accounts/password_reset_confirm.html', {'form': form})


def password_reset_done_view(request):
    return render(request, 'accounts/password_reset_done.html')

def password_reset_complete_view(request):
    return render(request, 'accounts/password_reset_complete.html')


