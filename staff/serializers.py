#!/usr/bin/env python
# -*- coding: utf-8 -*-

# rest framework
from rest_framework import serializers

# other
from . models.supervisor import Supervisor
from .models.translator import Translator

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout


class TranslatorSerializer(serializers.ModelSerializer):
    role = serializers.IntegerField

    class Meta:
        model = Translator
        fields = ('user','role',)

    def create(self, validated_data):
        """ Create and return a new Translator instance, given the validated data. """
        return Translator.objects.create(user=validated_data['user'],
                                         role= validated_data['role'])

    def validate(self, data):
        """ Validate all fields are filled. """
        # print(data)
        if 'role' not in data:
            raise serializers.ValidationError({'role': ['Cannot Be Blank']})
        return data


class SupervisorSerializer(serializers.ModelSerializer):
    role = serializers.IntegerField()

    class Meta:
        model = Supervisor
        fields = ('user','role')

    def create(self, validated_data):
        """ Create and return a new Supervisor instance, given the validated data. """
        return Supervisor.objects.create(user=validated_data['user'])

    def validate(self, data):
        print(data)
        """ Validate all fields are filled. """
        if 'role' not in data:
            raise serializers.ValidationError({'role': ['Cannot Be Blank']})
        return data


class StaffLoginSerializer(serializers.ModelSerializer):
    """ Serializer for login staff. """

    class Meta:
        model = User
        fields = ('email', 'password',)

    def __init__(self, *args, **kwargs):
        super(StaffLoginSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        """ Validate email exists in the DB. """
        for field_name in self.fields:
            if field_name not in data or data[field_name] is None or len(data[field_name]) <= 0:
                raise serializers.ValidationError({field_name: ['Cannot Be Blank']})

        email = data['email']
        # print(data['password'], User.objects.get(email=email).password)
        if not User.objects.filter(email=email).exists() or \
                not check_password(data['password'], User.objects.get(email=email).password):

            raise serializers.ValidationError({'error': ['1Email Does Not Exist']})

        else:
            user = User.objects.get(email=email)
            # print(Translator.objects.filter(user=user))
            if not Translator.objects.filter(user=user).exists() and \
                    not Supervisor.objects.filter(user=user).exists():

                raise serializers.ValidationError({'error': ['2Email Does Not Exist']})

        return data

    def login(self,request):
        user = authenticate(request,username=self.data['email'],password=self.data['password'])
        if user is not None:
            login(request,user)
        else:
            raise serializers.ValidationError({'msg':'Authentication Failed'})
        return User.objects.get(username=self.data['email'])

    def logout(self,request):
        logout(request)