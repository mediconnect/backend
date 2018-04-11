from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Patient

# Create your tests here.
class PatientModuleTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_add_check_then_update(self):
        # Setup the patient
        patient_create_url = reverse('patient_create')
        sample_instance = {
            "user_id": "4f773",
            "first_name": "Test",
            "last_name": "Sicker",
            "first_name_pinyin": "Test",
            "last_name_pinyin": "Sicker",
            "gender": "M",
            "birthdate": "2017-01-01",
            "relationship": "dude",
            "passport": "E12345678",
        }

        response = self.client.post(patient_create_url, sample_instance, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Patient.objects.count(), 1)
        self.assertTrue(False)
        ## To be continued


