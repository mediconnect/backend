"""
    We will store different url prefix here. You should include different
    url path handlers here instead of directly putting a specific url.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/customer/', include('customer.urls')),
    path('api/patient/', include('patient.views')),
    path('api/reservation/', include('reservation.views')),
    path('api/slot/', include('slot.views')),
    path('api/supervisor/', include('supervisor.urls')),
    path('api/document/',include('document.views')),
    path('api/hospital/',include('hospital.views')),
    path('api/disease/',include('disease.views')),
]
