"""
    We will store different url prefix here. You should include different
    url path handlers here instead of directly putting a specific url.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('customer/', include('customer.urls')),
]
