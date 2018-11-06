#!/usr/bin/env python
# -*- coding: utf-8 -*-

# rest framework
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import routers, filters
from rest_framework.response import Response

# django
from django.urls import path
from django.contrib.auth.models import User
from django.core.mail import send_mail
from  django_filters.rest_framework import DjangoFilterBackend

# other
from atlas.permissions import SupPermission
from .serializers import ReservationAdminSerializer, ValidationSerializer
from reservation.models import Reservation


class ReservationAdminViewset(ModelViewSet):

    queryset = Reservation.objects.all()
    serializer_class = ReservationAdminSerializer
    filter_backends = (filters.OrderingFilter,DjangoFilterBackend,)
    filter_fields = '__all__'
    ordering_fields = '__all__'
    # permission_classes = [SupPermission]

    def create(self, request, *args, **kwargs):
        pass # not allowed


class ValidateOperation(APIView):

    def post(self, request,format=None):
        data = request.data.copy()
        data['user_id'] = request.user.id

        validation_serializer = ValidationSerializer(data=data)

        if validation_serializer.is_valid():

            return Response({'Msg':'Allowed'},status=200)
        else:
            errors = {}
            for field, msg in validation_serializer.errors.items():
                errors[field] = msg[-1]
        return Response({'Error':'Illegal Operation'},status=403)


class StaffSendEmail(APIView):

    def post(self,request):
        content = request.data['content']
        user_id = request.data['user_id']
        user = User.objects.get(user_id=user_id)
        errors = send_mail(
            '',
            content,
            user.email,
            'gabrielwry@gmail.com',
            fail_silently=False,
        )
        return Response({'errors':errors},status=200)


router = routers.SimpleRouter()

router.register(r'reservation/admin',
                ReservationAdminViewset,
                base_name='reservation/admin')
urlpatterns = router.urls +\
              [
               path('auth/validate',
                    ValidateOperation.as_view(),
                    name='validate-operation'),
               path('auth/send',
                    StaffSendEmail.as_view(),
                    name='staff-send-email')
               ]