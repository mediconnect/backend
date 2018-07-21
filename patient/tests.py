from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
import json
from .models import Patient
from atlas.creator import with_optional_field_autofill

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
        self.assertEqual(with_optional_field_autofill(expecting_obj, response_obj.keys()), response_obj)

        # Successful Update
        patient_update_url = reverse('patient_update', kwargs={'ptid': ptid})
        update_instance = {
            "first_name_pinyin": "tai'si'te",
            "last_name_pinyin": "xi'ke'er"
        }
        response = self.client.post(patient_update_url, data=update_instance, format='json')
        response_obj = json.loads(response.content)
        expecting_obj = dict(sample_instance, id=ptid, **update_instance)
        self.assertEqual(with_optional_field_autofill(expecting_obj, response_obj.keys()), response_obj)

    def test_bad_inputs(self):
        ptid = 1
        patient_get_url = reverse('patient_get', kwargs={'ptid': ptid})
        err_resp = self.client.get(patient_get_url, format="json")
        self.assertEqual(err_resp.status_code, 400)
        # self.assertEqual(err_resp.content, {})

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

        patient_create_url = reverse("patient_create")
        err_resp = self.client.post(patient_create_url, data={'first_name': sample_instance['first_name']}, format='json')
        self.assertEqual(err_resp.status_code, 400)
        # self.assertEqual(err_resp.content, "")

        patient_update_url = reverse("patient_update", kwargs={'ptid': ptid})
        err_resp = self.client.post(patient_update_url, data=sample_instance, format='json')
        self.assertEqual(err_resp.status_code, 400)
        # self.assertEqual(err_resp.content, "")