from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, URLPatternsTestCase
import json
import uuid

from .models import Hospital

class HospitalModuleTest(APITestCase):

    def test_create_hospital(self):
        """
        Ensure that we can create a hospital
        """
        url = reverse('hospital-list')
        data = {
            'id': uuid.uuid4(),
            'name': 'demo_hospital',
            'email':'demo@demo.com',
            'overall_rank':1,
            'average_score':0.0,
            'review_number':10
        }
        print(url)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)