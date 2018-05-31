import json
import uuid
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Requirement, FileType
from atlas.comparer import APITestCaseExtend


class SlotnModuleTest(APITestCaseExtend):
    def setUp(self):
        self.client = APIClient()

    def test_general(self):
        dummy_types = [{'name': 'test%d' % i, 'description': 'test%d' % i} for i in range(100)]
        create_ftype = reverse("filetype_create")
        response = self.client.post(create_ftype, data=dummy_types[0])
        self.assertDictIntersectEqual(json.loads(response), dummy_types[0])

        for each in dummy_types[1:50]:
            self.client.post(create_ftype, data=each)

        self.assertDictIntersectEqual(
            json.loads(self.client.get(reverse("filetype_get", kwargs={'ftid': 10}))),
            dummy_types[10]
        )