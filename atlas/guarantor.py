"""
Guarantor decorator
"""

from rest_framework.parsers import JSONParser
from django.http import JsonResponse

def use_serializer(Serializer):
    def _decorator(func):
        def wrapper(self, request, *args, **kwargs):
            payload = JSONParser().parse(request)
            payload_serializer = Serializer(data=payload)
            if not payload_serializer.is_valid():
                return JsonResponse(
                    payload_serializer.errors,
                    status=400
                )
            return func(self, payload_serializer.create(payload), *args, **kwargs)

        return wrapper
    return _decorator