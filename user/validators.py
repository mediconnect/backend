# rest framework
from rest_framework import serializers
# other
import re


def validate_password_complexity(password):
    """ Validate password is complicated enough. """
    if not re.match(r'[A-Za-z0-9!@#$%*^&+=.,/]{8,}', password):
        raise serializers.ValidationError('password complexity')

def validate_email_format(email):
    """ Validate email uniqueness and valid format. """
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise serializers.ValidationError('email')

def validate_confirmed_password(confirmed_password):
    """Validate confirmed password"""
    def innerfn(password):
        print(password,dir(confirmed_password))
        if password != confirmed_password.get_value('condirmed_password'):
            raise serializers.ValidationError('Password doesn\'t match')
    return innerfn