class ImmutableStatusException(Exception):
    pass


class ImmutableFieldException(Exception):
    def __init__(self, field):
        super().__init__('"{field}" cannot be changed!'.format(field=field))