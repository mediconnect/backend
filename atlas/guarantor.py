"""
Guarantor decorator
"""

from rest_framework.parsers import JSONParser
from django.http import JsonResponse

def use_serializer(Serializer, pass_in='auto', many=False):
    def _decorator(func):
        def wrapper(self, request, *args, **kwargs):
            payload = JSONParser().parse(request)
            payload_serializer = Serializer(data=payload, many=many)

            payload_serializer.is_valid(raise_exception=True)
            return func(self,
                        payload_serializer if not (pass_in == 'data') else payload_serializer.data,
                        *args, **kwargs)

        return wrapper
    return _decorator