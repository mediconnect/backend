from django.urls import reverse
from rest_framework import status
from rest_framework.test import  APITestCase

from .models import Document


class UploadFileTest(APITestCase):

    def test_create_document(self):
        """
        Ensure that we can create a hospital
        """

