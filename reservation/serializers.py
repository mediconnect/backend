from rest_framework import serializers
from .models import Reservation
from atlas.creator import create_optional_field_serializer

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ("user_id", "patient_id", "hospital_id", "disease_id", "ctime")


CompleteReservationSerializer = create_optional_field_serializer(ReservationSerializer)


class CreateReservationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    patient_id = serializers.IntegerField()
    hospital_id = serializers.IntegerField()
    disease_id = serializers.IntegerField()
    slot_id = serializers.IntegerField()