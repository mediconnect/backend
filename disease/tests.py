from django.urls import reverse
from atlas.comparer import APITestClient

from rest_framework import status
from rest_framework.test import APITestCase
import uuid

from .models import Disease
from backend.common_test import CommonSetup


class DiseaseModuleTest(APITestCase):

    def setUp(self):
        self.client = APITestClient()
        self.dummy = CommonSetup(hospital=1,
                                 customer=1,
                                 patient=1)
        self.supervisor = self.dummy.supervisor

    def test_create_disease(self):
        """
        Ensure that we can create a hospital
        """
        self.client.force_login(self.supervisor)

        url = reverse('disease-list')
        data = {
            'name': 'demo_disease',
            'keyword': 'demo demo'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()
