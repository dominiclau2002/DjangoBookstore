from django.contrib import admin
from .models import Book, Order, OrderItem, OrderItemBook
# Register your models here.

admin.site.register(Book)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderItemBook)