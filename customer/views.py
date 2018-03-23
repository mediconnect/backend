from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from .serializers import CustomerSerializer, UserSerializer
from django.http import JsonResponse


class Register(APIView):
    """ View for handling registration request. """
    def post(self, request, format=None):
        data = JSONParser().parse(request)

        user_serializer = UserSerializer(data=data['auth'])
        customer_serializer = CustomerSerializer(data=data['customer'])

        # Validate both data but leave the user foreign key as empty.
        if user_serializer.is_valid() and customer_serializer.is_valid():
            user = user_serializer.save()

            # After saving user to DB, update the customer serializer.
            data['user'] = user.id
            customer_serializer = CustomerSerializer(data=data)
            if customer_serializer.is_valid():
                customer_serializer.save()
            return JsonResponse({"msg": "success"}, status=200)

        # Gather error from serializer. Because the strange design of Django
        # serializer, we need call is_valid before accessing its attributes.
        errors = {}
        if not user_serializer.is_valid():
            for field, msg in user_serializer.errors.items():
                errors[field] = msg
        if not customer_serializer.is_valid():
            for field, msg in customer_serializer.errors.items():
                errors[field] = msg
        return JsonResponse(errors, status=400)

