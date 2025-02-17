from django.db import models

# Create your models here.

#Create Book model
class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10,decimal_places=2) #current retail price of the book
    
    #Display name of Book instance when called
    def __str__(self):
        return self.name

#Create Order model
class Order(models.Model):
    
    #Define options for order status
    class OrderStatusChoices(models.TextChoices):
        #Actual Value        #Displayed on Django Admin
        PENDING = 'PENDING', 'Pending'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
    
    order_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10,choices=OrderStatusChoices.choices, default=OrderStatusChoices.PENDING)
    
    #Displayed when the Order instance is converted to a string, e.g Order 1 - PENDING
    def __str__(self):
        return f"Order {self.id} - {self.status}"

#Create OrderItem model
class OrderItem(models.Model):
    
    #set up a one-to-many relationship: One Order can have many OrderItem instances
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    book = models.ManyToManyField(Book, through='OrderItemBook') #create a many-to-many relationship with Book and OrderItem, with through model OrderItemBook to store qty and price of book
    
    

    def __str__(self):
        books_info = ", ".join([f"{item.book.name} - {item.quantity} x ${item.price_at_order}"
                              for item in self.order_items.all()])
        return f"OrderItem {self.id} - {books_info}"
    
#Create through model for many-to-many relationship
class OrderItemBook(models.Model):
    
    order_item = models.ForeignKey(OrderItem, related_name="order_items" ,on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  # Quantity of this specific book in the order item
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the book at the time of the order
    
    def save(self, *args, **kwargs): #automatically assign the book_price based on the associated Book object's price if book_price is not explicitly set when creating OrderItem
        if not self.price_at_order:
            self.price_at_order = self.book.price #assign the book's price to price_at_order
        super().save(*args,**kwargs)
        
    def __str__(self):
        return f"OrderItemBook {self.id} - {self.book.name} - {self.quantity} x ${self.price_at_order}"