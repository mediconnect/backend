#!/usr/bin/env python
# -*- coding: utf-8 -*-

# rest framework
from rest_framework import serializers

# django
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate

# other
from . models import Supervisor
from customer.models import Customer
from translator.models import Translator

ROLE_CHOICES = (
    ('客户',0),
    ('管理员',1),
    ('汉译英',2),
    ('英译汉',3),
)

class SupervisorLoginSerializer(serializers.ModelSerializer):
    """
        Handle supervisor Login
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = Supervisor
        fields = ('user.email','user.password')

    def validate(self,data):
        email = data['email']
        password = data['password']
        if not User.objects.filter(email=email).exists()or not \
                check_password(password, User.objects.get(email=email).password):
            raise serializers.ValidationError('邮箱密码不正确')

        user = authenticate(username=self.data['email'])
        if not Supervisor.objects.filter(user=user).exists():
            raise serializers.ValidationError('邮箱密码不正确')
        return data

    def login(self):
        user = authenticate(username=self.data['email'])
        supervisor = Supervisor(user=user)
        return supervisor

