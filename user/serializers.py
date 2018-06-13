#!/usr/bin/env python
# -*- coding: utf-8 -*-

# rest_framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# django
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# other
from .validators import validate_email_format,validate_password_complexity


class UserSerializer(serializers.ModelSerializer):
    """ Base serializer for display user information."""
    class Meta:
        model = User
        exclude = ('password','is_supervisor','is_staff','username',)


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
        required = True,
        validators = [validate_password_complexity]
    )
    confirmed_password = serializers.CharField(
        required = True,
        # validators = [validate_password_match(password=password)]
    )

    first_name = serializers.CharField(required= True)
    last_name = serializers.CharField(required= True)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        make_password(validated_data['password']))
        return user

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name','tel','address')