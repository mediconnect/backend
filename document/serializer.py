from rest_framework import serializers
from document.models import Document


class DocumentSerializer(serializers.ModelSerializer):
    upload_by = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = (
            "id", "owner", "upload_at", "resid", "data",
        )