#orders\views.py

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Sum, F
from django.utils.dateparse import parse_date

from .models import Order, Book, OrderItem, OrderItemBook

# Create your views here.
def revenue_index(request):
    """
    Renders an HTML page with a form to filter orders by start and end date
    and displays the total revenue for completed orders.
    
    """
    total = None
    #GET query parameters
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    #Initialize start_date and end_date so they are always available
    start_date = None
    end_date = None
    
    if start_date_str or end_date_str:
        #Convert string to date (None if blank)
        start_date = parse_date(start_date_str) if start_date_str else None
        end_date = parse_date(end_date_str) if end_date_str else None
    
    #Filter for COMPLETED orders only
    orders_qs = Order.objects.filter(status=Order.OrderStatusChoices.COMPLETED)
    
    #Filter by date range if specified
    if start_date:
        orders_qs = orders_qs.filter(order_date__gte=start_date)
    if end_date:
        orders_qs = orders_qs.filter(order_date__lte=end_date)
        
    #Sum the total revenue from OrderItemBook
    #OrderItemBook has (quantity,price_at_order) fields
    total = (
        OrderItemBook.objects.filter(order_item__order__in=orders_qs).aggregate(
            total=Sum(F('quantity') * F('price_at_order'))
        )['total']
    )
    
    if total is None:
        total = 0
        
    #Prepare context data for the template
    context = {
        'total_revenue' : total,
        'start_date': start_date_str or '',
        'end_date': end_date_str or '',
    }
        
    return render(request, 'orders/revenue.html',context)
    
    