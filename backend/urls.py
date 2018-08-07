"""
    We will store different url prefix here. You should include different
    url path handlers here instead of directly putting a specific url.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/customer/', include('customer.urls')),
    path('api/reservation/', include('reservation.views')),
    path('api/slot/', include('slot.views')),
    path('api/', include('supervisor.urls')),
    path('api/',include('document.views')),
    path('api/',include('hospital.views')),
    path('api/',include('disease.views')),
    path('api/',include('patient.views')),
]
