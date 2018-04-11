from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
import json
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
        # Successful Add
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Patient.objects.count(), 1)

        ptid = json.loads(response.content)['id']
        self.assertTrue(ptid > 0)

        # Successful Get
        patient_get_url = reverse('patient_get', kwargs={'ptid': ptid})
        response = self.client.get(patient_get_url, format='json')
        response_obj = json.loads(response.content)
        expecting_obj = dict(sample_instance, id=ptid)
        for k in response_obj.keys():
            if k not in expecting_obj:
                expecting_obj[k] = ""
        self.assertEqual(expecting_obj, response_obj)
        ## To be continued


