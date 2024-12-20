from django.urls import path
from .views import *


urlpatterns = [
    path('', home_view, name='home'),
    path('index/', index, name='index'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password_reset/', password_reset_view, name='password_reset'),
    path('password_reset_done/', password_reset_done_view, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),
    path('password_reset_complete/', password_reset_complete_view, name='password_reset_complete'),
    
    path('items/', items_view, name='items'),
    path('create_items/', create_items_view, name='create_items'),
    path('items/edit/<int:item_id>/', edit_items, name='edit_items'),
    path('items/delete/<int:item_id>/', delete_items, name='delete_items'),    
    
    path('staff/', staff_view, name='staff'),
    path('create_staff/', create_staff_view, name='create_staff'),
    path('staff/edit/<int:staff_id>/', edit_staff_view, name='edit_staff'),
    path('staff/delete/<int:staff_id>/', delete_staff_view, name='delete_staff'),
    
    path('item_requests/', item_requests_view, name='item_requests'),
    path('create_item_requests/', create_item_requests_view, name='create_item_requests'),
    path('item_requests/edit/<int:item_requests_id>/', edit_item_requests_view, name='edit_item_requests'),
    path('item_requests/delete/<int:item_requests_id>/', delete_item_requests_view, name='delete_item_requests'),
    
    path('restocks/', restocks_view, name='restocks'),
    path('create_restocks/', create_restocks_view, name='create_restocks'),
    path('restocks/edit/<int:restock_id>/', edit_restocks_view, name='edit_restocks'),
    path('restocks/delete/<int:restock_id>/', delete_restocks_view, name='delete_restocks'),
    
    path('approved_requests/', approved_requests_view, name='approved_requests'),
    path('pending_requests/', pending_requests_view, name='pending_requests'),
    path('declined_requests/', declined_requests_view, name='declined_requests'),
    path('total_requests', total_requests_view, name='total_requests'),
    ]