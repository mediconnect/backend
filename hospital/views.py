from django.http import JsonResponse, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from rest_framework import routers, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Hospital, HospitalReview,LikeHospital
from .serializers import HospitalSerializer, HospitalReviewSerializer,LikeHospitalSerializer

from atlas.permissions import SupPermission, CanReviewPermission
import json


class HospitalViewSet(ModelViewSet):
    serializer_class = HospitalSerializer
    queryset = Hospital.objects.all()
    filter_backends = (filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend)
    filter_fields = ('name','specialty')
    search_fields = ('=name','=specialty')
    ordering_fields = ('name', 'overall_rank')
    ordering = ('name','overall_rank',)

    # def get_permissions(self):
    #     if self.action == 'create':
    #         # If not original file, only supervisor and translator can create
    #         permission_classes = [SupPermission]
    #     else:
    #         permission_classes = []
    #
    #     return [permission() for permission in permission_classes]

    # def get_queryset(self):
    #     """
    #     Filter/sort by query param in url
    #     """
    #     queryset = Hospital.objects.all()
    #     query_dic = {}
    #
    #     for field in Hospital._meta.get_fields():
    #         if field.name in self.request.query_params:
    #             query_dic[field.name] = self.request.query_params.get(field.name)
    #     queryset = queryset.filter(**query_dic)
    #     order_by = self.request.query_params.get('_order',None)
    #     if order_by:
    #         queryset.order_by(order_by)
    #     return queryset


# class HospitalReviewViewSet(ModelViewSet):
#     serializer_class = HospitalReviewSerializer
#     filter_backends = (filters.OrderingFilter,DjangoFilterBackend)
#     filter_fields = ('hospital','disease','customer')
#     ordering_fields = ('score',)
#     ordering = ('score',)
#
#     def get_queryset(self):
#         hospital_id = self.kwargs['hospital_id']
#         disease_id = self.kwargs['disease_id']
#         return HospitalReviewSerializer.objects.filter(hospital_id=hospital_id,disease_id=disease_id)
#
#     def create(self, request, *args, **kwargs):
#         customer_id=self.kwargs['customer_id']
#         hospital_id


router = routers.DefaultRouter()
router.register('', HospitalViewSet,base_name='hospital')
urlpatterns = router.urls
