from rest_framework import serializers
from .models import FileType

class FileTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileType
        fields = '__all__'
        read_only_fields = (
            "id", "extensions", "limit", "obsolete"
        )


class RequirementSerializer(serializers.Serializer):
    hospital_id = serializers.UUIDField()
    disease_id = serializers.IntegerField()
    types = serializers.PrimaryKeyRelatedField(queryset=FileType.objects.all(), many=True)

    @staticmethod
    def serialize_types(binary):
        return [i << 3 + j for i, b in enumerate(binary) for j, c in enumerate('{0:08b}'.format(b)[-1::1]) if c == '1']


    @staticmethod
    def deserialize_types(types):
        length = int(max(types) / 8)
        bitarr = bytearray([0]*length)

        for t in types:
            bitarr[t >> 3] |= (1 << (t & 7))

        return bytes(bitarr)

    @staticmethod
    def from_object(obj):
        return RequirementSerializer(dict(obj, types=RequirementSerializer.serialize_types(obj.require_list)))