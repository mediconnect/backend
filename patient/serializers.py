from rest_framework import serializers
from .models import Patient
from atlas.creator import create_optional_field_serializer

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ('id',)

OptionalPatientSerializer = create_optional_field_serializer(PatientSerializer)