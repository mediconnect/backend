from django.urls import path
from . import views

urlpatterns = [
    path('', views.Search.as_view(), name='search_hospital'),
    path('disease/', views.HospitalByDisease.as_view(), name='search_hospital_by_disease')
]
