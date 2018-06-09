from django.test import TestCase
from customer.models import Customer
from django.test import Client
import copy


class NormalRegisterTestCase(TestCase):
    """ Test normal customer registration procedural. """

    data = {
        'email': 'normal_test@test.com',
        'password': '/.,buz123',
        'password_confirmation': '/.,buz123',
        'first_name': 'do not fuck',
        'last_name': 'me',
        'tel': '123456789',
        'address': 'the test is awesome'
    }

    def setUp(self):
        Customer.objects.filter(user__email='normal_test@test.com').delete()

    def test_normal_register(self):
        c = Client()
        response = c.post('/register/', self.data)
        self.assertEqual(response.status_code, 200)


class RegisterExceptionHandlingTestCase(TestCase):
    """ Test customer registration exception. """

    data = {
        'email': 'exception_test@test.com',
        'password': '/.,buz123',
        'password_confirmation': '/.,buz123',
        'first_name': 'fuck',
        'last_name': 'me',
        'tel': '123456789',
        'address': 'the test is awesome'
    }
    fields = ['email', 'password', 'password_confirmation', 'first_name', 'last_name', 'tel', 'address']

    def setUp(self):
        Customer.objects.filter(user__email='exception_test@test.com').delete()

    def test_fields_blank_exception(self):
        c = Client()
        request = copy.deepcopy(self.data)
        for field in self.fields:
            request.pop(field, None)
            response = c.post('/register/', request)
            self.assertEqual(response.status_code, 400)
            request.update({field: self.data[field]})
