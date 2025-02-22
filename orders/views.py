#orders\views.py
import re
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Sum, F
from django.utils.dateparse import parse_date

from .models import Order, Book, OrderItem, OrderItemBook

# Regular expression to match YYYY-MM-DD format
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Create your views here.

def is_valid_date(date_str):
    """ Returns True if date is valid and exists in the calendar. """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")  # Parse date to check validity
        return True
    except ValueError:
        return False  # Invalid date (e.g., April 32, February 30, etc.)
    
    
def revenue_index(request):
    """
    Renders an HTML page with a form to filter orders by start and end date
    and displays the total revenue for completed orders.
    
    """
    total = None
    error_message = None
    #GET query parameters
    start_date_str = request.GET.get('start_date','').strip()
    end_date_str = request.GET.get('end_date','').strip()
    
    # Ensure both dates are entered before proceeding with validation
    if not start_date_str or not end_date_str:
        error_message = "Please enter both start and end dates!"
    
    #Initialize start_date and end_date so they are always available
    start_date = None
    end_date = None
    
    # Validate date format (YYYY-MM-DD)
    if start_date_str and not DATE_PATTERN.fullmatch(start_date_str):
        error_message = "Invalid Start Date format! Please use YYYY-MM-DD."
    elif end_date_str and not DATE_PATTERN.fullmatch(end_date_str):
        error_message = "Invalid End Date format! Please use YYYY-MM-DD."
        
    # Validate date existence (prevent invalid days like 2024-02-30)
    elif start_date_str and not is_valid_date(start_date_str):
        error_message = "Invalid Start Date! The date does not exist."
    elif end_date_str and not is_valid_date(end_date_str):
        error_message = "Invalid End Date! The date does not exist."
    
    if not error_message:
        #Convert string to date (None if blank)
        start_date = parse_date(start_date_str) if start_date_str else None
        end_date = parse_date(end_date_str) if end_date_str else None
        
        #Ensure valid dates were parsed
        if (start_date_str and not start_date) or (end_date_str and not end_date):
            error_message = "Invalid date! Please enter a correct date in YYYY-MM-DD format."
    
    
    
    if not error_message and start_date and end_date:
        #check if the start_date is after the end_date
        if start_date > end_date:
            error_message = "Error! Start Date cannot be after the End Date!"
        #Filter by date range if specified
        else:
            #Filter for COMPLETED orders only
            orders_qs = Order.objects.filter(status=Order.OrderStatusChoices.COMPLETED, order_date__range=[start_date,end_date]
            )
            
            #Sum the total revenue from OrderItemBook
            #OrderItemBook has (quantity,price_at_order) fields
            total = (
                OrderItemBook.objects.filter(order_item__order__in=orders_qs).aggregate(
                    total=Sum(F('quantity') * F('price_at_order'))
                )['total']
            )
            
            if total is None:
                error_message = "No orders found for this specified date range!"
            else:
                total = round(total,2)
        
    #Prepare context data for the template
    context = {
        'total_revenue' : total,
        'start_date': start_date_str or '',
        'end_date': end_date_str or '',
        'error_message': error_message,
    }
        
    return render(request, 'orders/revenue.html',context)
    
    