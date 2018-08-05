from django.urls import path
from . import views

urlpatterns = [
    path('^supervisor/login/', views.Login.as_view(), name='supervisor-login'),
]+views.urlpatterns
