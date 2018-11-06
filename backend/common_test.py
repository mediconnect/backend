import uuid
from collections import defaultdict
from datetime import datetime
from typing import List

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.urls import reverse

from rest_framework.test import APIClient,force_authenticate

from hospital.models import Hospital
from disease.models import Disease
from customer.models import Customer
from patient.models import Patient
from staff.models.supervisor import Supervisor
from staff.models.translator import Translator

client = APIClient()


def supervisor_setup():

    user = User(email='sup4Common@test.com',
                username='sup4Common',
                password=make_password('/.,Buz123'))
    user.save()
    supervisor = Supervisor(user=user)
    supervisor.save()

    return supervisor.user


def translator_setup():

    user = User(email='trans4Common@test.com',
                username='trans4Common',
                password=make_password('/.,Buz123'))
    user.save()
    translator = Translator(user=user,role=1)
    translator.save()

    return translator.user


def hospital_setup(num: int = 1) -> List:

    url = reverse('hospital-list')

    for i in range(num):

        data = {
            'id':uuid.uuid4(),
            'name':"Dummy Hospital %d" % i,
            'email': 'demo%d@demo.com' % i,
            'overall_rank': '%d' % i,
        }
        client.post(url, data, format='json')

    return list(map(lambda h: h.id, Hospital.objects.all()))


def disease_setup(num: int = 1) -> List:

    url = reverse('disease-list')
    for i in range(num):
        data = {
            'id': uuid.uuid4(),
            'name': "Dummy Disease %d" % i,

        }
        client.post(url, data, format='json')
    return list(map(lambda d: d.id, Disease.objects.all()))


def customer_setup(num: int = 1) -> List:
    users = map(
        lambda i: User.objects.create_user(
            username="User %d" % (i + 1),
            password="pwd"
        ),
        range(num)
    )

    Customer.objects.bulk_create(
        map(
            lambda user: Customer(
                user=user,
            ),
            users
        )
    )

    return list(map(lambda d: d.id, Customer.objects.all()))


def patient_setup(customers: List, num: int = 1) -> List:

    for i in range(num):
        for c_id in customers:
            customer=Customer.objects.get(id=c_id)
            client.force_login(user=customer.user)
            url = reverse('patient-list',args=(customer.id,))
            data = {
                'first_name':"Patient %d" % i,
                'last_name':"of User %d" % i,
                'first_name_pinyin':"Patient %d" % i,
                'last_name_pinyin':"of User %d" % c_id,
                'gender':'MF'[i % 2],
                'birthdate':datetime.now().date(),
                'relationship':"ship",
                'passport':"port",
                'notes':"something",

            }
            client.post(url, data, format='json')
            client.logout()

    return list(map(lambda d: d.id, Patient.objects.all()))


class CommonSetup:

    def __init__(self,
                 hospital: int = 0,
                 disease: int = 0,
                 customer: int = 1,
                 patient: int = 0,
                 **kwargs
                 ):
        kwargs_map = defaultdict(dict)
        for kw, arg in kwargs.items():
            kwsplits = kw.split('_')
            if len(kwsplits) == 1:
                continue
            kwspace = kwsplits.pop(0)
            kwkey = '_'.join(kwsplits)
            kwargs_map[kwspace][kwkey] = arg

        self.supervisor = supervisor_setup()
        self.translator =  translator_setup()
        client.force_login(self.supervisor)
        self.hospital = hospital_setup(hospital)
        self.disease = disease_setup(disease)
        client.logout()

        self.customer = customer_setup(customer)
        self.patient = patient_setup(self.customer, patient)

