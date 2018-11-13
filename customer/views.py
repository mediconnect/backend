from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from .serializers import CustomerRegistrationSerializer, UserRegistrationSerializer, UserLoginSerializer, \
    CustomerProfileSerializer
from .models import Customer
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout

class Register(APIView):
    """ View for handling registration request. """

    def post(self, request, format=None):
        data = request.data
        errors = {}

        user_serializer = UserRegistrationSerializer(data=data['auth'])
        customer_serializer = CustomerRegistrationSerializer(data=data['customer'])

        user_info_valid, customer_info_valid = user_serializer.is_valid(), customer_serializer.is_valid()

        # Validate both data but leave the user foreign key as empty.
        if user_info_valid and customer_info_valid and self._validate_password_confirmation(data['auth'], errors):
            user = user_serializer.save()

            # After saving user to DB, update the customer serializer.
            data['customer']['user'] = user.id
            customer_serializer = CustomerRegistrationSerializer(data=data['customer'])
            customer_info_valid = customer_serializer.is_valid()
            if customer_info_valid:
                customer_serializer.save()
                return JsonResponse({
                    "msg": "success",
                    "user_id": user.id,
                    "customer_id": Customer.objects.get(user=user).id
                }, status=200)

        # Gather error from serializer. Because the strange design of Django
        # serializer, we need call is_valid before accessing its attributes.
        if not user_info_valid:
            for field, msg in user_serializer.errors.items():
                errors[field] = msg[-1]
        if not customer_info_valid:
            for field, msg in customer_serializer.errors.items():
                errors[field] = msg[-1]
        if user_info_valid and customer_info_valid:
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


class Login(APIView):
    """ View for handling login request. """

    def post(self, request, format=None):
        # data = None
        # print(type(request.data))
        # if isinstance(request,Request):
        #     data = request.data
        # elif isinstance(request,str):
        #     data = JSONParser().parse(request)
        # else:
        #     return JsonResponse({"Error":"Unsupported Type"},status=400)
        data = request.data
        errors = {}

        user_serializer = UserLoginSerializer(data=data)
        if user_serializer.is_valid():
            user = user_serializer.login()
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            return JsonResponse({
                    "msg": "success",
                    "user_id": user.id,
                    "customer_id": Customer.objects.get(user=user).id
                }, status=200)

        # Gather error from serializer. Because the strange design of Django
        # serializer, we need call is_valid before accessing its attributes.
        if not user_serializer.is_valid():
            for field, msg in user_serializer.errors.items():
                errors[field] = msg[-1]
        return JsonResponse(errors, status=400)


class Logout(APIView):
    """View for handling logout"""

    def post(self,request,format=None):
        logout(request)
        return JsonResponse({
            "msg":"success"
        },status=200)
        # return HttpResponseRedirect(content={"msg":"Logout"},status=200, redirect_to=reverse('search_hospital'))


class Profile(APIView):
    """ View for handling customer profile information. """

    def put(self, request, format=None):
        data = request.data

        customer_profile_serializer = CustomerProfileSerializer(data=data)

        # Gather error from serializer. Because the strange design of Django
        # serializer, we need call is_valid before accessing its attributes.
        errors = dict()
        if not customer_profile_serializer.is_valid():
            for field, msg in customer_profile_serializer.errors.items():
                errors[field] = msg[-1]
            return JsonResponse(errors, status=400)

        customer_profile_serializer.update_wrapper()
        return JsonResponse({"msg": "success"}, status=200)

    def get(self, request, format=None):
        id = request.query_params.get('id')
        data = {'id': id}

        customer_profile_serializer = CustomerProfileSerializer(data=data)

        # Gather error from serializer. Because the strange design of Django
        # serializer, we need call is_valid before accessing its attributes.
        errors = dict()
        if not customer_profile_serializer.is_valid():
            for field, msg in customer_profile_serializer.errors.items():
                errors[field] = msg[-1]
            return JsonResponse(errors, status=400)

        return JsonResponse(customer_profile_serializer.get(), status=200)
