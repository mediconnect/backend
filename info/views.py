from django.http import JsonResponse, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from rest_framework import routers, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Info, LikeInfo
from customer.models import Customer
from .serializers import InfoSerializer, LikeInfoSerializer
from atlas.permissions import IsOwner, CanReviewPermission
import json


class InfoViewSet(ModelViewSet):
    serializer_class = InfoSerializer
    queryset = Info.objects.all()
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    filter_fields = ('disease', 'hospital')
    search_fields = ('=disease__name', '=hospital__name')
    ordering_fields = ('disease', 'hospital', 'rank', 'deposit', 'full_price')
    ordering = ('rank', 'deposit', 'full_price')

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


class LikeInfoViewSet(ModelViewSet):
    serializer_class = LikeInfoSerializer
    filter_backends = (filters.OrderingFilter,DjangoFilterBackend,filters.SearchFilter,)
    filter_fields = ('info__disease__name',)
    ordering_fields = ('info__rank', 'info__deposit','info__full_price','info__feedback_time')
    permission_classes = [IsAuthenticated,IsOwner]

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        return LikeInfo.objects.all().filter(customer__id = customer_id)

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.id != Customer.objects.get(id=self.kwargs['customer_id']).user_id:
            return Response({'error':'Not Allowed'},status=403)
        customer_id = int(self.kwargs['customer_id'])
        data = request.data.copy()
        data['customer'] = customer_id
        serializer = LikeInfoSerializer(data=data)
        if serializer.is_valid():
            like_info = serializer.save()
            return Response({'msg':'created',
                             'id':like_info.id},
                            status=201)
        else:
            return Response(serializer.errors,status=400)


router = routers.DefaultRouter()
router.register('', InfoViewSet,base_name='info')
router.register('like/<(?P<customer_id>[^/.]+)',LikeInfoViewSet, base_name='like-info')
urlpatterns = router.urls
