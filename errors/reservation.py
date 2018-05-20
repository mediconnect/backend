class ImmutableStatusException(Exception):
    pass


class ImmutableFieldException(Exception):
    def __init__(self, field, when=""):
        super().__init__('"{field}" cannot be changed{cond}!'.format(field=field, cond=" " + when if len(when) else ""))


class InsufficientSpaceException(Exception):
    def __init__(self):
        super().__init__("Can't add reservation to a full time slot")