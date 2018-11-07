from rest_framework import serializers
from .models import Customer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
import re


class CustomerProfileSerializer(serializers.Serializer):
    """
        Customized customer information serializer.
    """

    # Declare when validate data this field can be optional, but
    # it is required while being saved to DB.
    id = serializers.IntegerField()
    tel = serializers.CharField(required=False)
    address = serializers.CharField(required=False)

    def create(self, validated_data):
        self.instance = Customer.objects.get(id=self.validated_data['id'])
        self.user = self.instance.user
        return self.instance

    def update_wrapper(self):
        self.instance = Customer.objects.get(id=self.validated_data['id'])
        self.update(self.instance, self.validated_data)

    def update(self, instance, validated_data):
        instance.tel = validated_data['tel']
        instance.address = validated_data['address']
        instance.save()

    def get(self):
        self.instance = Customer.objects.get(id=self.validated_data['id'])
        self.user = self.instance.user
        self.validated_data['tel'] = self.instance.tel
        self.validated_data['address'] = self.instance.address

        ukeys = ['first_name', 'last_name', 'email']
        data = dict()
        for field in ukeys:
            data[field] = self.user.serializable_value(field)

        data['tel'] = self.validated_data['tel']
        data['address'] = self.validated_data['address']
        return data

    def validate(self, data):
        for field_name in self.fields:
            field = self.fields[field_name]
            if field.required and (field_name not in data or data[field_name] is None):
                raise serializers.ValidationError({field: ['Cannot Be Blank']})
        return data


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
        pass

    def validate(self, data):
        """ Validate all fields are filled. """
        for field_name in self.fields:
            if field_name == 'user':
                continue
            if field_name not in data or data[field_name] is None or len(data[field_name]) <= 0:
                raise serializers.ValidationError({field_name: ['Cannot Be Blank']})
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
        for field_name in self.fields:
            if field_name not in data or data[field_name] is None or len(data[field_name]) <= 0:
                raise serializers.ValidationError({field_name: ['Cannot Be Blank']})
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
        authenticate(username=self.data['email'])
        return User.objects.get(username=self.data['email'])
