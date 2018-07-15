#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid

# rest framework
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

# django
from django.http import JsonResponse

# other
from atlas.guarantor import use_serializer, any_exception_throws_400
from .serializers import ReservationUpdateSerializer,ValidationSerializer
from reservation.models import Reservation

class Update(APIView):

    @any_exception_throws_400
    @use_serializer(Serializer=ReservationUpdateSerializer, pass_in='data')
    def post(self, request,updated_fields, resid):

        if self.validate(request):
            reservation = Reservation.objects.get(res_id=resid)
            for attr, value in updated_fields.items():
                setattr(reservation, attr, value)
            reservation.save()

            return JsonResponse({'updated_fields': list(updated_fields.keys())})
        else:
            return JsonResponse(status=400)

    def validate(self, request,format=None):
        user =  request.user

        errors = {}
        data = JSONParser().parse(request)
        data['user'] = user
        validation_serializer = ValidationSerializer(data=data)

        if validation_serializer.is_valid():
            return True
        else:
            for field, msg in validation_serializer.errors.items():
                errors[field] = msg[-1]
        return False
