###
# Private generic exception class
###
class _GeneralLimitedException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

        self.stack_limit = 0


###
# General public throwables
###

class InvalidArgumentException(Exception):
    pass


# we may not need this
class InsufficientPermissionException(Exception):
    pass