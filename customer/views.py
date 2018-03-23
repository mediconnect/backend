from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from .serializers import CustomerSerializer, UserSerializer
from django.http import JsonResponse


class Register(APIView):
    """ View for handling registration request. """
    def post(self, request, format=None):
        data = JSONParser().parse(request)
        errors = {}

        user_serializer = UserSerializer(data=data['auth'])
        customer_serializer = CustomerSerializer(data=data['customer'])

        # Validate both data but leave the user foreign key as empty.
        if user_serializer.is_valid() and customer_serializer.is_valid() \
                and self._validate_password_confirmation(data['auth'], errors):
            user = user_serializer.save()

            # After saving user to DB, update the customer serializer.
            data['user'] = user.id
            customer_serializer = CustomerSerializer(data=data)
            if customer_serializer.is_valid():
                customer_serializer.save()
            return JsonResponse({"msg": "success"}, status=200)

        # Gather error from serializer. Because the strange design of Django
        # serializer, we need call is_valid before accessing its attributes.
        if not user_serializer.is_valid():
            for field, msg in user_serializer.errors.items():
                errors[field] = msg[-1]
        if not customer_serializer.is_valid():
            for field, msg in customer_serializer.errors.items():
                errors[field] = msg[-1]
        self._validate_password_confirmation(data['auth'], errors)
        return JsonResponse(errors, status=400)

    def _validate_password_confirmation(self, data, errors):
        """
            Because password_confirmation does not belong to any field.
            We use a protected method here for validating password_confirmation.

            Arguments:
                data: Auth data.
                errors: Error dictionary.

            Return:
                True, if no error. False, otherwise.
        """
        if 'password_confirmation' not in data:
            errors['password_confirmation'] = 'Cannot Be None'
            return False
        if data['password_confirmation'] != data['password']:
            errors['password_confirmation'] = 'Does not Match Password'
            return False
        return True
