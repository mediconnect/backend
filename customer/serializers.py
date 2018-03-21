from rest_framework import serializers
from . models import Customer
from django.contrib.auth.models import User


class CustomerSerializer(serializers.Serializer):
    class Meta:
        model = Customer
        fields = ('user', 'tel', 'address')

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
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


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

    email = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def create(self, validated_data):
        """ Create and return a new Customer instance, given the validated data. """
        return User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

    def update(self, instance, validated_data):
        """ Restrict User object update. """
        return instance
