import copy

def create_optional_field_serializer(Serializer):
    all_field_names = map(lambda field: field.name,
                          Serializer.Meta.model._meta.get_fields())
    new_extra_kwargs = copy.deepcopy(Serializer.Meta.extra_kwargs or {})
    for name in all_field_names:
        new_extra_kwargs[name] = new_extra_kwargs.get(name, {})
        new_extra_kwargs[name]['required'] = False

    class _optional_field_serializer(Serializer):
        class Meta(Serializer.Meta):
            extra_kwargs = new_extra_kwargs

    return _optional_field_serializer