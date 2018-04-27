# django
from django.http import JsonResponse,Http404
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.parsers import JSONParser
from .models import Supervisor,User


class AccountTests(APITestCase):
    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse('create-user')
        data = {'role': 1,
                'username':'aaa@aa.com',
                'first_name':'test',
                'last_name':'superviosr',
                'email':'aaa@aa.com',
                'password':'password',
                'tel':'None',
                'address':'None',
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_ID = response.data['user_ID']
        user = User.objects.get(id = user_ID)
        self.assertEqual(user.username, 'aaa@aa.com')
        self.assertEqual(user.email,'aaa@aa.com')
        print(user.password)
        self.assertEqual(Supervisor.objects.filter(user = user_ID).count(),1)
        self.assertEqual(Supervisor.objects.filter(user = user_ID).count(),1)

    def test_list_supervisor(self):
        """
        Ensure we can list all users
        """
        url = reverse('supervisor-list')
