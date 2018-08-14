from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import  check_password

from reservation.models import Reservation


class ReservationUpdateSerializer(serializers.ModelSerializer):
    """
    A serializer to update certain fields of a reservation.
    """
    translator_id = serializers.UUIDField()
    status = serializers.IntegerField()
    trans_status = serializers.IntegerField()
    note = serializers.CharField()

    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = (
            "res_id", "user_id", "patient_id", "hospital_id", "disease_id",
            "ctime", "commit_at"
        )


class ValidationSerializer(serializers.Serializer):
    """
    Serializer to valid user's pass word and authorize operation.
    """
    user_id = serializers.IntegerField()
    password = serializers.CharField()
    update_data = serializers.DictField()

    def __init__(self, *args, **kwargs):
        super(ValidationSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):


        user = User.objects.get(id=data['user_id'])
        update_data = data['update_data']

        # TODO: validate update data
        print(check_password(data['password'],user.password))
        if not check_password(data['password'], user.password):

            raise serializers.ValidationError({'authorization': ['Authorization Denied']})

        return data