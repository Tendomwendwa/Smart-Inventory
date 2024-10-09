from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('index/', index, name='index'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('items/', items_view, name='items'),
    path('create_items/', create_items_view, name='create_items'),
    path('items/edit/<int:item_id>/', edit_items_view, name='edit_items'),
    path('items/delete/<int:item_id>/', delete_items_view, name='delete_items'),
    
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
]