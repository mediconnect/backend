# rest framework
from rest_framework import serializers
# other
import re


def validate_password_complexity(password):
    """ Validate password is complicated enough. """
    if not re.match(r'[A-Za-z0-9!@#$%*^&+=]{8,}', password):
        raise serializers.ValidationError('密码必须至少包含：大写字母A-Z，小写字母a-z，数字0-9,特殊符号!@#$%^&*+=,长度至少为8')


def validate_email_format(email):
    """ Validate email uniqueness and valid format. """
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise serializers.ValidationError('邮箱格式不符合要求')

def validate_confirmed_password(confirmed_password):
    """Validate confirmed password"""
    def innerfn(password):
        print(password,dir(confirmed_password))
        if password != confirmed_password.get_value('condirmed_password'):
            raise serializers.ValidationError('Password doesn\'t match')
    return innerfn