def create_optional_field_serializer(Serializer):
    all_field_names = map(lambda field: field.name,
                          Serializer.Meta.model._meta.get_fields())

    class _optional_field_serializer(Serializer):
        class Meta(Serializer.Meta):
            extra_kwargs = {}

    return _optional_field_serializer