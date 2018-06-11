from rest_framework import serializers
from .models import Reservation
from atlas.creator import create_optional_field_serializer


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = (
            "res_id", "user_id", "patient_id", "hospital_id", "disease_id",
            "ctime", "commit_at"
        )

        _on_commit_finalize_fields = ("timeslot", )


CompleteReservationSerializer = create_optional_field_serializer(ReservationSerializer)


class CreateReservationSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    patient_id = serializers.IntegerField()
    hospital_id = serializers.UUIDField()
    disease_id = serializers.IntegerField()
    timeslot_id = serializers.UUIDField()