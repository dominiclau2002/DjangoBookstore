# orders\tests.py

#import python packages
import random
from datetime import timedelta, datetime


#import django packages and models
from django.test import TestCase, Client
from django.urls import reverse
from .models import Order, OrderItem, OrderItemBook, Book
from django.utils import timezone

class OrderTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        #Seed for reproducibility of the test results (only affects date and price)
        random.seed(42)
        
    def test_order_creation(self):
        #Basic order creation test.
        book = Book.objects.create(name="Test Book", author = "Test Author", price = 15.00)
        order = Order.objects.create(status=Order.OrderStatusChoices.PENDING)
        order_item = OrderItem.objects.create(order=order)
        order_item_book = OrderItemBook.objects.create(order_item=order_item, book=book, quantity=2)
        
        #check that the created parameters match the intended parameters 
        self.assertEqual(order.status, 'PENDING')
        self.assertEqual(order_item_book.quantity, 2)
        self.assertEqual(order_item_book.book.name, "Test Book")
        self.assertEqual(order_item_book.price_at_order, 15.00)
        
    def create_orders_spanning_year(self, num_orders=100):
        """
        Creates a set of COMPLETED orders with order dates randomized between January 1, 2024
        and January 1, 2025. Each order will have one OrderItem containing one or more books
        drawn deterministically from a fixed list of book titles. The price for each OrderItemBook
        is a random value between $10 and $30.
        
        Returns:
            expected_total_revenue (float): Sum of revenue from all created OrderItemBook records.
        """
        #initialize variables for total revenue, start_date, end_date, total_days
        expected_total_revenue = 0
        start_date = datetime(2024,1,1)
        end_date = datetime(2025,1,1)
        total_days = (end_date - start_date).days
        
        #list of book_titles to be randomized
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
        
        num_titles = len(book_titles)
        book_counter = 0 #initialize the book_counter variable
        
        for i in range(num_orders):
            #Randomize the order date within the one-year range given
            random_offset = random.randint(0, total_days -1)
            naive_date = start_date + timedelta(days=random_offset)
            order_date = timezone.make_aware(naive_date)
            
            #create an Order object with the order date that was randomly generated and assign the order status
            order = Order.objects.create(
                order_date = order_date,
                status=Order.OrderStatusChoices.COMPLETED
            )
            
            #Determine how many books to include in this order (cycles through 1,2,3)
            num_books_in_order = (i%3) + 1
            #create an OrderItem object with foreign key Order that was previously created
            order_item = OrderItem.objects.create(order=order) 
            
            for j in range(num_books_in_order):
                #select a book title from the provided list in a round-robin fashion. Index will go back to 0 at the end of the cycle.
                title = book_titles[book_counter % num_titles]
                book_counter += 1
                
                #Create or get the book instance
                #get_or_create returns the book object and a boolean value, 'book, _' indicates to ignore the boolean value
                book, _ = Book.objects.get_or_create(
                    name = title, #set name to the title generated previously
                    defaults={'author': 'Test Author', 'price': round(random.uniform(10,30), 2)}
                )
                
                #generate a random price between $10 and $30 for this OrderItemBook
                random_price = round(random.uniform(10,30),2)
                
                #use a deterministic quantity (cycles through values 1 to 5)
                quantity = ((i+j) % 5) + 1
                OrderItemBook.objects.create(
                    order_item=order_item,
                    book=book,
                    quantity=quantity,
                    price_at_order=random_price
                )
                expected_total_revenue += quantity * random_price
            
            # Print order details and its contents.
            print(f"\nOrder {order.id} - Date: {order.order_date}, Status: {order.status}")
            for item in order.items.all():
                for oib in item.order_items.all():
                    print(f"   Book: {oib.book.name}, Quantity: {oib.quantity}, Price: {oib.price_at_order}")

        return expected_total_revenue
    
    def test_revenue_computation_over_date_range(self):
        """
        Test that the revenue view correctly computes the total revenue for COMPLETED orders
        within a specified date range. Orders are created with random dates between 2024-01-01
        and 2025-01-01, and each order contains one or more books from a fixed list with prices
        varying between $10 and $30.
        """
        expected_revenue = self.create_orders_spanning_year(num_orders=100)
        
        # Call the revenue view with the full date range.
        response = self.client.get(
            reverse('revenue-index'),
            {'start_date': '2024-01-01', 'end_date': '2025-01-01'}
        )
        self.assertEqual(response.status_code, 200)
        
        # Retrieve the computed revenue from the context passed to the template and round the floats of expected and computed revenue to 2d.p
        computed_revenue = float(response.context.get('total_revenue'))
        expected_revenue = round(expected_revenue,2)
        self.assertEqual(round(computed_revenue,2), round(expected_revenue,2))
        
        print(f"Computed Revenue = ${computed_revenue} : Expected Revenue = ${expected_revenue}")