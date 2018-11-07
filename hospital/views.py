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
#     queryset = HospitalReview.objects.all()
#     serializer_class = HospitalReviewSerializer
#
#     def get_permissions(self):
#         """
#             Permission class based on action type
#         """
#         if self.action == 'comment':
#             permission_classes = [CanReviewPermission]
#             # TODO: This is not correct
#         else:
#             permission_classes = [SupPermission]
#
#         return [permission() for permission in permission_classes]
#
#     def post(self, payload, request, **kwargs):
#
#         if request.method == 'POST':
#             serializer = self.serializer_class(**payload)
#
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data,)
#             else:
#                 return Response(serializer.errors,)
#
#         # Return GET by default
#         else:
#             serializer = self.serializer_class(instance=self.queryset, many=True)
#
#             return Response(serializer.data)


# class LikeHospitalReviewViewSet(ModelViewSet):
#     queryset = LikeHospital.objects.all()
#     serializer_class = LikeHospitalSerializer
#
#     def get_permissions(self):
#         return [IsAuthenticated,]
#
#     def post(self, payload, request, **kwargs):
#
#         if request.method == 'POST':
#             serializer = self.serializer_class(**payload)
#
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, )
#             else:
#                 return Response(serializer.errors, )
#
#         # Return GET by default
#         else:
#             serializer = self.serializer_class(instance=self.queryset, many=True)
#
#             return Response(serializer.data)


router = routers.DefaultRouter()
router.register('', HospitalViewSet,base_name='hospital')
urlpatterns = router.urls
