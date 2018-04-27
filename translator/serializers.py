#!/usr/bin/env python
# -*- coding: utf-8 -*-

# rest framework
from rest_framework import serializers

# django
from django.contrib.auth.models import User

#other
from . models import Translator
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate

ROLE_CHOICES = (
    ('汉译英',1),
    ('英译汉',2),
)


class TranslatorLoginSerializer(serializers.ModelSerializer):
    """
        Handle translator Login
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = Translator
        fields = ('user.email','user.password')

    def validate(self,data):
        email = data['email']
        password = data['password']
        if not User.objects.filter(email=email).exists()or not \
                check_password(password, User.objects.get(email=email).password):
            raise serializers.ValidationError({'password': ['邮箱密码不正确']})

        user = authenticate(username=self.data['email'])
        if not Translator.objects.filter(user=user).exists():
            raise serializers.ValidationError({'password': ['邮箱密码不正确']})

        return data

    def login(self):
        user = authenticate(username=self.data['email'])
        translator = Translator(user=user)
        return translator
