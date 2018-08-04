from collections import defaultdict
from datetime import datetime
from typing import List

from django.contrib.auth.models import User

from hospital.models import Hospital
from disease.models import Disease
from customer.models import Customer
from patient.models import Patient


def hospital_setup(num: int = 1) -> List:
    Hospital.objects.bulk_create(
        map(
            lambda i: Hospital(
                name="Dummy Hospital %d" % (i+1)
            ),
            range(num)
        )
    )
    return list(map(lambda h: h.id, Hospital.objects.all()))


def disease_setup(num: int = 1) -> List:
    Disease.objects.bulk_create(
        map(
            lambda i: Disease(
                name="Disease %d" % (i + 1)
            ),
            range(num)
        )
    )
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
    Patient.objects.bulk_create([
        Patient(
            user_id=customer,
            first_name="Patient %d" % j,
            last_name="of User %d" % i,
            first_name_pinyin="Patient %d" % j,
            last_name_pinyin="of User %d" % i,
            gender='MF'[j % 2],
            birthdate=datetime.now().date(),
            relationship="ship",
            passport="port"
        )
        for i, customer in enumerate(customers)
        for j in range(num)
    ])
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

        self.hospital = hospital_setup(hospital)
        self.disease = disease_setup(disease)
        self.customer = customer_setup(customer)
        self.patient = patient_setup(self.customer, patient)
