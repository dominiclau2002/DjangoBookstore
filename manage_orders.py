#manage_orders.py
import os
import django
from datetime import datetime

#Tells python to use the bookstore.settings file as the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE','bookstore.settings')
django.setup()

#import order models from orders/models.py
from orders.models import Book, Order, OrderItem, OrderItemBook

#function to create a Book object
def create_book(name,author,price):
    #if book is not in database, create Book object with name,author and price. If it already exists, created = False, return existing book
    book,created = Book.objects.get_or_create(name=name,author=author, defaults={'price' : price})
    if created:
        print(f"Book '{name}' added successfully!")
    else:
        print(f"Book '{name}' already exists!")
    
    return book

#UPDATE a Book (e.g., change the price)
def update_book(book_id, new_name=None, new_author=None, new_price=None):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        print(f"Book with ID {book_id} not found.")
        return

    if new_name:
        book.name = new_name
    if new_author:
        book.author = new_author
    if new_price is not None:
        book.price = new_price
    book.save()
    print(f"Book '{book.id}' updated successfully!")

#DELETE a Book
def delete_book(book_id):
    try:
        book = Book.objects.get(id=book_id)
        book.delete()
        print(f"Book '{book_id}' deleted successfully!")
    except Book.DoesNotExist:
        print(f"Book with ID {book_id} not found.")
        
#Define a function to create an Order, optionally accepting a custom date/time and status
def create_order(order_date=None, status=None):
    
    order_args = {} #Dictionary to store order arguments passed by the user
    if order_date:
        order_args['order_date'] = order_date #If user passed a date/time, use it
    if status:
        order_args['status'] = status #If user passed a order status, use it
        
     # Create the Order object in the database with the given arguments (or defaults)
    order = Order.objects.create(**order_args)
    print(f"Order {order.id} created with date {order.order_date} and status {order.status}.")
    return order

#UPDATE an Order (e.g., change the status)
def update_order(order_id, new_status=None):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        print(f"Order with ID {order_id} not found.")
        return

    if new_status:
        order.status = new_status
    order.save()
    print(f"Order '{order.id}' updated successfully! (Status: {order.status})")

# DELETE an Order
def delete_order(order_id):
    try:
        order = Order.objects.get(id=order_id)
        order.delete()
        print(f"Order '{order_id}' deleted successfully!")
    except Order.DoesNotExist:
        print(f"Order with ID {order_id} not found.")

#Define a function to link a Book to an existing Order via OrderItem and OrderItemBook
def add_order_item(order_id, book_id, quantity=1):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        print(f"Error: Order with ID {order_id} does not exist")
        return
    
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        print(f"Error: Book with ID {book_id} does not exist")
        return
    
    #Check if there is an existing OrderItem for this Order or create a new one
    order_item, created = OrderItem.objects.get_or_create(order=order)
    
    #create the through-model record linking the Book and the OrderItem
    OrderItemBook.objects.create(
        order_item = order_item,
        book = book,
        quantity = quantity,
        price_at_order = book.price
    )
    
    print(f"Added {quantity} x '{book.name}' to Order {order.id}.")
    

#Define a function to display all Orders and their associated Books
def view_orders():
    orders = Order.objects.all()
    if not orders:
        print("No orders found")
        return
    
    for order in orders:
        print(f"\nID: {order.id} - Order {order.id} - {order.status} - {order.order_date}")
        for order_item in order.items.all():
            #order_item.order_items references the related OrderItemBook entries
            for order_item_book in order_item.order_items.all():
                print(f"   - Book: {order_item_book.book.name} "
                      f"| Qty: {order_item_book.quantity} "
                      f"| Price at Order: ${order_item_book.price_at_order}")
                
#Function to view all book objects
def view_books():
    books = Book.objects.all()
    if not books:
        print("No books found.")
        return

    print("\n=== All Books ===")
    for book in books:
        print(f"ID: {book.id} | Name: {book.name} | Author: {book.author} | Price: {book.price}")


#The main menu function providing a CLI interface
def main():
    while True:
        print("\n=== Bookstore Management ===")
        print("1. Add a new book")
        print("2. Update a book")
        print("3. Delete a book")
        print("4. Create a new order")
        print("5. Update an order")
        print("6. Delete an order")
        print("7. Add books to an order")
        print("8. View all orders")
        print("9. View all books")  # <-- new
        print("10. Exit")

        choice = input("Enter your choice: ")
        
        # (1) CREATE a new book
        if choice == "1":
            name = input("Enter book name: ")
            author = input("Enter book author: ")
            price = float(input("Enter book price: "))
            create_book(name, author, price)

        # (2) UPDATE a book
        elif choice == "2":
            try:
                book_id = int(input("Enter the Book ID to update: "))
            except ValueError:
                print("❌ Book ID must be a number.")
                continue
            new_name = input("Enter new book name (or leave blank): ")
            new_author = input("Enter new author (or leave blank): ")
            new_price_input = input("Enter new price (or leave blank): ")
            new_price = float(new_price_input) if new_price_input else None
            update_book(book_id, new_name or None, new_author or None, new_price)

        # (3) DELETE a book
        elif choice == "3":
            try:
                book_id = int(input("Enter the Book ID to delete: "))
                delete_book(book_id)
            except ValueError:
                print("❌ Book ID must be a number.")
        
        # (4) CREATE a new order
        elif choice == "4":
            custom_date = input("Enter date/time for order (YYYY-MM-DD HH:MM) or blank for now: ")
            if custom_date.strip():
                try:
                    order_date_obj = datetime.strptime(custom_date, "%Y-%m-%d %H:%M")
                except ValueError:
                    print("Invalid date/time format. Using the current time instead.")
                    order_date_obj = None
            else:
                order_date_obj = None
            
            status_input = input("Enter status (PENDING, COMPLETED, CANCELLED) or blank for default: ").upper()
            if status_input not in ["", "PENDING", "COMPLETED", "CANCELLED"]:
                print("Invalid status; using default PENDING.")
                status_input = None
            elif status_input == "":
                status_input = None
            
            create_order(order_date=order_date_obj, status=status_input)

        # (5) UPDATE an order
        elif choice == "5":
            try:
                order_id = int(input("Enter the Order ID to update: "))
            except ValueError:
                print("❌ Order ID must be a number.")
                continue
            new_status = input("Enter new status (PENDING, COMPLETED, CANCELLED) or blank to skip: ").upper()
            if new_status not in ["", "PENDING", "COMPLETED", "CANCELLED"]:
                print("Invalid status; skipping update.")
                new_status = None
            elif new_status == "":
                new_status = None
            update_order(order_id, new_status)

        # (6) DELETE an order
        elif choice == "6":
            try:
                order_id = int(input("Enter the Order ID to delete: "))
                delete_order(order_id)
            except ValueError:
                print("❌ Order ID must be a number.")

        # (7) ADD books to an existing order
        elif choice == "7":
            try:
                order_id = int(input("Enter order ID: "))
                book_id = int(input("Enter book ID: "))
                quantity = int(input("Enter quantity: "))
                add_order_item(order_id, book_id, quantity)
            except ValueError:
                print("Invalid ID or quantity. Must be a number.")

        # (8) VIEW all orders
        elif choice == "8":
            view_orders()

        # (9) VIEW all books
        elif choice == "9":
            view_books()
            
        #EXIT the program
        elif choice == "10":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please try again.")


# (12) Run the main function when file is run directly
if __name__ == "__main__":
    main()