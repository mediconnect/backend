from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.Serializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ('user_id',)

    def create(self, validated_data):
        return Patient.objects.create(**validated_data)