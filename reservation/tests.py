from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
import json
from .models import Reservation
from atlas.creator import with_optional_field_autofill

# Create your tests here.
class ReservationModuleTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_all_workflows(self):
        resv_init_sample = {
            'user_id': 1234,
            'patient_id': 2345,
            'hospital_id': 3456,
            'disease_id': 4567,
            'slot_id': 5678,
        }

        create_resv_url = reverse("reservation_init")
        response = self.client.put(create_resv_url, resv_init_sample, format='json')
        self.assertEqual(json.loads(response.content), {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reservation.objects.count(), 1)

        resvid = json.loads(response.content)['rid']

        get_resv_url = reverse("reservation_get", kwargs={'resid': resvid})
        response = self.client.get(get_resv_url)
        self.assertEqual(response.status_code, 200)
        response_obj = json.loads(response)
        self.assertEqual(resv_init_sample, dict(filter(lambda kv: kv[0] in resv_init_sample.keys(), response_obj.items())))
        self.assertNotEqual(response_obj.ctime, None)
        self.assertEqual(response_obj.commit_at, None)
        self.assertEqual(response_obj, None)
