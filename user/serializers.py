#!/usr/bin/env python
# -*- coding: utf-8 -*-

# rest_framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# django
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate

# other
from .validators import validate_email_format,validate_password_complexity,validate_confirmed_password
import uuid


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
        Use this as a base user type registration serializer, all other user type serializer can inherit this
    """
    # Declare fields needed
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all()),validate_email_format]
    )
    password = serializers.CharField(
        required=True,
        validators=[validate_password_complexity,validate_confirmed_password]
    )
    confirmed_password = serializers.CharField()

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    role = serializers.ChoiceField(
        (
            (0,'Customer'),
            (1,'Supervisor'),
            (2,'Translator C2E'),
            (3,'Translator E2C'),
         ),default=0,required=False
    )
    tel = serializers.CharField(default='Not set',required=False)
    address = serializers.CharField(default='Not set',required=False)

    class Meta:
        model = User
        fields = ('email', 'password','confirmed_password', 'first_name', 'last_name','role','tel','address')

    def create(self, validated_data):
        """ Create and return a new Customer instance, given the validated data. """
        return User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

    def validate(self, data):
        if not data.get('password') or not data.get('confirmed_password'):
            raise serializers.ValidationError("Please enter a password and "
                                              "confirm it.")

        if data.get('password') != data.get('confirmed_password'):
            raise serializers.ValidationError("Those passwords don't match.")

        return data


class UserLoginSerializer(serializers.ModelSerializer):
    """ Serializer for login user. """

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, data):
        """ Validate email exists in the DB. """
        for field_name in self.fields:
            if field_name not in data or data[field_name] is None or len(data[field_name]) <= 0:
                raise serializers.ValidationError({field_name: ['Cannot Be Blank']})

        email = data['email']
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': ['Email Does Not Exist']})
        elif not check_password(data['password'], User.objects.get(email=email).password):
            raise serializers.ValidationError({'password': ['Password Does Not Match']})

        return data

    def login(self):
        user = authenticate(username=self.data['email'])
        return user