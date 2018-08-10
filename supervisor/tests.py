from django.urls import reverse
from rest_framework import status
from rest_framework.test import  APITestCase

from .models import Supervisor,User
from customer.models import Customer


class CreateUserTest(APITestCase):

    def test_create_user(self):
        """
        Ensure that we can create users
        """

        url = reverse('user-list')
        data = {
            'email':'demo1@demo.com',
            'password':'Password123!',
            'confirmed_password':'Password123!',
            'first_name':'de',
            'last_name':'mo',
            'role':0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_log_in(self):
        url = reverse('supervisor-login')
        data = {
            'email':'demo1@demo.com',
            'password':'Password123!',
        }
        response = self.client.post(url,data,format = 'json')
        self.assertEqual(response.status_code,200)

