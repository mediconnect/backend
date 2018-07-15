from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password


class ReservationUpdateSerializer(serializers.ModelSerializer):
    """
    A serializer to update certain fields of a reservation.
    """
    translator_id = serializers.UUIDField()
    status = serializers.IntegerField()
    trans_status = serializers.IntegerField()
    note = serializers.CharField()

class ValidationSerializer(serializers.ModelSerializer):
    """
    Serializer to valid user's pass word and authorize operation.
    """
    class Meta:
        model = User
        fields = ('password')

    def __init__(self, *args, **kwargs):
        super(ValidationSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        """ Validate email exists in the DB. """
        for field in self.fields:
            if field not in data or data[field] is None or len(data[field]) <= 0:
                raise serializers.ValidationError({field: ['Cannot Be Blank']})

        user = data['user']
        status = data['status']
        allowed_status = data['allowed_status']
        if not check_password(data['password'], user.password):
            raise serializers.ValidationError({'authorization': ['Authorization Denied']})

        if not status in allowed_status:
            raise serializers.ValidationError({
                'authorization': ['This operation cannot be performed at this time']})

        return data