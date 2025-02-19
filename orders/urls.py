#orders\urls.py

from django.urls import path
from .views import revenue_index

urlpatterns = [
    path('',revenue_index, name="revenue-index"),
]