from django.urls import reverse
from rest_framework import status
from rest_framework.test import  APITestCase

from .models import Document
from  reservation.models import Reservation
from customer.models import User,Customer
from patient.models import Patient
import uuid
import datetime

class UploadFileTest(APITestCase):

    def test_create_document(self):
        """
        Ensure that we can create document
        """
        url = reverse('user-list')
        user_data = {
            'email': 'demo1@demo.com',
            'password': 'Password123!',
            'confirmed_password': 'Password123!',
            'first_name': 'de',
            'last_name': 'mo',
            'role': 0
        }
        response = self.client.post(url, user_data, format='json')

        customer = Customer.objects.get(user=User.objects.get(email='demo1@demo.com'))
        patient = Patient(user=customer,
                          first_name='de',
                          last_name='mo',
                          first_name_pinyin='dede',
                          last_name_pinyin='momo',
                          gender='M',
                          birthdate=datetime.datetime.now(),
                          relationship='other',
                          passport='1234567')
        patient.save()
        res = Reservation.objects.all()[0]
        print(res)
        res.save()

        url = reverse('document-list')
        data = {
            'data':'2345',
            'type':'2',
            'resid':res.res_id,

        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

