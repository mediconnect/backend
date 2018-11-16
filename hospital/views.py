from django.http import JsonResponse, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from rest_framework import routers, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Hospital
from .serializers import HospitalSerializer

from atlas.permissions import SupPermission
import json


class HospitalViewSet(ModelViewSet):
    serializer_class = HospitalSerializer
    queryset = Hospital.objects.all()
    filter_backends = (filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend)
    filter_fields = ('name','specialty')
    search_fields = ('=name','=specialty')
    ordering_fields = ('name', 'overall_rank')
    ordering = ('name','overall_rank',)

    def get_permissions(self):
        if self.action in ['create','update','destroy','partial_update']:
            permission_classes = [SupPermission,]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


router = routers.DefaultRouter()
router.register('', HospitalViewSet,base_name='hospital')
urlpatterns = router.urls
