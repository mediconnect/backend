from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.test import  APITestCase
import uuid

from .models import Disease
from staff.models.supervisor import Supervisor

class DiseaseModuleTest(APITestCase):

    def test_create_disease(self):
        """
        Ensure that we can create a hospital
        """
        user = User(email='demo4Disease@test.com', password=make_password('/.,Buz123'))
        user.save()
        supervisor = Supervisor(user=user)
        supervisor.save()
        self.client.force_login(supervisor.user)

        url = reverse('disease-list')
        data = {
            'id': uuid.uuid4(),
            'name': 'demo_disease',
            'keyword':'demo demo'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        disease = Disease.objects.get(name='demo_disease')
        self.client.logout()
