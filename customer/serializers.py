from rest_framework import serializers
from . models import Customer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
import re


class CustomerRegistrationSerializer(serializers.Serializer):
    """
        Use customized fields here, because some fields are not equivalent to the
        original model.
    """

    # Declare when validate data this field can be optional, but
    # it is required while being saved to DB.
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    tel = serializers.CharField()
    address = serializers.CharField()

    def create(self, validated_data):
        """ Create and return a new Customer instance, given the validated data. """
        return Customer.objects.create(
            user=validated_data['user'],
            tel=validated_data['tel'],
            address=validated_data['address']
        )

    def update(self, instance, validated_data):
        """ Update and return an existing Customer instance, given the validated data. """
        instance.linenos = validated_data.get('tel', instance.linenos)
        instance.language = validated_data.get('address', instance.language)
        instance.save()
        return instance

    def validate(self, data):
        """ Validate all fields are filled. """
        for field in self.fields:
            if field == 'user':
                continue
            if field not in data or data[field] is None or len(data[field]) <= 0:
                raise serializers.ValidationError({field: ['Cannot Be Blank']})
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
        We use ModelSerializer here because this serializer is complete duplicate
        as our User model.
    """

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        """ Create and return a new Customer instance, given the validated data. """
        return User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

    def validate(self, data):
        """ Validate all fields are filled. """
        for field in self.fields:
            if field not in data or data[field] is None or len(data[field]) <= 0:
                raise serializers.ValidationError({field: ['Cannot Be Blank']})
        return data

    def validate_email(self, email):
        """ Validate email uniqueness and valid format. """
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise serializers.ValidationError('Please Enter Valid Email Format')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email Already Exists')
        return email

    def validate_password(self, password):
        """ Validate password is long enough. """
        if len(password) < 8:
            raise serializers.ValidationError('Password Must Be At Least 8 Characters')
        return make_password(password)


class UserLoginSerializer(serializers.ModelSerializer):
    """ Serializer for login user. """
    class Meta:
        model = User
        fields = ('email', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        """ Validate email exists in the DB. """
        for field in self.fields:
            if field not in data or data[field] is None or len(data[field]) <= 0:
                raise serializers.ValidationError({field: ['Cannot Be Blank']})

        email = data['email']
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': ['Email Does Not Exist']})
        elif not check_password(data['password'], User.objects.get(email=email).password):
            raise serializers.ValidationError({'password': ['Password Does Not Match']})

        return data

    def login(self):
        user = authenticate(username=self.data['email'])
        return user
