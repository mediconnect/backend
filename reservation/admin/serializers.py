from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from reservation.models import Reservation


class ReservationUpdateSerializer(serializers.ModelSerializer):
    """
    A serializer to update certain fields of a reservation.
    """

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
    allowed_state = serializers.HiddenField(default = [1,])
    allowed_trans_state =  serializers.HiddenField(default=[1,])
    required_asset = serializers.HiddenField(default = [0,])

    def __init__(self,*args, **kwargs):
        update_data = kwargs['data']['update_data']
        res_id = update_data['res_id']
        res = Reservation.objects.get(res_id=res_id)
        if res.status == 0:
            self.allowed_state =[1,]
            self.allowed_trans_state = [1,]
            self.required_asset = [0,]
        elif res.status == 1:
            self.allowed_state = serializers.HiddenField(default = [0,2,])
            self.required_asset = serializers.HiddenField(default =  [0,1,])
        super(ValidationSerializer, self).__init__(*args, **kwargs)

    def validate(self, data,*args,**kwargs):

        user = User.objects.get(id=data['user_id'])
        update_data = data['update_data']
        print(update_data)
        # TODO: validate update data
        if update_data['status'] not in self.allowed_state or update_data['trans_status'] not in  self.allowed_trans_state:
            raise serializers.ValidationError({
                'Authorization': "Illegal Update"
            })
        print(check_password(data['password'],user.password))

        if not check_password(data['password'], user.password):

            raise serializers.ValidationError({'authorization': ['Authorization Denied']})

        return data
