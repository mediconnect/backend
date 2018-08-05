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
        fields = ('email','password')

    def validate(self,data):
        email = data.get('email',None)
        password = data.get('password',None)
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email or Password doesn't Match")
        else:
            user = User.objects.get(email=email)
            if not check_password(password,user.password):
                raise serializers.ValidationError("Email or Password doesn't Match")
            else:
                if not Supervisor.objects.filter(user=user).exists():
                    raise serializers.ValidationError("Email or Password doesn't Match")
                else:
                    supervisor = Supervisor.objects.get(email=email)
                    data['id'] = supervisor.id

        return data

    def login(self,validated_data):
        user = authenticate(username=self.data['email'])
        supervisor = Supervisor(user=user)
        return supervisor

