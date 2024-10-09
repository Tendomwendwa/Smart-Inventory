from django.contrib import admin
from .models import Item, Staff, ItemRequest, Restock

# Register your models here.
admin.site.register(Item)
admin.site.register(Staff)
admin.site.register(ItemRequest)
admin.site.register(Restock)