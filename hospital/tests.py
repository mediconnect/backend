import faker
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Custom settings goes here

# Test Database setup
class TestCreate(APITestCase):
    """
    Test create endpoints here
    """
    def setUp(self):
        self.fake = faker.Faker()
    def test_create_customer(self):
        url = reverse('create-customer')
        data = {''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_hospital(self):
        url = reverse('create-hospital')
        data = {'id' : self.fake.id(),
                'name': self.fake.name(),
                'email':self.fake.email(),
                'area': self.fake.area(),
                'overall_rank':self.fake.overall_rank(),
                'website':self.fake.website(),
                'introduction':self.fake.introduction()
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.statusgit_code, status.HTTP_201_CREATED)