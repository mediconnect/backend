#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project
from customer.models import Customer
from supervisor.models import Supervisor
from translator.models import Translator

# rest_framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# django
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password

# other
from .validators import validate_email_format,validate_password_complexity,validate_confirmed_password


class UserSerializer(serializers.ModelSerializer):
    """ Base serializer for display user information."""
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',)
        write_only_fields = ('username',)

    def validate(self, data):
        # Making sure the username always matches the email
        email = data.get('email', None)
        if email:
            data['username'] = email

        return data

    def create(self, validated_data):

        validated_data['password'] = make_password(validated_data['password'])
        validated_data['username'] = validated_data['email']
        create_data = {k:v for k,v in validated_data.items()
                       if k in [x.name for x in User._meta.get_fields()]}
        user = User.objects.create_user(**create_data)

        if validated_data['role'] == 0: # customer type
            customer = Customer(user=user)

            return customer

        elif validated_data['role'] == 1: # supervisor type
            supervisor = Supervisor(user=user)

            return supervisor

        elif validated_data['role'] == 2: # c2e translator type
            translator = Translator(user=user,role=0)
            return translator

        elif validated_data['role'] == 3: # e2c translator type
            translator = Translator(user=user,role=1)
            return translator


class UserRegistrationSerializer(serializers.Serializer):
    """
        Use this as a base user type registration serializer, all other user type serializer can inherit this
    """
    # Declare fields needed
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all()),validate_email_format]
    )
    password = serializers.CharField(
        required = True,
        validators = [validate_password_complexity]
    )
    confirmed_password = serializers.CharField()

    first_name = serializers.CharField(required= True)
    last_name = serializers.CharField(required= True)
    role = serializers.IntegerField()

    def validate(self, data):
        if not data.get('password') or not data.get('confirmed_password'):
            raise serializers.ValidationError("Please enter a password and "
                                              "confirm it.")

        if data.get('password') != data.get('confirmed_password'):
            raise serializers.ValidationError("Those passwords don't match.")

        return data