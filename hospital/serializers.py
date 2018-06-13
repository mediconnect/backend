from rest_framework import serializers
from .models import Hospital
from atlas.creator import create_optional_field_serializer

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'