"""
Guarantor decorator
"""

from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from .creator import create_general_exception_response_body

def use_serializer(Serializer, pass_in='auto', many=False):
    # A decorator to read in payload to functions
    def _decorator(func):
        def wrapper(self, request, *args, **kwargs):
            payload = JSONParser().parse(request)
            payload_serializer = Serializer(data=payload, many=many)

            payload_serializer.is_valid(raise_exception=True)
            return func(self,
                        payload_serializer if not (pass_in == 'data') else payload_serializer.validated_data,
                        *args, **kwargs)

        return wrapper
    return _decorator


def on_exception_response(exception_or_list, status=400):
    if isinstance(exception_or_list, type):
        all_exceptions = (exception_or_list, )
    else:
        all_exceptions = tuple(exception_or_list)

    def _decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except all_exceptions as e:
                print(str(e))
                return JsonResponse({
                    'error': type(e).__name__,
                    'detail': str(e)
                }, status=status)
        return wrapper
    return _decorator


any_exception_throws_400 = on_exception_response(Exception)
