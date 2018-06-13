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
from user.serializers import UserRegistrationSerializer,UserSerializer

ROLE_CHOICES = (
    ('客户',0),
    ('管理员',1),
    ('汉译英',2),
    ('英译汉',3),
)


class SupervisorSerializer(UserSerializer):
    """ For display supervisor information purpose."""
    role = serializers.CharField(read_only=True,default='管理员')

    class Meta:
        model = Supervisor
        fields = 'role'


class TranslatorSerializer(UserSerializer):
    """ For display translator information purpose."""

    class Meta:
        model = Supervisor
        fields = 'role'


class CustomerSerializer(serializers.ModelSerializer):
    """ For display translator information purpose."""
    class Meta:
        model = Customer
        fields = ('tel','address','wechat','qq')


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


class CreateUserSerializer(UserRegistrationSerializer):
    """
        Handle supervisor registration
    """
    tel = serializers.CharField()
    address = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'])
        if validated_data['role'] == 0:  # create a customer type user
            if not validated_data['tel'] or not validated_data['address']:  # customer type user requires tel and address info
                raise serializers.ValidationError('信息填写不完整')
            customer = Customer(user=user)
            return customer.user_id
        if validated_data['role'] == 1:  # create a supervisor type user
            supervisor = Supervisor(user=user)
            return supervisor.user_id
        if validated_data['role'] == 2:  # create a translator_C2E type user
            translator = Translator(user=user,role=0)
            return translator.user_id
        if validated_data['role'] == 3:  # create a translator_E2C type user
            translator = Translator(user=user,role=1)
            return translator.user_id


