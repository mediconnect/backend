from django.urls import reverse
from rest_framework import status
from rest_framework.test import  APITestCase

from .models import Supervisor,User
from customer.models import Customer


class CreateUserTest(APITestCase):

    def test_create_user(self):
        """
        Ensure that we can create a hospital
        """
        url = reverse('user-list')
        data = {
            'email':'demo1@demo.com',
            'password':'password',
            'confirmed_password':'password',
            'first_name':'de',
            'last_name':'mo',
            'role':0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email='demo1@demo.com')
        customer = Customer.objects.get(user=user)
        self.assertEqual(customer.user.email,'demo1@demo.com')
