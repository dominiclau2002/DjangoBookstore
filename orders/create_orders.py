#orders/create_orders.py
#import python packages
import os
import random
import django
from datetime import datetime, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookstore.settings")
django.setup() #Ensure Django is setup before importing models

#import Django packages and models
from django.utils import timezone
from django.db.models import Sum,F
from orders.models import Order, OrderItem, OrderItemBook, Book

def create_orders(num_orders=100):
    """
    Creates a set of COMPLETED orders with order dates randomized between January 1, 2024
    and January 1, 2025. Each order will have one OrderItem containing one or more books
    drawn deterministically from a fixed list of book titles. The price for each OrderItemBook
    is a random value between $10 and $30.
    
    Returns:
        expected_total_revenue (float): Sum of revenue from all created OrderItemBook records.
    """
    #initialize variables for total revenue, start_date, end_date, total_days
    
    total_revenue = 0
    start_date = datetime(2024,1,1)
    end_date = datetime(2025,1,1)
    total_days = (end_date - start_date).days
    
    book_titles = [
            "Shadows of the Forgotten",
            "The Clockmaker’s Secret",
            "Echoes of a Distant Star",
            "Beneath the Crimson Sky",
            "The Last Library",
            "Whispers in the Fog",
            "The Alchemist’s Apprentice",
            "Lost in the Labyrinth",
            "The Moonstone Prophecy",
            "A Tale of Two Dimensions",
            "Secrets of the Hidden Valley",
            "The Enchanted Quill",
            "Winds of the Eternal Sea",
            "The Time Traveler’s Dilemma",
            "Legends of the Starborn",
            "The Silent Watcher",
            "Curse of the Silver Phoenix",
            "The Forgotten Manuscript",
            "Echoes from the Abyss",
            "The Guardian’s Oath"
        ]
        
    #initialize variables for the number of titles and the book_counter
    num_titles = len(book_titles)
    book_counter = 0
    
    for i in range(num_orders):
        #create the random offset to randomize the order date within the year given
        random_offset = random.randint(0, total_days - 1)
        naive_date = start_date + timedelta(days=random_offset)
        order_date = timezone.make_aware(naive_date)
        
        #create an Order object with the date set to the randomized date, and status completed
        order = Order.objects.create(
            order_date = order_date,
            status = Order.OrderStatusChoices.COMPLETED
        )
        
        #determine the number of books in the order (cycle through 1,2,3)
        num_books_in_order = (i%3) + 1
        #create OrderItem object with Foreign Key as the created Order object
        order_item = OrderItem.objects.create(order=order)
        
        for j in range(num_books_in_order):
            #select book title in round robin fashion, each iteration will increase the counter by 1 until 20
            title = book_titles[book_counter % num_titles]
            book_counter += 1
            
            #create or get book instance:
            book, _ = Book.objects.get_or_create(
                name = title,
                defaults={'author' : 'Test Author', 'price':round(random.uniform(10,30),2)}
            )
            
            #generate random price and quantity
            price = round(random.uniform(10,30),2)
            quantity = ((i+j) % 5 ) + 1
            
            #create OrderItemBook object corresponding to the previously created OrderItem, Book, book quantity and price
            OrderItemBook.objects.create(
                order_item = order_item,
                book = book,
                quantity = quantity,
                price_at_order = price
            )
            
            total_revenue += quantity * price

        #Print order details
        print(f"Order {order.id} - Date: {order.order_date}, Status:{order.status}")
        for item in order.items.all():
            for oib in item.order_items.all():
                print(f"Book: {oib.book.name}, Quantity: {oib.quantity}, Price: {oib.price_at_order}")
                
    #check the actual revenue from the database
    actual_revenue = OrderItemBook.objects.aggregate(
        total=Sum(F('quantity') * F('price_at_order'))
    )['total'] or 0.00 #returns 0 if the database is empty
    
    
    #Print total revenue and actual revenue
    print(f"\nTotal Expected Revenue: ${round(total_revenue,2)}")
    print(f"Total Actual Revenue (from DB): ${round(actual_revenue,2)}")
    
    # Compare the values
    if round(total_revenue, 2) == round(float(actual_revenue), 2):
        print("Revenue match confirmed!")
    else:
        print("Revenue mismatch! Investigate the discrepancy.")

if __name__ == '__main__':
    create_orders(num_orders=100)


# ================================================================================

