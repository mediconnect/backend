from django.http import JsonResponse, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from rest_framework import routers, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Info
from .serializers import InfoSerializer
from atlas.permissions import SupPermission, CanReviewPermission
import json


class InfoViewSet(ModelViewSet):
    serializer_class = InfoSerializer
    queryset = Info.objects.all()
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    filter_fields = ('disease', 'hospital')
    search_fields = ('=disease', '=hospital')
    ordering_fields = ('disease', 'hospital', 'rank', 'deposit', 'full_price')
    ordering = ('rank', 'deposit', 'full_price')


router = routers.DefaultRouter()
router.register('', InfoViewSet,base_name='info')
urlpatterns = router.urls
