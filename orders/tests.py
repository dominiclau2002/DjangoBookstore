from django.test import TestCase
from .models import Book, Order, OrderItem, OrderItemBook
# Create your tests here.
class OrderTestCase(TestCase):
    def test_order_creation(self):
        book = Book.objects.create(name="Test Book", author="Test Author", price=10.00)
        order = Order.objects.create(status='PENDING')
        order_item = OrderItem.objects.create(order=order)
        order_item_book = OrderItemBook.objects.create(order_item=order_item, book=book, quantity=2)

        self.assertEqual(order.status, 'PENDING')
        self.assertEqual(order_item_book.quantity, 2)
        self.assertEqual(order_item_book.book.name, "Test Book")
        self.assertEqual(order_item_book.price_at_order, 10.00)