#!/usr/bin/env python
# -*- coding: utf-8 -*-

# rest framework
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status,permissions

#django
from django.shortcuts import render
from django.http import JsonResponse

#other
from .serializers import TranslatorLoginSerializer
class Login(APIView):
    """ View for handling supervisor login request. """

    def post(self, request):
        data = JSONParser().parse(request)
        errors = {}

        translator_serializer = TranslatorLoginSerializer(data=data)
        if translator_serializer.is_valid():
            translator_serializer.login()
            return JsonResponse({"msg": "success"}, status=200)

        if not translator_serializer.is_valid():
            for field, msg in translator_serializer.errors.items():
                errors[field] = msg[-1]
        return JsonResponse(errors, status=400)
