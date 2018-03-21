from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from .serializers import CustomerSerializer, UserSerializer
from django.http import JsonResponse


class Register(APIView):
    """ View for handling registration request. """
    def post(self, request, format=None):
        data = JSONParser().parse(request)

        user_data = {
            'email': data['email'],
            'password': data['password'],
            'first_name': data['first_name'],
            'last_name': data['last_name']
        }
        user_serializer = UserSerializer(data=user_data)

        if user_serializer.is_valid():
            user = user_serializer.save()
            customer_data = {
                'user': user.id,
                'tel': data['tel'],
                'address': data['address']
            }
            customer_serializer = CustomerSerializer(data=customer_data)

            print(customer_serializer)
            if customer_serializer.is_valid():
                print(customer_serializer.error_messages)
                customer_serializer.save()
                return JsonResponse(user_serializer.data, status=200)

        return JsonResponse(user_serializer.data, status=400)

