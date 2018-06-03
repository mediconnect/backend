"""
    We will store different url prefix here. You should include different
    url path handlers here instead of directly putting a specific url.
"""
from django.contrib import admin
from django.urls import path, include
# from patient import patient_module

urlpatterns = [
    path('api/customer/', include('customer.urls')),
    path('api/patient/', include('patient.views')),
    path('api/reservation/', include('reservation.views')),
    path('api/slot/', include('slot.views')),
    path('api/requirement/', include('requirement.views')),
]
