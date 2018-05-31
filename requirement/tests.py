import json
import uuid
import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Requirement, FileType
from atlas.comparer import APITestCaseExtend


class SlotnModuleTest(APITestCaseExtend):
    def setUp(self):
        self.client = APIClient()
        self.maxDiff = None

    def test_general(self):
        dummy_types = [{'name': 'test%d' % i, 'description': 'test%d' % i} for i in range(100)]
        create_ftype = reverse("filetype_create")
        response = self.client.post(create_ftype, data=dummy_types[0])
        self.assertDictIntersectEqual(json.loads(response.content), dummy_types[0])

        for each in dummy_types[1:50]:
            self.client.post(create_ftype, data=each)

        self.assertDictIntersectEqual(
            json.loads(self.client.get(reverse("filetype_get", kwargs={'ftid': 10})).content),
            dummy_types[9]
        )

        dummy_requirement = {
            'hospital_id': uuid.uuid4(),
            'disease_id': 1,
            'types': sorted(random.sample(range(1, 51), 10))
        }
        create_requirement = reverse('requirement_set')
        response = self.client.post(create_requirement, data=dummy_requirement)
        res_json = json.loads(response.content)

        self.assertEqual(res_json['obsolete_types'], [])
        self.assertJSONEqual(res_json['created'], dummy_requirement)

        self.client.post(reverse('filetype_retire', kwargs={'ftid': dummy_requirement['types'][0]}))
        response = self.client.get(
            reverse('requirement_get', kwargs={'hospital': dummy_requirement['hospital_id'], 'disease': dummy_requirement['disease_id']})
        )
        self.assertJSONEqual(json.loads(response.content), dict(dummy_requirement, types=dummy_requirement['types'][1:]))

        FileType.objects.all().update(obsolete=True)
        self.client.post(create_ftype, data=dummy_types[50])
        response = self.client.post(create_requirement, data=dict(dummy_requirement, types=dummy_requirement['types'] + [51]))
        res_json = json.loads(response.content)

        self.assertEqual(res_json['obsolete_types'], dummy_requirement['types'])
        self.assertJSONEqual(res_json['created'], dict(dummy_requirement, types=[51]))

