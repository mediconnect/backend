"""
    We will store different url prefix here. You should include different
    url path handlers here instead of directly putting a specific url.
"""
from django.contrib import admin
from django.urls import path, include
import hospital.views as hospital_views
import disease.views as disease_views
import supervisor.views as supervisor_views
# from patient import patient_module

urlpatterns = [
    path('api/customer/', include('customer.urls')),
    path('api/patient/', include('patient.views')),
    path('api/reservation/', include('reservation.views')),
    path('api/slot/', include('slot.views')),
    path('api/questionnaire', include('questionnaire.views')),
    # path('api/supervisor', include('supervisor.views')),
    # path('api/translator',include('translator.views')),
]+hospital_views.urlpatterns+disease_views.urlpatterns+supervisor_views.urlpatterns
